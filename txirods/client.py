#############################################################################
#
# Copyright (c) 2009 Victorian Partnership for Advanced Computing Ltd and
# Contributors.
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


from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor, defer
from twisted.python import log
import sys

from protocol import IRODS

class Command(object):
    def __init__(self, command, *args, **kw):
        self.command = command
        self.args = args
        self.kw = kw
        self.deferred = defer.Deferred()

    def execute(self, irods):
        return self.command(*self.args, **self.kw)


class IRODSClient(IRODS):
    def connectionLost(self, *a):
        self.nextDeferred.callback('Connection closed by remote host.')



def parse_sqlResult(data):
    new_data = []
    for col in data.sqlResult:
        for r in range(data.rowCnt):
            if len(new_data) < data.rowCnt:
                new_data.append({})
            new_data[r][col.const] = col.value[r]
    return new_data

def success(response):
    if response is None:
        log.msg('Success!  Got response')
    else:
        log.msg('Success!  Got response\n' + str(response))


def print_st(error):
    log.err(error.printTraceback())
    # Gulp!
    return

from twisted.internet.protocol import ClientCreator

def main():

    def connectionFailed(f):
        print "Connection Failed:", f
        reactor.stop()

    def connectionMade(irodsClient):
        d = irodsClient.sendConnect(proxy_user='rods', proxy_zone='tempZone', client_zone='tempZone', client_user='rods')
        d.addCallbacks(success, print_st)

        d = irodsClient.send_auth_challenge('rods')
        d.addCallbacks(success, print_st)

        #d = irodsClient.sendApiReq(700)
        #d.addCallbacks(success, print_st)

        d = irodsClient.obj_stat('/tempZone/home/rods')
        d.addCallbacks(success, print_st)

        #d = irodsClient.list_objects('/tempZone/home/rods')
        #d.addCallbacks(success, print_st)

        #d = irodsClient.list_collections('/tempZone/home/rods')
        #d.addCallbacks(success, print_st)

        d = irodsClient.sendDisconnect()
        d.addCallbacks(success, print_st)
        d.addCallback(lambda result: reactor.stop())

    log.startLogging(sys.stdout)
    creator = ClientCreator(reactor, IRODSClient)
    creator.connectTCP('localhost', 1247).addCallback(connectionMade).addErrback(connectionFailed)
    reactor.run()
    return

