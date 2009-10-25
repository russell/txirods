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
import struct
from sys import stdout
import messages
from xml.dom import minidom

class IRODS(Protocol):
    def __init__(self):
        self.num = 139
        self.msg_len = 0
        self.msg_type = ''
        self.api = 0

    def sendMessage(self, msg_type='', err_len=0, bs_len=0, int_info=0, data=''):
        num = struct.pack('!l', self.num)
        msg_len = len(data)
        header = messages.header.substitute({'type':msg_type, 'msg_len':msg_len, 'err_len':err_len, 'bs_len':bs_len, 'int_info':int_info})
        stdout.write("\n--------SEND\n" + str(self.num) + header + data)
        self.transport.write(num + header + data)

    def sendConnect(self, reconnFlag=0, connectCnt=0, proxy_user='', proxy_zone='', client_user='', client_zone='', option=''):
        stdout.write("\nsendConnect\n")
        startup = messages.connect.substitute({'irodsProt':self.api, 'reconnFlag': reconnFlag,
                                               'connectCnt': connectCnt, 'proxy_user':proxy_user,
                                               'proxy_zone': proxy_zone, 'client_user': client_user,
                                               'client_zone': client_zone, 'option': option})
        self.sendMessage('RODS_CONNECT',data=startup)

    def irods_rods_api_reply(self, data):
        #stdout.write(repr(data))
        server_info = {}
        d = struct.unpack('!iI', data[:8])
        server_info['serverType'] = d[0]
        server_info['serverBootTime'] = d[1]
        d = data[8:].split('\0')
        server_info['relVersion'] = d[0]
        server_info['apiVersion'] = d[1]
        server_info['rodsZone'] = d[2]
        stdout.write(str(server_info))
        self.nextDeferred.callback(server_info)

    def irods_rods_version(self, data):
        """
        <Version_PI>
        <status>0</status>
        <relVersion>rods2.1</relVersion>
        <apiVersion>d</apiVersion>
        <reconnPort>0</reconnPort>
        <reconnAddr></reconnAddr>
        <cookie>0</cookie>
        </Version_PI>
        """
        #stdout.write(data)
        self.nextDeferred.callback(data)

    def responseReceived(self):
        pass

    def dataReceived(self, data):
        stdout.write("\n--------RECIEVE\n" + repr(data))
        if self.msg_len < 1:
            self.num = struct.unpack('!l', data[:4])[0]
            data = data[4:]
            #stdout.write(data)

            if data.startswith('<MsgHeader_PI>'):
                eom = '</MsgHeader_PI>\n'
                seperator = data.index(eom) + len(eom)
                header = data[:seperator]
                data = data[seperator:]
                msg = minidom.parseString(header)
                msg_type = msg.getElementsByTagName('type')[0].childNodes[0].data
                msg_len = msg.getElementsByTagName('msgLen')[0].childNodes[0].data
                err_len = msg.getElementsByTagName('errorLen')[0].childNodes[0].data
                bs_len = msg.getElementsByTagName('bsLen')[0].childNodes[0].data
                intinfo = msg.getElementsByTagName('intInfo')[0].childNodes[0].data
                self.msg_len = int(msg_len)
                self.msg_type = msg_type

        self.msg_len = self.msg_len - len(data)

        if data:
            print 'Calling: irods_' + self.msg_type.lower()
            if hasattr(self, 'irods_' + self.msg_type.lower()):
                getattr(self, 'irods_' + self.msg_type.lower())(data)






