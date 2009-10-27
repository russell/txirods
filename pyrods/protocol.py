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
from pyGlobus.security import GSSCred, GSSContext, GSSContextException
from pyGlobus.security import GSSName, GSSMechs, GSSUsage
from pyGlobus.security import ContextRequests
from pyGlobus import gssc

class IRODS(Protocol):
    def __init__(self):
        self.num = 139
        self.msg_len = 0
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
        if self.command == 700:
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
        if self.command == 711:
            if self.command.data.has_key('stage') and self.command.data['stage'] == 1:
                context = self.command.data['context']
                init_cred=self.command.data['cred']
                target_name=self.command.data['targetName']
                requests=self.command.data['requests']
                major,minor,outToken = context.init_context(init_cred=init_cred,
                                                            target_name=target_name,
                                                            inputTokenString=data,
                                                            requests=requests)
                print "part 2 %s %s" % (str(major), str(minor))
                self.command.data['stage'] += 1
                self.data = ''
                self.transport.write(outToken)
                return
            elif self.command.data.has_key('stage') and self.command.data['stage'] == 2:
                context = self.command.data['context']
                init_cred=self.command.data['cred']
                target_name=self.command.data['targetName']
                requests=self.command.data['requests']
                major,minor,outToken = context.init_context(init_cred=init_cred,
                                                            target_name=target_name,
                                                            inputTokenString=data,
                                                            requests=requests)
                print "part 2 %s %s" % (str(major), str(minor))
                self.command.data['stage'] += 1
                self.data = ''
                self.transport.write(outToken)
                self.num = 139
                self.nextDeferred.callback(data)
                return
            else:
                server_dn = data.split('\0')[0]
                print server_dn
                self.command.data['server_dn'] = server_dn
                # create credential
                cred = GSSCred()
                name, mechs, usage  = GSSName(), GSSMechs(), GSSUsage()
                #usage.set_usage_initiate()
                cred.acquire_cred(name, mechs, usage)

                lifetime, credName = cred.inquire_cred()
                context = GSSContext()
                requests = ContextRequests()

                targetName = GSSName()
                major, minor, targetName_handle = gssc.import_name('arcs-df.vpac.org', gssc.cvar.GSS_C_NT_HOSTBASED_SERVICE)
                targetName._handle = targetName_handle

                #requests.set_delegation()
                requests.set_mutual()
                requests.set_replay()

                major,minor,outToken = context.init_context(init_cred=cred,
                                                            target_name=targetName,
                                                            inputTokenString='',
                                                            requests=requests)

                self.command.data.update({'name':name, 'lifetime':lifetime, 'credName':credName,
                                          'targetName':targetName, 'todelete':name,
                                          'context':context, 'requests':requests, 'cred': cred})

                print "part one %s %s" % (str(major), str(minor))
                print repr(context.inquire())
                self.command.data['stage'] = 1
                self.msg_len = 10000000000000
                self.transport.write(outToken)
                return
            #self.nextDeferred.callback(server_dn)

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
        #stdout.write("\n--------RECIEVE\n" + repr(data))
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

        if self.command == 711 and self.command.data.has_key('stage'):
            if hasattr(self, 'data') and self.command.data.has_key('length'):
                print "add to buffer"
                self.data = self.data + data
            if not self.command.data.has_key('length'):
                print "init"
                self.command.data['length'] = struct.unpack('!L', data[:4])[0]
                self.data = data
                return
            data = self.data
        if data:
            print 'Calling: irods_' + self.msg_type.lower()
            if hasattr(self, 'irods_' + self.msg_type.lower()):
                getattr(self, 'irods_' + self.msg_type.lower())(data)






