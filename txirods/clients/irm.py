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

import sys
import posixpath as rpath

from twisted.python import log, failure
from twisted.internet import reactor
from txirods.clients.base import IRODSClientController


class RmController(IRODSClientController):

    usage = """usage: %prog [options] FILE..."""

    def configure(self, opts, args):
        IRODSClientController.configure(self, opts, args)
        pwd = self.config.irodsCwd

        self.paths = []
        for path in args:
            if rpath.isabs(path):
                self.paths.append(path)
            else:
                self.paths.append(rpath.normpath(rpath.join(self.config.irodsCwd, path)))

        if not self.paths:
            sys.exit(0)

        self.flags = dict.fromkeys(opts.flags, '')

    def parseArguments(self, optp):
        optp.add_option("-r", "--recursive", action='append_const', const='recursiveOpr',
                        dest="flags", default=[], help="copy directories recursively")
        optp.add_option("-f", "--force", action='append_const', const='forceFlag',
                        dest="flags", default=[], help="force deletion of files, skipping trash")
        IRODSClientController.parseArguments(self, optp)

    def sendCommands(self, data):
        pwd = self.config.irodsCwd
        for path in self.paths:
            d = self.client.objStat(path)
            d.addErrback(self.sendDisconnect)
            d.addCallback(self.cb_checkRemotePath, path)
            d.addErrback(self.printStacktrace)
        return data

    def cb_checkRemotePath(self, data, path):
        if data.objType == 'DATA_OBJ_T':
            d = self.sendRm(path)
            return data
        if data.objType == 'COLL_OBJ_T':
            if not 'recursiveOpr' in self.flags:
                if self.paths[-1] == path:
                    self.sendDisconnect(data)
                return failure.Failure(Exception("cannot remove `%s': Is a directory" % path))
            else:
                self.sendRmDir(path)
                return data
        if self.paths[-1] == path:
            self.sendDisconnect(data)
        return failure.Failure(Exception("remote path exists, but not sure what it is"))

    def sendRmDir(self, path):
        d = self.client.rmcoll(path, **self.flags)
        if self.paths[-1] == path:
            d.addBoth(self.sendDisconnect)
        d.addErrback(self.printStacktrace)
        return d

    def sendRm(self, path):
        d = self.client.rmobj(path, **self.flags)
        if self.paths[-1] == path:
            d.addBoth(self.sendDisconnect)
        d.addErrback(self.printStacktrace)
        return d


def main(*args):
    controller = RmController(reactor)

    reactor.run()
    return
