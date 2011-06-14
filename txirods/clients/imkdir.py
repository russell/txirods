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
from twisted.internet import defer
from twisted.internet import reactor

from txirods import errors
from txirods.clients.base import IRODSClientController


class MkdirController(IRODSClientController):

    usage = """usage: %prog [options] DIRECTORY..."""

    def configure(self, opts, args):
        IRODSClientController.configure(self, opts, args)

        self.paths = []
        for path in args:
            if rpath.isabs(path):
                self.paths.append(path)
            else:
                self.paths.append(rpath.normpath(
                    rpath.join(self.config.irodsCwd, path)))

    @defer.inlineCallbacks
    def sendCommands(self, data):
        pwd = self.config.irodsCwd
        try:
            yield self.client.objStat(pwd)
        except errors.USER_FILE_DOES_NOT_EXIST:
            log.err()
            log.err("The current working directory doesn't exist.")
            yield self.client.sendDisconnect()
            return

        for path in self.paths:
            try:
                yield self.client.mkcoll(path)
            except errors.CATALOG_ALREADY_HAS_ITEM_BY_THAT_NAME:
                log.err()
            except:
                log.err()
        yield self.client.sendDisconnect()


def main(*args):
    MkdirController(reactor)
    reactor.run()
