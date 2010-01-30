#############################################################################
#
# Copyright (c) 2009 Victorian Partnership for Advanced Computing Ltd and
# Contributors.
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
from twisted.internet.interfaces import IPushProducer
from twisted.internet import defer, reactor
from twisted.protocols import basic
from twisted.python import log, failure, filepath
from zope.interface import implements
import struct
from txirods.encoding import binary as messages
from txirods import errors
from md5 import md5
from xml.sax import make_parser
from pyGlobus.security import GSSCred, GSSContext, GSSContextException
from pyGlobus.security import GSSName, GSSMechs, GSSUsage
from pyGlobus.security import ContextRequests, GSSCredException
from pyGlobus import gssc
from construct import Container
import logging

from txirods.header import IRODSHeaderHandler

class IRODSGeneralException(Exception):
    def __init__(self, errorNumber):
        self.errorNumber = errorNumber

    def errorName(self):
        error_name = 'UNKNOWN'
        if errors.int_to_const.has_key(self.errorNumber):
            error_name = errors.int_to_const[self.errorNumber]
        return error_name

    def __str__(self):
        return "General iRODS API exception %s: %s" % (self.errorName(), self.errorNumber)


class GSIAuth(object):
    implements(IPushProducer)

    def beginAuthentication(self, data, consumer, producer):
        self.paused = 0; self.stopped = 0
        self.consumer = consumer
        self.producer = producer
        self.deferred = deferred = defer.Deferred()
        self.consumer.registerProducer(self, False)
        self.producer.registerConsumer(self)
        self.data = {}
        self.buffer = ''
        self.resumeProducing(data, first=True)
        return deferred

    def pauseProducing(self):
        self.paused = True

    def write(self, data):
        # TODO should use the buffer in the class
        #self.buffer = self.buffer + data
        self.resumeProducing(data)

    def resumeProducing(self, data='', first=False):
        # transport calls resumeProducing when this is attached
        if not first and not data:
            return
        self.paused = False
        if first:
            if not data:
                # Already Authed because there was no DN recieved from the server
                self.consumer.unregisterProducer()
                self.producer.unregisterConsumer()
                reactor.callLater(0.001, self.deferred.callback, True)
                return
            server_dn = data.split('\0')[0]
            log.msg(server_dn)
            self.data['server_dn'] = server_dn

            # create credential
            init_cred = GSSCred()
            name, mechs, usage  = GSSName(free=False), GSSMechs(), GSSUsage()

            try:
                init_cred.acquire_cred(name, mechs, usage)
            except GSSCredException:
                self.deferred.errback()
                return

            try:
                lifetime, credName = init_cred.inquire_cred()
            except GSSCredException:
                self.deferred.errback()
                return

            context = GSSContext()
            requests = ContextRequests()

            target_name = GSSName()
            major, minor, targetName_handle = gssc.import_name('arcs-df.vpac.org', gssc.cvar.GSS_C_NT_HOSTBASED_SERVICE)
            target_name._handle = targetName_handle

            requests.set_mutual()
            requests.set_replay()

            self.data.update({'name':name, 'lifetime':lifetime, 'credName':credName,
                              'targetName':target_name, 'todelete':name,
                              'context':context, 'requests':requests, 'cred': init_cred})
        else:
            context = self.data['context']
            init_cred=self.data['cred']
            target_name=self.data['targetName']
            requests=self.data['requests']
            self.buffer = self.buffer + data
            data = self.buffer

        try:
            major,minor,outToken = context.init_context(init_cred=init_cred,
                                                        target_name=target_name,
                                                        inputTokenString=data,
                                                        requests=requests)
        except GSSContextException:
            # XXX this doesn't seem to be called, no idea
            print GSSContextException
        else:
            self.buffer = ''

        self.consumer.write(outToken)
        # XXX WTF is with this number?
        if major == gssc.GSS_S_COMPLETE:
            # Reset all class variables
            self.consumer.msg_len = 0
            self.consumer.unregisterProducer()
            self.producer.unregisterConsumer()
            reactor.callLater(0.001, self.deferred.callback, True)
        return

    def stopProducing(self):
        print 'stopProducing: invoked'
        self.consumer.unregisterProducer()
        self.producer.unregisterConsumer()



class Request(object):
    def __init__(self):
        self.deferred = defer.Deferred()
        self.int_info = 0
        self.msg_type =''
        self.data = ''


class Response(object):
    def __init__(self):
        self.msg_type = ''
        self.msg_len = 0
        self.err_len = 0
        self.bs_len = 0
        self.intinfo = 0

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
        """
        msg_len = len(data)
        self.int_info = int(int_info)
        header = messages.header.substitute({'type':msg_type,
                                             'msg_len':msg_len,
                                             'err_len':err_len,
                                             'bs_len':bs_len,
                                             'int_info':int_info})
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
            # XXX Backwards compatability from before i had a response object
            self.msg_len = self.response.msg_len
            self.msg_type = self.response.msg_type

            self.parser.close()
            self.parser = None
            self._processed_header = True
            self.message_len, self.error_len, self.bytestream_len = self.response.getMessageLengths()

        rawdata = data[self.header_len:]

        self.header_len = self.header_len - len(data[:self.header_len])

        if self.response.intinfo < 0:
            self.nextDeferred.errback(IRODSGeneralException(self.response.intinfo))


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
            # probably doesn't need buffer
            if len(data) < self.bytestream_len:
                self._buffer = self._buffer + data
                if len(self._buffer) < self.bytestream_len:
                    return
                data = self._buffer
                self._buffer = ''
            self.bytestream_len = self.bytestream_len - len(data)
            return self.processByteStream(data)

        return self.processOther(data)


    def processMessage(self, data):
        pass


    def processError(self, data):
        pass


    def processByteStream(self, data):
        pass


    def processOther(self, data):
        pass


    def doneProcessing(self):
        self._processed_header = False
        self._buffer = ''
        log.msg("\nDONE PROCESSING\n")


from txirods.encoding import rods2_1_binary_inp, rods2_1_generic, \
                        rods2_1_binary_out

class IRODS(IRODSChannel):
    def __init__(self):
        IRODSChannel.__init__(self)
        self.msg_len = 0
        self.api = 0
        self.consumer = None
        self.data = ''
        self.api_reponse_map = rods2_1_binary_out
        self.api_request_map = rods2_1_binary_inp
        self.generic_reponse_map = rods2_1_generic
        self.request_queue = defer.DeferredQueue()
        self.nextDeferred = None


    def sendRequest(self, request):
        log.msg('===========SEND=REQUEST============')
        self.nextDeferred = request.deferred
        self.int_info = request.int_info
        self.sendMessage(request.msg_type, int_info=request.int_info, data=request.data)


    def sendNextRequest(self, data):
        self.request_queue.get().addCallback(self.sendRequest)
        return data


    def connectionMade(self):
        self.sendNextRequest(None)


    def finishConnect(self, data):
        log.msg("\nFinish connection, by setting up api and version info\n", debug=True)


    def listObjects(self, path=''):
        """
        list the objects in a collection at path
        """
        data = Container(keyValPair = Container(len = 0,
                                                keyWords = None,
                                                values = None),
                         continueInx = 0,
                         inxIvalPair = Container(
                            len = 7,
                            inx = [501, 403, 401, 421, 407, 420, 419],
                            value = [1, 1, 1, 1, 1, 1, 1]),
                         inxValPair = Container(
                            len = 1,
                            inx = [501],
                            value = [" = '%s'" % path]),
                         maxRows = 500, options = 32, partialStartIndex = 0)
        d = self.sendApiReq(int_info=702,
                            data=self.api_request_map[702].build(data))
        d.addBoth(self.sendNextRequest)
        return d


    def mkcoll(self, path=''):
        """
        make a new collection
        """
        data = Container(collName = path,
                         flags = 0,
                         oprType = 0,
                         keyValPair = Container(len = 0,
                                                keyWords = None,
                                                values = None),)
        d = self.sendApiReq(int_info=681,
                            data=self.api_request_map[681].build(data))
        d.addBoth(self.sendNextRequest)
        return d


    def listCollections(self, path=''):
        """
        list the collections in a collection at path
        """
        data = Container(keyValPair = Container(len = 0,
                                                keyWords = None,
                                                values = None),
                         continueInx = 0,
                         inxIvalPair = Container(
                            len = 7,
                            inx = [501, 503, 508, 509, 510, 511, 512],
                            value = [1, 1, 1, 1, 1, 1, 1]),
                         inxValPair = Container(
                            len = 1,
                            inx = [502],
                            value = [" = '%s'" % path]),
                         maxRows = 500, options = 32, partialStartIndex = 0)
        d = self.sendApiReq(int_info=702,
                            data=self.api_request_map[702].build(data))
        d.addBoth(self.sendNextRequest)
        return d


    def objStat(self, path=''):
        """
        stat the details of an object
        """
        data = Container(keyValPair = Container(len = 0,
                                                keyWords = None,
                                                values = None),
                         createMode = 0,
                         dataSize = 0,
                         numThreads = 0,
                         objPath = path,
                         offset = 0,
                         openFlags = 0,
                         oprType = 0,
                         specColl = None)
        d = self.sendApiReq(int_info=633,
                            data=self.api_request_map[633].build(data))
        d.addBoth(self.sendNextRequest)
        return d


    def put(self, file=None, remotefile=None):
        """
        send a file to irods
        """
        f = filepath.FilePath(file)
        size = f.getsize()

        data = Container(createMode = 33261,
                         dataSize = size,
                         keyValPair = Container(
                             len = 2,
                             keyWords = ['dataType', 'dataIncluded'],
                             values = ['generic', '']),
                         numThreads = 0,
                         objPath = remotefile,
                         offset = 0,
                         openFlags = 2,
                         oprType = 1,
                         specColl = None)
        d = self.sendApiReq(int_info=606, bs_len=size,
                            data=self.api_request_map[606].build(data))
        p = f.open('rb')
        d = basic.FileSender().beginFileTransfer(p, self.transport)
        d.addCallback(self.nextDeferred.callback)


    def sendApiReq(self, int_info=0, err_len=0, bs_len=0, data=''):
        d = defer.Deferred()
        r = Request()
        r.deferred = d
        r.msg_type = 'RODS_API_REQ'
        r.int_info = int_info
        r.data = data
        self.request_queue.put(r)
        return d


    def sendDisconnect(self, err_len=0, bs_len=0, int_info=0, data=''):
        d = defer.Deferred()
        d.addCallback(self.sendNextRequest)
        r = Request()
        r.deferred = d
        r.msg_type = 'RODS_DISCONNECT'
        self.request_queue.put(r)
        return d


    def sendConnect(self, reconnFlag=0, connectCnt=0, proxy_user='',
                    proxy_zone='', client_user='', client_zone='', option=''):
        log.msg("\nsendConnect\n", logging.INFO)
        self.connect_info = {'irodsProt':self.api, 'reconnFlag': reconnFlag,
                             'connectCnt': connectCnt, 'proxy_user':proxy_user,
                             'proxy_zone': proxy_zone, 'client_user': client_user,
                             'client_zone': client_zone, 'option': option}
        startup = messages.connect.substitute(self.connect_info)
        d = defer.Deferred()
        d.addCallback(self.finishConnect)
        d.addCallback(self.sendNextRequest)
        r = Request()
        r.deferred = d
        r.msg_type = 'RODS_CONNECT'
        r.data = startup
        self.request_queue.put(r)
        return d


    def registerConsumer(self, consumer):
        if self.consumer:
            raise Exception("Can't register consumer, another consumer is registered")
        self.consumer = consumer


    def unregisterConsumer(self):
        self.consumer = None



    def sendAuthGsi(self):
        d = self.sendApiReq(711)
        d.addCallback(self.sendNextRequest)
        return d

    def handleAuthGsi(self, data, first=False):
        """
        irods GSI auth reply
        """
        def unhook(data, prot):
            reactor.callLater(0.001, prot.sendNextRequest)
            return data

        a = GSIAuth()
        d = a.beginAuthentication(data, self.transport, self)
        d.addCallback(unhook, self)
        d.addCallback(self.nextDeferred.callback)
        return


    def sendAuthChallenge(self, password):
        self.password = password
        d = self.sendApiReq(703)
        d.addBoth(self.sendNextRequest)
        return d


    def handleAuthChallange(self, data):
        log.msg("\nChallenge\n" + repr(data), debug=True)
        MAX_PASSWORD_LEN = 50
        CHALLENGE_LEN = 64
        resp_len = CHALLENGE_LEN + MAX_PASSWORD_LEN

        resp = data + self.password
        del self.password

        # response is padded with binary nulls
        resp = resp + '\0' * (resp_len - len(resp))
        resp = md5(resp).digest()

        # replace and 0 with 1
        resp = resp.replace('\0', '\x01')

        userandzone = self.connect_info['proxy_user'] + '#' \
                + self.connect_info['proxy_zone']
        # pad message with 0
        self.sendMessage(msg_type='RODS_API_REQ', int_info=704, data=resp + userandzone + '\0')


    def handleAuthChallangeResponse(self, data):
        if self.response.intinfo >= 0:
            log.msg("\nSuccessfully authed\n", debug=True)
            self.nextDeferred.callback("Authed")

    def miscServerInfo(self):
        d = self.sendApiReq(700)
        d.addCallback(self.sendNextRequest)
        return d

    def processMessage(self, data):
        """
        irods message processing
        """
        log.msg("\nPROCESSMESSAGE\n", debug=True)
        if self.int_info in self.api_reponse_map:
            try:
                data = self.api_reponse_map[self.int_info].parse(data)
            except:
                self.nextDeferred.errback(failure.Failure())
            else:
                self.nextDeferred.callback(data)
            return

        if self.msg_type in self.generic_reponse_map:
            try:
                data = self.generic_reponse_map[self.msg_type](data)
            except:
                self.nextDeferred.errback(failure.Failure())
            else:
                self.nextDeferred.callback(data)
            return

        if self.int_info == 703:
            self.handleAuthChallange(data)
            return


    def processOther(self, data):
        log.msg("\nPROCESSOTHER\n", debug=True)
        if self.int_info == 711:
            self.handleAuthGsi(data, True)
            return True
        if self.int_info == 704:
            self.handleAuthChallangeResponse(data)
            return

        # handle empty reponse messages
        if self.int_info in [681,]:
            self.nextDeferred.callback('')
            return

