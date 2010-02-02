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

from twisted.internet import reactor, defer
from twisted.python import log, failure
from txirods.encoding import binary as messages
from txirods import api
from md5 import md5
from construct import Container
import logging

from protocol import IRODSChannel, Request


from txirods.encoding import rods2_1_binary_inp, rods2_1_generic, \
                        rods2_1_binary_out

class IRODS(IRODSChannel):
    def __init__(self):
        IRODSChannel.__init__(self)
        self.msg_len = 0
        self.api = 0
        self.consumer = None
        self.bytestream_consumer = None
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

        if request.bs_consumer:
            self.bytestream_consumer = request.bs_consumer
            self.bytestream_consumer.registerProducer(self, False)

        self.sendMessage(request.msg_type,
                         int_info=request.int_info,
                         bs_len=request.bs_len,
                         err_len=request.err_len,
                         data=request.data)

        if request.data_stream_cb:
            request.data_stream_cb.callback(None)


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
                            len = 8,
                            inx = ['COL_COLL_NAME', 'COL_DATA_NAME',
                                   'COL_D_DATA_ID', 'COL_D_OWNER_NAME',
                                   'COL_DATA_MODE', 'COL_DATA_SIZE',
                                   'COL_D_MODIFY_TIME', 'COL_D_CREATE_TIME'],
                            value = [1, 1, 1, 1, 1, 1, 1, 1]),
                         inxValPair = Container(
                            len = 1,
                            inx = ['COL_COLL_NAME'],
                            value = [" = '%s'" % path]),
                         maxRows = 500, options = 32, partialStartIndex = 0)
        d = self.sendApiReq(int_info=api.GEN_QUERY_AN,
                            data=self.api_request_map[api.GEN_QUERY_AN].build(data))
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
        d = self.sendApiReq(int_info=api.COLL_CREATE_AN,
                            data=self.api_request_map[api.COLL_CREATE_AN].build(data))
        d.addBoth(self.sendNextRequest)
        return d


    def rmcoll(self, path='', recursive=False):
        """
        remove collection
        """
        data = Container(collName = path,
                         flags = 0,
                         oprType = 0,
                         keyValPair = Container(keyWords = None,
                                                len = 0,
                                                values = None))
        if recursive:
            data.keyValPair = Container(keyWords = ['recursiveOpr'],
                                        len = 1,
                                        values = [''])
        d = self.sendApiReq(int_info=api.RM_COLL_AN,
                            data=self.api_request_map[api.RM_COLL_AN].build(data))
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
                            inx = ['COL_COLL_NAME',
                                   'COL_COLL_OWNER_NAME',
                                   'COL_COLL_CREATE_TIME',
                                   'COL_COLL_MODIFY_TIME',
                                   'COL_COLL_TYPE',
                                   'COL_COLL_INFO1',
                                   'COL_COLL_INFO2'],
                            value = [1, 1, 1, 1, 1, 1, 1]),
                         inxValPair = Container(
                            len = 1,
                            inx = ['COL_COLL_PARENT_NAME'],
                            value = [" = '%s'" % path]),
                         maxRows = 500, options = 32, partialStartIndex = 0)
        d = self.sendApiReq(int_info=api.GEN_QUERY_AN,
                            data=self.api_request_map[api.GEN_QUERY_AN].build(data))
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
        d = self.sendApiReq(int_info=api.OBJ_STAT_AN,
                            data=self.api_request_map[api.OBJ_STAT_AN].build(data))
        d.addBoth(self.sendNextRequest)
        return d


    def put(self, producer_cb, objPath, size):
        """
        send a file to irods

        :param producer_cb: a callback that registers a producer to start producing over clients transport.
        :param objPath: the location of the object
        :type objPath: String
        :param size: the size of the object in bytes
        :type size: Int
        :rtype: :class:`~twisted.internet.defer.Deferred`
        """
        data = Container(createMode = 33261,
                         dataSize = size,
                         keyValPair = Container(
                             len = 2,
                             keyWords = ['dataType', 'dataIncluded'],
                             values = ['generic', '']),
                         numThreads = 0,
                         objPath = objPath,
                         offset = 0,
                         openFlags = 2,
                         oprType = 1,
                         specColl = None)
        d = self.sendApiReq(int_info=api.DATA_OBJ_PUT_AN, bs_len=size,
                            data=self.api_request_map[api.DATA_OBJ_PUT_AN].build(data),
                            data_stream_cb=producer_cb)
        d.addBoth(self.sendNextRequest)
        return d


    def get(self, consumer, objPath, size):
        """
        get a file from irods

        :param consumer: provides :class:`~twisted.internet.interfaces.IConsumer`.
        :param objPath: the location of the object
        :type objPath: String
        :param size: the size of the object in bytes
        :type size: Int
        :rtype: :class:`~twisted.internet.defer.Deferred`
        """

        data = Container(createMode = 0,
                         dataSize = size,
                         keyValPair = Container(keyWords = None,
                                                len = 0,
                                                values = None),
                         numThreads = 0,
                         objPath = objPath,
                         offset = 0,
                         openFlags = 0,
                         oprType = 2,
                         specColl = None)

        d = self.sendApiReq(int_info=api.DATA_OBJ_GET_AN,
                            data=self.api_request_map[api.DATA_OBJ_GET_AN].build(data),
                            bs_consumer=consumer)
        d.addBoth(self.sendNextRequest)
        return d


    def rmobj(self, path='', force=False):
        """
        unlink an object from the irods file system
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
        if force:
            data.keyValPair = Container(keyWords = ['forceFlag'],
                                        len = 1,
                                        values = [''])
        d = self.sendApiReq(int_info=api.DATA_OBJ_UNLINK_AN,
                            data=self.api_request_map[api.DATA_OBJ_UNLINK_AN].build(data))
        d.addBoth(self.sendNextRequest)
        return d


    def sendApiReq(self, int_info=0, err_len=0, bs_len=0, data='', bs_consumer=None, data_stream_cb=None):
        d = defer.Deferred()
        r = Request()
        r.deferred = d
        r.msg_type = 'RODS_API_REQ'
        r.int_info = int_info
        r.bs_len = bs_len
        r.err_len = err_len
        r.data = data
        r.data_stream_cb = data_stream_cb
        r.bs_consumer = bs_consumer
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
        d = self.sendApiReq(api.GSI_AUTH_REQUEST_AN)
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
        d = self.sendApiReq(api.AUTH_REQUEST_AN)
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
        self.sendMessage(msg_type='RODS_API_REQ',
                         int_info=api.AUTH_RESPONSE_AN,
                         data=resp + userandzone + '\0')


    def handleAuthChallangeResponse(self, data):
        if self.response.intinfo >= 0:
            log.msg("\nSuccessfully authed\n", debug=True)
            self.nextDeferred.callback("Authed")

    def miscServerInfo(self):
        d = self.sendApiReq(api.GET_MISC_SVR_INFO_AN)
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

        if self.response.msg_type in self.generic_reponse_map:
            try:
                data = self.generic_reponse_map[self.msg_type](data)
            except:
                self.nextDeferred.errback(failure.Failure())
            else:
                self.nextDeferred.callback(data)
            return

        if self.int_info == api.AUTH_REQUEST_AN:
            self.handleAuthChallange(data)
            return


    def processByteStream(self, data):
        self.bytestream_consumer.write(data)
        if self.bytestream_len == 0:
            self.bytestream_consumer.unregisterProducer()
            self.bytestream_consumer = None
            self.nextDeferred.callback('')


    def processOther(self, data):
        log.msg("\nPROCESSOTHER\n", debug=True)
        if self.int_info == api.GSI_AUTH_REQUEST_AN:
            self.handleAuthGsi(data, True)
            return True
        if self.int_info == api.AUTH_RESPONSE_AN:
            self.handleAuthChallangeResponse(data)
            return

        # handle empty reponse messages
        if self.int_info in [api.COLL_CREATE_AN,
                             api.DATA_OBJ_PUT_AN,
                             api.DATA_OBJ_UNLINK_AN]:
            if self.response.intinfo >= 0:
                self.nextDeferred.callback('')
            return


class IRODSClient(IRODS):
    def connectionLost(self, *a):
        self.nextDeferred.callback('Connection closed by remote host.')

