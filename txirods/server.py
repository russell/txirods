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

import struct
import random
from md5 import md5

from twisted.internet.protocol import Factory
from twisted.python import log, failure

from txirods.protocol import IRODSChannel
from txirods import api
from txirods.encoding import rodsml

from txirods.encoding import rods2_1_binary_inp, rods2_1_generic, \
                        rods2_1_binary_out


class IRODSBaseServer(IRODSChannel):
    def __init__(self):
        IRODSChannel.__init__(self)
        self.api_reponse_map = rods2_1_binary_out
        self.api_request_map = rods2_1_binary_inp
        self.generic_reponse_map = rods2_1_generic

    def processMessage(self, data):
        """
        irods message processing
        """
        log.msg("\nPROCESSMESSAGE\n", debug=True)
        if self.response.msg_type in self.generic_reponse_map:
            try:
                data = self.generic_reponse_map[self.response.msg_type](data)
            except:
                self.nextDeferred.errback(failure.Failure())
            else:
                if hasattr(self, 'msg_' + self.response.msg_type.lower()):
                    return getattr(self, 'msg_' + self.response.msg_type.lower())(data)
                else:
                    raise Exception("WTF")

        if hasattr(self, 'msg_' + self.response.msg_type.lower() + '_' + str(self.response.int_info)):
            return getattr(self, 'msg_' + self.response.msg_type.lower() + '_' + str(self.response.int_info))(data)
        else:
            raise Exception("WTF Message Erro")

        if self.int_info == api.AUTH_REQUEST_AN:
            self.handleAuthChallange(data)
            return
        print data
        self.sendMessage('RODS_API_REPLY')


    def processOther(self, data):
        log.msg("\nPROCESSOTHER\n", debug=True)

        # handle empty reponse messages
        print self.response.int_info
        if self.response.int_info in [api.AUTH_REQUEST_AN,]:
            if hasattr(self, 'msg_' + self.response.msg_type.lower() + '_' + str(self.response.int_info)):
                return getattr(self, 'msg_' + self.response.msg_type.lower() + '_' + str(self.response.int_info))(data)
            else:
                raise Exception("WTF Other Error")


    def msg_rods_api_req(self, data):
        if self.response.int_info in self.api_reponse_map:
            try:
                data = self.api_reponse_map[self.int_info].parse(data)
            except:
                self.nextDeferred.errback(failure.Failure())
            else:
                print data
                #self.nextDeferred.callback(data)
            return

    def msg_rods_api_req_703(self, data):
        self.challange = ''.join([struct.pack('!f', random.random()) for i in range(16)])
        self.sendMessage('RODS_API_REPLY', data=self.challange)
        return


    def msg_rods_api_req_704(self, data):
        log.msg("\nChallenge response\n" + repr(data), debug=True)
        MAX_PASSWORD_LEN = 50
        CHALLENGE_LEN = 64
        resp_len = CHALLENGE_LEN + MAX_PASSWORD_LEN

        resp = self.challange + 'rods'

        # response is padded with binary nulls
        resp = resp + '\0' * (resp_len - len(resp))
        resp = md5(resp).digest()

        # replace and 0 with 1
        resp = resp.replace('\0', '\x01')

        userandzone = self.connect_info['proxyUser'] + '#' \
                + self.connect_info['proxyRcatZone']

        # pad message with 0
        if resp + str(userandzone) + '\0' == str(data):
            self.sendMessage(msg_type='RODS_API_REPLY')
            return

        # else fail the auth
        self.sendMessage(msg_type='RODS_API_REQ',
                         int_info=api.AUTH_RESPONSE_AN,
                         data=resp + userandzone + '\0')


    def msg_rods_connect(self, data):
        """
        {u'proxyRcatZone': u'tempZone', u'option': '', u'relVersion': u'rods2.1', u'proxyUser': u'rods', u'irodsProt': 0, u'connectCnt': 0, u'apiVersion': u'd', u'reconnFlag': 0, u'clientUser': u'rods', u'clientRcatZone': u'tempZone'}
        """
        self.connect_info = data
        response_data = {'status': 0, 'relVersion':'rods2.1',
                         'apiVersion': 'd', 'reconnPort':0,
                         'reconnAddr': '', 'cookie': 0}
        response_data = rodsml.version_pi.substitute(response_data)
        self.sendMessage('RODS_VERSION', data=response_data)

class IRODSServerFactory(Factory):

    protocol = IRODSBaseServer

    def __init__(self):
        self.test = "yes it works"

