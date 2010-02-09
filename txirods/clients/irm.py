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

from os import path

from twisted.internet import reactor
from txirods.clients.base import IRODSClientController


class RmController(IRODSClientController):

    def configure(self, opts, args):
        IRODSClientController.configure(self, opts, args)
        pwd = self.config.irodsCwd
        self.rm_path = path.join(pwd, args[0])

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
        pwd = self.config.irodsCwd
        d = self.client.objStat(self.rm_path)
        d.addCallbacks(self.sendRm, self.printStacktrace)
        return data

    def sendRm(self, data):
        pwd = self.config.irodsCwd
        d = self.client.rmobj(self.rm_path)
        d.addErrback(self.printStacktrace)
        return self.sendDisconnect(data)


def main(*args):
    controller = RmController(reactor)

    reactor.run()
    return

