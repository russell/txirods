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
import warnings
warnings.filterwarnings("ignore")

from twisted.python import log
from twisted.internet import reactor, defer

from txirods.clients.base import IRODSClientController


class PwdController(IRODSClientController):

    usage = """usage: %prog [options]..."""

    @defer.inlineCallbacks
    def sendCommands(self, data):
        pwd = self.config.irodsCwd
        try:
            yield self.client.objStat(pwd)
        except:
            log.err()
        else:
            print pwd
        yield self.client.sendDisconnect(data)


def main(*args):
    PwdController(reactor)
    reactor.run()
