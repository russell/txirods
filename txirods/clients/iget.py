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
import os.path
import sys
import posixpath as rpath

from twisted.python import log, filepath
from twisted.internet import reactor, defer

from txirods.clients.base import IRODSClientController
from txirods.protocol import FileRecever


class GetController(IRODSClientController):

    usage = """usage: %prog [options] SOURCE...
  or:  %prog [options] SOURCE... DIRECTORY
  or:  %prog [options] SOURCE DEST"""

    def configure(self, opts, args):
        IRODSClientController.configure(self, opts, args)

        self.paths = []
        for path in args:
            if rpath.isabs(path):
                self.paths.append(path)
            else:
                self.paths.append(rpath.normpath(rpath.join(self.config.irodsCwd, path)))

        if not self.paths:
            sys.exit(0)
        # TODO still need to handle the case where there is one argument and
        # it has the same name as a local file.

        # If the last path element is local it might be the dest
        if filepath.FilePath(args[-1]).exists():
            self.paths.pop()
            dest = args[-1]
            if not rpath.isabs(dest):
                dest = rpath.normpath(rpath.join(os.getcwd(), dest))
            self.dest = dest
        else:
            self.dest = os.getcwd()

    def sendCommands(self, data):
        for path in self.paths:
            self.sendGet(path)

    def sendGet(self, path):
        d = self.client.objStat(path)
        d.addCallbacks(self.cb_get, self.printStacktrace, [path])
        if path == self.paths[-1]:
            d.addErrback(self.sendDisconnect)
        return d

    def cb_get(self, data, path):
        f = FileRecever(os.path.normpath(os.path.join(self.dest, rpath.basename(path))))
        d = self.client.get(f, path, data.objSize)
        d.addErrback(self.printStacktrace)
        if self.paths[-1] == path:
            d.addBoth(self.sendDisconnect)
        return data


def main(*args):
    controller = GetController(reactor)

    reactor.run()
    return
