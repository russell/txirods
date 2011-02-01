#############################################################################
#
# Copyright (c) 2010 Russell Sim <russell.sim@gmail.com> and Contributors.
# All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from twisted.internet.protocol import Protocol
from twisted.internet import interfaces
from twisted.internet import defer
from twisted.python import log
from zope.interface import implements
import struct
from txirods.encoding import binary as messages
from txirods import errors
from xml.sax import make_parser

from txirods.header import IRODSHeaderHandler


class FileRecever(object):
    """
    A consumer consumes data from a producer.
    """
    implements(interfaces.IConsumer)

    def __init__(self, filename):
        self.file = open(filename, 'w')

    def registerProducer(self, producer, streaming):
        """
        Register to receive data from a producer.

        This sets self to be a consumer for a producer.  When this object runs
        out of data (as when a send(2) call on a socket succeeds in moving the
        last data from a userspace buffer into a kernelspace buffer), it will
        ask the producer to resumeProducing().

        For :class:`~twisted.internet.interfaces.IPullProducer` providers,
        C{resumeProducing} will be called once each time data is required.

        For :class:`~twisted.internet.interfaces.IPushProducer` providers,
        C{pauseProducing} will be called whenever the write buffer fills up
        and C{resumeProducing} will only be called when it empties.

        :param producer: :class:`~twisted.internet.interfaces.IProducer`
           provider
        :param streaming: True if producer provides
           :class:`~twisted.internet.interfaces.IPushProducer`, False if
           producer provides
           :class:`~twisted.internet.interfaces.IPullProducer`.
        :type streaming: Bool
        :raises RuntimeError: If a producer is already registered.
        :rtype: None
        """
        self.producer = producer
        self.producerIsStreaming = streaming

    def unregisterProducer(self):
        """
        Stop consuming data from a producer, without disconnecting.
        """
        if self.producer is not None:
            del self.producer
            del self.producerIsStreaming
            self.file.close()
            del self.file

    def write(self, data):
        """
        The producer will write data by calling this method.
        """
        self.file.write(data)


class Request(object):
    """
    This object contains the information required to start sending and
    recieve a command.

    :var int_info: the message API number
    :var err_len: the length of the error component of the message.
    :var bs_len: the length of the byte stream component of the message.
    :var msg_type: the type of message to be sent.
    :var data: the data to be sent in the message.
    :var bs_consumer: byte stream consumer to recieve data.
    :var data_stream_cb: a callback that starts byte stream producer.
    """
    def __init__(self):
        self.deferred = defer.Deferred()
        self.int_info = 0
        self.err_len = 0
        self.bs_len = 0
        self.msg_type = ''
        self.data = ''
        self.bs_consumer = None
        self.data_stream_cb = None


class Response(object):
    """
    This object contains the information returned from the server.

    :var int_info: the message API number
    :var err_len: the length of the error component of the message.
    :var bs_len: the length of the byte stream component of the message.
    :var msg_type: the type of message to be sent.
    :var msg_len: the length of the message.
    """
    def __init__(self):
        self.msg_type = ''
        self.msg_len = 0
        self.err_len = 0
        self.bs_len = 0
        self.int_info = 0

    def getMessageLengths(self):
        return (self.msg_len, self.err_len, self.bs_len)


class IRODSChannel(Protocol):
    def __init__(self):
        self.consumer = None
        self.parser = None
        self.header_len = 0
        self.message_len = 0
        self.error_len = 0
        self.bytestream_len = 0
        self._processed_header = False
        self._buffer = ''

    def sendMessage(self, msg_type='', err_len=0, bs_len=0, int_info=0,
                    data=''):
        """
        wrap an irods message with a header and send it

        :param msg_type: the message type
        :type msg_type: str
        :param err_len: the size of the error component of the message
        :type err_len: int
        :param bs_len: the size of the byte stream component of the message
        :type bs_len: int
        :param int_info: the const that represents the type of message
        :type int_info: int
        :type data: str
        :rtype: None
        """
        msg_len = len(data)
        self.int_info = int(int_info)
        header = messages.header.substitute({'type': msg_type,
                                             'msg_len': msg_len,
                                             'err_len': err_len,
                                             'bs_len': bs_len,
                                             'int_info': int_info})
        log.msg("\n--------SEND\n" + header + repr(data), debug=True)
        num = struct.pack('!L', len(header))
        self.transport.write(num + header + data)

    def dataReceived(self, data):
        if self.consumer:
            self.consumer.write(data)
            return
        log.msg("\n--------RECIEVE\n" + repr(data), debug=True)

        if not self._processed_header:
            data = self.headerReceived(data)
        if not self._processed_header:
            return
        log.msg("\n--------Data\n" + repr(data), debug=True)

        if self.processData(data):
            return

        if self.message_len or self.error_len or self.bytestream_len:
            return

        self.doneProcessing()

    def headerReceived(self, data):
        if self._processed_header:
            return data

        if not self.header_len:
            self._buffer = self._buffer + data
            if len(self._buffer) < 4:
                return
            data = self._buffer
            self._buffer = ''
            self.header_len = struct.unpack('!L', data[:4])[0]
            data = data[4:]
            self.response = Response()
            self.parser = make_parser()
            self.parser.setContentHandler(IRODSHeaderHandler(self.response))

        self.parser.feed(data[:self.header_len])

        # if we just processed the last part of the header, cleanup and finish
        if self.header_len <= len(data):
            self.parser.close()
            self.parser = None
            self._processed_header = True
            self.message_len, self.error_len, self.bytestream_len = \
                self.response.getMessageLengths()

        rawdata = data[self.header_len:]

        self.header_len = self.header_len - len(data[:self.header_len])

        if self.response.int_info < 0:
            if self.response.int_info in errors.int_to_cls:
                self.nextDeferred.errback(
                    errors.int_to_cls[self.response.int_info]())
            else:
                general_error = errors.IRODSException()
                general_error.number = self.response.int_info
                self.nextDeferred.errback(general_error)

        return rawdata

    def processData(self, data):
        if self.message_len:
            if len(data) < self.message_len:
                self._buffer = self._buffer + data
                if len(self._buffer) < self.message_len:
                    return
                data = self._buffer
                self._buffer = ''
            self.message_len = self.message_len - len(data)
            return self.processMessage(data)

        if self.error_len:
            if len(data) < self.error_len:
                self._buffer = self._buffer + data
                if len(self._buffer) < self.error_len:
                    return
                data = self._buffer
                self._buffer = ''
            self.error_len = self.error_len - len(data)
            return self.processError(data)

        if self.bytestream_len:
            self.bytestream_len = self.bytestream_len - len(data)
            return self.processByteStream(data)

        return self.processOther(data)

    def processMessage(self, data):
        """
        This function is called once the message header is parsed and the
        message body has been loaded into a buffer.
        """
        pass

    def processError(self, data):
        """
        This function is called once the message header is parsed and the
        error has been loaded into a buffer.
        """
        pass

    def processByteStream(self, data):
        """
        This function is called as data arrives, until there is no more to
        be sent.
        """
        pass

    def processOther(self, data):
        """
        This function is called last and is used to handle data that doesn't
        fit within the normal constraints of a response.

        To force this to be called again, return True
        """
        pass

    def doneProcessing(self):
        """
        After all other process functions have finished this function is
        called to cleanup the state of the protocol.
        """
        self._processed_header = False
        self._buffer = ''
        log.msg("\nDONE PROCESSING\n")
