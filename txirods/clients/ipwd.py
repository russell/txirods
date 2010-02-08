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

from txirods.clients.base import IRODSClientController
from twisted.internet import reactor, defer

class PwdController(IRODSClientController):

    def connectClient(self, client):
        self.client = client
        self.sendConnect()

    def printResult(self, data):
        pwd = self.config.irodsCwd
        print pwd
        return data

    def sendConnect(self):
        user = self.config.irodsUserName
        zone = self.config.irodsZone
        d = self.client.sendConnect(proxy_user=user, proxy_zone=zone,
                                    client_zone=zone, client_user=user)
        d.addCallbacks(self.sendAuth, self.printStacktrace)
        d.addErrback(self.sendDisconnect)

    def sendAuth(self, data):
        d = self.client.sendAuthChallenge(self.credentials.password)
        d.addCallbacks(self.sendPwd, self.sendDisconnect)

    def sendPwd(self, data):
        pwd = self.config.irodsCwd
        d = self.client.objStat(pwd)
        d.addCallbacks(self.printResult, self.printStacktrace)
        self.sendDisconnect(data)
        return data


def main(*args):
    controller = IRODSClientController(reactor)

    reactor.run()
    return

