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
from os.path import join
from os.path import isabs
from os.path import normpath

import sys
from posixpath import join as rjoin
from posixpath import isabs as risabs
from posixpath import basename as rbasename
from posixpath import normpath as rnormpath

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
            if risabs(path):
                self.paths.append(path)
            else:
                self.paths.append(rnormpath(rjoin(self.config.irodsCwd, path)))

        if not self.paths:
            sys.exit(0)
        # TODO still need to handle the case where there is one argument and
        # it has the same name as a local file.

        # If the last path element is local it might be the dest
        if filepath.FilePath(args[-1]).exists():
            dest = self.paths.pop()
            if not isabs(dest):
                dest = normpath(join(os.getcwd(), dest))
            self.dest = dest
        else:
            self.dest = os.getcwd()

    @defer.inlineCallbacks
    def sendCommands(self, data):
        for path in self.paths:
            try:
                data = yield self.client.objStat(path)
            except:
                log.err()
            else:
                f = FileRecever(rnormpath(rjoin(self.dest, rbasename(path))))
                try:
                    yield self.client.get(f, path, data.objSize)
                except:
                    log.err()
        yield self.client.sendDisconnect()


def main(*args):
    GetController(reactor)
    reactor.run()
