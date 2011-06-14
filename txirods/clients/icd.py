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

from twisted.python import log
from twisted.internet import reactor, defer

from txirods.clients.base import IRODSClientController
from txirods import errors


class CdController(IRODSClientController):

    usage = """usage: %prog [options] FILE..."""

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

    @defer.inlineCallbacks
    def sendCommands(self, data):
        try:
            yield self.client.objStat(self.path)
        except errors.USER_FILE_DOES_NOT_EXIST:
            log.err()
        else:
            print self.path
            self.config.irodsCwd = self.path
            self.config.write()
        yield self.sendDisconnect(data)


def main(*args):
    CdController(reactor)
    reactor.run()
