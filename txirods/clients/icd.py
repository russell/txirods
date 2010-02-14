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

import posixpath as rpath
from getpass import getpass

from twisted.python import log
from twisted.internet import reactor

from txirods.clients.base import IRODSClientController
from twisted.internet import reactor, defer


class CdController(IRODSClientController):

    def configure(self, opts, args):
        IRODSClientController.configure(self, opts, args)

        if args:
            path = args[0]
        else:
            path = self.config.irodsHome

        if rpath.isabs(path):
            self.path = path
        else:
            self.path = rpath.normpath(rpath.join(self.config.irodsCwd, path))

    def sendCommands(self, data):
        d = self.client.objStat(self.path)
        d.addCallbacks(self.saveCwd, self.printCwd)
        d.addErrback(self.printStacktrace)
        d.addErrback(self.sendDisconnect)
        return data

    def saveCwd(self, data):
        self.config.irodsCwd = self.path
        self.config.write()
        self.sendDisconnect(data)
        return data

    def printCwd(self, data):
        print self.path
        return data

def main(*args):
    controller = CdController(reactor)

    reactor.run()
    return
