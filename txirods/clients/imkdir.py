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

from twisted.internet import reactor
from txirods.clients.base import IRODSClientController


class MkdirController(IRODSClientController):

    usage = """usage: %prog [options] DIRECTORY..."""

    def configure(self, opts, args):
        IRODSClientController.configure(self, opts, args)

        path = args[0]
        if rpath.isabs(path):
            self.path = path
        else:
            self.path = rpath.normpath(rpath.join(self.config.irodsCwd, path))

    def sendCommands(self, data):
        pwd = self.config.irodsCwd
        d = self.client.objStat(pwd)
        d.addCallbacks(self.sendMkdir, self.printStacktrace)
        return data

    def sendMkdir(self, data):
        d = self.client.mkcoll(self.path)
        d.addErrback(self.printStacktrace)
        return self.sendDisconnect(data)


def main(*args):
    controller = MkdirController(reactor)

    reactor.run()
    return
