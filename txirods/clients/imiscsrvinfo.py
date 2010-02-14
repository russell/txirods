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

from datetime import datetime

class PwdController(IRODSClientController):

    usage = """usage: %prog [options]..."""

    def sendCommands(self, data):
        d = self.client.miscServerInfo()
        d.addCallbacks(self.printMiscServerInfo, self.printStacktrace)
        self.sendDisconnect(data)
        return data

    def printMiscServerInfo(self, data):
        if data.serverType:
            print "RCAT_ENABLED"
        else:
            print "RCAT_NOT_ENABLED"
        print "relVersion=%s" % data.relVersion
        print "apiVersion=%s" % data.apiVersion
        print "rodsZone=%s" % data.rodsZone
        td = datetime.now() - datetime.fromtimestamp(data.serverBootTime)
        print "up %s" % ':'.join(str(td).split(':')[:2])
        return data


def main(*args):
    controller = PwdController(reactor)

    reactor.run()
    return
