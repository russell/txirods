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


from construct import Container

from txirods import api
from txirods.encoding.binary import rodsObjStat, genQueryOut, miscSvrInfo
from txirods.encoding.binary import collOprStat, collInp21
from txirods.encoding.binary import collInp, genQueryInp, dataObjInp
from txirods.encoding.binary import connect
from txirods.encoding.rodsml import SimpleXMLParser

rods2_1_generic = {
    'RODS_CONNECT': SimpleXMLParser,
    'RODS_VERSION': SimpleXMLParser,
}

rods2_1_binary_inp = {
    608: dataObjInp,
    615: dataObjInp,
    633: dataObjInp,
    606: dataObjInp,
    681: collInp,
    679: collInp,
    702: genQueryInp,
}

rods2_1_binary_out = {
    633: rodsObjStat,
    679: collOprStat,
    663: collOprStat,
    700: miscSvrInfo,
    702: genQueryOut,
}


def get_api_mapper(relVersion, apiVersion):
    if relVersion.startswith('rods2.0'):
        return rods20
    if relVersion.startswith('rods2.1'):
        return rods21


class rodsSafe(object):
    api = 0

    def connect(self, reconnFlag=0, connectCnt=0, proxy_user='',
                proxy_zone='', client_user='', client_zone='', option=''):
        connect_info = {'irodsProt': self.api,
                        'reconnFlag': reconnFlag,
                        'connectCnt': connectCnt,
                        'proxyUser': proxy_user,
                        'proxyRcatZone': proxy_zone,
                        'clientUser': client_user,
                        'clientRcatZone': client_zone,
                        'option': option}
        startup = connect.substitute(connect_info)
        return {'msg_type': 'RODS_CONNECT', 'data': startup}

    def RODS_VERSION(self):
        pass


class rods20(rodsSafe):
    def mkcoll(self, path):
        data = Container(collName=path,
                         flags=0,
                         oprType=0,
                         keyValPair=Container(len=0,
                                                keyWords=[],
                                                values=[]),)
        return {'int_info': api.COLL_CREATE_AN,
                'data': collInp.build(data)}

    def genQuery(self, *select, **where):
        """
        list the collections in a collection at path

        :param select: the columns to select from the iCAT.
        :type select: list of str
        :param where: keyword arguments the make up the where clause.
        :type where: str
        :rtype: :class:`~twisted.internet.defer.Deferred`
        """
        data = Container(keyValPair=Container(len=0,
                                              keyWords=[],
                                              values=[]),
                         continueInx=0,
                         inxIvalPair=Container(
                            len=0,
                            inx=[],
                            value=[]),
                         inxValPair=Container(
                            len=0,
                            inx=[],
                            value=[]),
                         maxRows=500, options=32, partialStartIndex=0)

        for s in select:
            data.inxIvalPair.len = data.inxIvalPair.len + 1
            data.inxIvalPair.inx.append(s)
            data.inxIvalPair.value.append(1)

        for k, v in where.items():
            data.inxValPair.len = data.inxValPair.len + 1
            data.inxValPair.inx.append(k)
            data.inxValPair.value.append(v)

        return {'int_info': api.GEN_QUERY_AN,
                'data': genQueryInp.build(data)}

    def rmcoll(self, path, recursive=False, **kwargs):
        data = Container(collName=path,
                         flags=0,
                         oprType=0,
                         keyValPair=Container(keyWords=[],
                                                len=0,
                                                values=[]))
        if recursive:
            data.keyValPair.len = data.keyValPair.len + 1
            data.keyValPair.keyWords.append('recursiveOp')
            data.keyValPair.values.append(1)
        for k, v in kwargs.items():
            data.keyValPair.len = data.keyValPair.len + 1
            data.keyValPair.keyWords.append(k)
            data.keyValPair.values.append(v)
        return {'int_info': api.RM_COLL_AN,
                'data': collInp.build(data)}

    def listObjects(self, path=''):
        """
        list the objects in a collection at path

        :param path: the location of the collection
        :type path: str
        :returns: a dictionary containing the int_info and the data
        :rtype: dict
        """
        return self.genQuery('COL_COLL_NAME',
                             'COL_DATA_NAME',
                             'COL_D_DATA_ID',
                             'COL_D_OWNER_NAME',
                             'COL_DATA_MODE',
                             'COL_DATA_SIZE',
                             'COL_D_MODIFY_TIME',
                             'COL_D_CREATE_TIME',
                             COL_COLL_NAME=" = '%s'" % path)


class rods21(rods20):
    def mkcoll(self, path):
        data = Container(collName=path,
                         flags=0,
                         oprType=0,
                         keyValPair=Container(len=0,
                                                keyWords=[],
                                                values=[]),)
        return {'int_info': api.COLL_CREATE_AN21,
                'data': collInp21.build(data)}

    def rmcoll(self, path, recursive=False, **kwargs):
        data = Container(collName=path,
                         flags=0,
                         oprType=0,
                         keyValPair=Container(keyWords=[],
                                                len=0,
                                                values=[]))
        if recursive:
            data.keyValPair.len = data.keyValPair.len + 1
            data.keyValPair.keyWords.append('recursiveOp')
            data.keyValPair.values.append(1)
        for k, v in kwargs.items():
            data.keyValPair.len = data.keyValPair.len + 1
            data.keyValPair.keyWords.append(k)
            data.keyValPair.values.append(v)
        return {'int_info': api.RM_COLL_AN21,
                'data': collInp21.build(data)}
