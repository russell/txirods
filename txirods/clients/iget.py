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

import os
from os import path

from twisted.internet import reactor, defer

from txirods.clients.base import IRODSClientController
from txirods.protocol import FileRecever


class GetController(IRODSClientController):

    def configure(self, opts, args):
        IRODSClientController.configure(self, opts, args)
        pwd = self.config.irodsCwd
        self.localfile = path.join(os.getcwd(), args[0])
        self.remotefile = path.join(pwd, args[0])

    def connectClient(self, client):
        IRODSClientController.connectClient(self, client)
        self.sendConnect()

    def sendConnect(self):
        user = self.config.irodsUserName
        zone = self.config.irodsZone
        d = self.client.sendConnect(proxy_user=user, proxy_zone=zone,
                                    client_zone=zone, client_user=user)
        d.addCallbacks(self.sendAuth, self.printStacktrace)
        d.addErrback(self.sendDisconnect)

    def sendAuth(self, data):
        d = self.client.sendAuthChallenge(self.credentials.password)
        d.addCallbacks(self.sendStat, self.sendDisconnect)

    def sendStat(self, data):
        d = self.client.objStat(self.remotefile)
        d.addCallbacks(self.sendGet, self.printStacktrace)
        d.addErrback(self.sendDisconnect)
        return data

    def sendGet(self, data):
        f = FileRecever(self.localfile)
        d = self.client.get(f, self.remotefile, data.objSize)
        d.addErrback(self.printStacktrace)
        self.sendDisconnect(data)
        return data


def main(*args):
    controller = GetController(reactor)

    reactor.run()
    return
