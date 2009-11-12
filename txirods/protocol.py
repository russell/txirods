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
import messages
import errors
from xml.dom import minidom
from pyGlobus.security import GSSCred, GSSContext, GSSContextException
from pyGlobus.security import GSSName, GSSMechs, GSSUsage
from pyGlobus.security import ContextRequests, GSSCredException
from pyGlobus import gssc
from construct import Container
import logging

class IRODSGeneralException(Exception):
    def __init__(self, errorNumber, errorName):
        self.errorName = errorName
        self.errorNumber = errorNumber

    def __str__(self):
        return "General iRODS API exception %s: %s" % (self.errorName, self.errorNumber)


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


class IRODS(Protocol):
    def __init__(self):
        self.msg_len = 0
        self.api = 0
        self.consumer = None
        self.data = ''


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
        #log.msg("\n--------SEND\n" + header + repr(data), debug=True)
        num = struct.pack('!L', len(header))
        self.transport.write(num + header + data)

    def list_objects(self, path=''):
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
        self.sendApiReq(int_info=702, data=messages.genQueryInp.build(data))


    def list_collections(self, path=''):
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
        self.sendApiReq(int_info=702, data=messages.genQueryInp.build(data))


    def obj_stat(self, path=''):
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
        self.sendApiReq(int_info=633, data=messages.dataObjInp.build(data))

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
        self.sendApiReq(int_info=606, bs_len=size, data=messages.dataObjInp.build(data))
        p = f.open('rb')
        d = basic.FileSender().beginFileTransfer(p, self.transport)
        d.addCallback(self.nextDeferred.callback)


    def sendApiReq(self, int_info=0, err_len=0, bs_len=0, data=''):
        self.sendMessage('RODS_API_REQ', err_len, bs_len, int_info, data)


    def sendDisconnect(self, err_len=0, bs_len=0, int_info=0, data=''):
        self.sendMessage('RODS_DISCONNECT', err_len, bs_len, int_info, data)


    def sendConnect(self, reconnFlag=0, connectCnt=0, proxy_user='', proxy_zone='', client_user='', client_zone='', option=''):
        log.msg("\nsendConnect\n", logging.INFO)
        startup = messages.connect.substitute({'irodsProt':self.api, 'reconnFlag': reconnFlag,
                                               'connectCnt': connectCnt, 'proxy_user':proxy_user,
                                               'proxy_zone': proxy_zone, 'client_user': client_user,
                                               'client_zone': client_zone, 'option': option})
        self.sendMessage('RODS_CONNECT',data=startup)


    def _rods_api_reply_633(self, data):
        """
        irods object stat reply
        """
        try:
            data = messages.rodsObjStat.parse(data)
        except:
            self.nextDeferred.errback(failure.Failure())
        else:
            self.nextDeferred.callback(str(data))

    def _rods_api_reply_702(self, data, first=False):
        """
        irods gen query reply
        """
        try:
            data = messages.genQueryOut.parse(data)
        except:
            self.nextDeferred.errback(failure.Failure())
        else:
            self.nextDeferred.callback(data)

    def registerConsumer(self, consumer):
        if self.consumer:
            raise Exception("Can't register consumer, another consumer is registered")
        self.consumer = consumer

    def unregisterConsumer(self):
        self.consumer = None

    def _rods_api_reply_711(self, data, first=False):
        """
        irods GSI auth reply
        """
        def unhook(data, prot):
            reactor.callLater(0.001, prot.sendNextCommand)
            return data

        a = GSIAuth()
        d = a.beginAuthentication(data, self.transport, self)
        d.addCallback(unhook, self)
        d.addCallback(self.nextDeferred.callback)
        return


    def _rods_api_reply_700(self, data):
        """
        irods server info reply
        """
        server_info = {}
        d = struct.unpack('!iI', data[:8])
        server_info['serverType'] = d[0]
        server_info['serverBootTime'] = d[1]
        d = data[8:].split('\0')
        server_info['relVersion'] = d[0]
        server_info['apiVersion'] = d[1]
        server_info['rodsZone'] = d[2]
        log.msg(str(server_info))
        self.nextDeferred.callback(server_info)


    def _rods_version(self, data):
        """
        irods version reply

        <Version_PI>
        <status>0</status>
        <relVersion>rods2.1</relVersion>
        <apiVersion>d</apiVersion>
        <reconnPort>0</reconnPort>
        <reconnAddr></reconnAddr>
        <cookie>0</cookie>
        </Version_PI>
        """
        self.nextDeferred.callback(data)


    def responseReceived(self):
        log.msg('Response Received', logging.INFO)


    def dataReceived(self, data):
        if self.consumer:
            self.consumer.write(data)
            return
        #log.msg("\n--------RECIEVE\n" + repr(data), debug=True)
        if self.msg_len < 1:
            if data[4:].startswith('<MsgHeader_PI>'):
                eom = struct.unpack('!L', data[:4])[0] + 4
                header = data[4:eom]
                data = data[eom:]
                msg = minidom.parseString(header)
                msg_type = msg.getElementsByTagName('type')[0].childNodes[0].data
                msg_len = msg.getElementsByTagName('msgLen')[0].childNodes[0].data
                err_len = msg.getElementsByTagName('errorLen')[0].childNodes[0].data
                bs_len = msg.getElementsByTagName('bsLen')[0].childNodes[0].data
                intinfo = int(msg.getElementsByTagName('intInfo')[0].childNodes[0].data)
                self.msg_len = int(msg_len)
                self.msg_type = msg_type
                if intinfo < 0:
                    error_name = 'UNKNOWN'
                    if errors.int_to_const.has_key(intinfo):
                        error_name = errors.int_to_const[intinfo]
                    try:
                        raise IRODSGeneralException(intinfo, error_name)
                    except:
                        self.nextDeferred.errback(failure.Failure())

        self.msg_len = self.msg_len - len(data)

        if self.int_info == 711:
            self._rods_api_reply_711(data, True)
            return
        if data:
            #print 'Calling: _' + self.msg_type.lower()
            if hasattr(self, '_' + self.msg_type.lower()):
                getattr(self, '_' + self.msg_type.lower())(data)
                return
            #print 'Calling: _' + self.msg_type.lower() + '_%s' % self.int_info
            elif hasattr(self, '_' + self.msg_type.lower() + '_%s' % self.int_info):
                getattr(self, '_' + self.msg_type.lower() + '_%s' % self.int_info)(data)
                return
            else:
                self.nextDeferred.callback(data)






