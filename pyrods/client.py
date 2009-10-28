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

from protocol import IRODS


class IRODSCommand(object):
    def __init__(self, command, *args, **kw):
        self.command = command
        self.args = args
        self.kw = kw
        self.deferred = defer.Deferred()

    def execute(self):
        return self.command(*self.args, **self.kw)


class IRODSAPICommand(IRODSCommand):
    def __init__(self, int_info, *args, **kw):
        self.int_info = int_info
        self.args = args
        self.kw = kw
        self.deferred = defer.Deferred()
        self.state = 0
        self.data = {}

    def execute(self, irods):
        return irods.sendMessage('RODS_API_REQ', int_info=self.int_info, *self.args, **self.kw)

    def __cmp__(self, y):
        return self.int_info.__cmp__(y)



class IRODSClient(IRODS):
    def __init__(self, reactor):
        IRODS.__init__(self)
        self.reactor = reactor
        self.actionQueue = []
        self._failed = 0
        self.command = None
        self.nextDeferred = None

    def connectionMade(self):
        IRODS.connectionMade(self)
        self.sendNextCommand()

    def sendNextInQueue(self, result):
        self.reactor.callLater(1, self.sendNextCommand)

    def sendNextCommand(self):
        #print "sendNextCommand " + str(self.actionQueue)
        if self.actionQueue:
            print "Command"
            command = self.actionQueue.pop(0)
        else:
            self.nextDeferred = None
            return
        self.command = command
        self.nextDeferred = command.deferred
        if isinstance(command, IRODSAPICommand):
            command.execute(self)
        else:
            self.nextDeferred.addCallback(self.sendNextInQueue)
            command.execute()

    def queueCommand(self, command):
        self.actionQueue.append(command)
        if (len(self.actionQueue) == 1 and self.transport is not None and self.nextDeferred is None):
            self.sendNextCommand()


class IRODSClientFactory(ClientFactory):
    protocol = IRODSClient

    def __init__(self, reactor, deferred=None):
        self.reactor = reactor
        self.deferred = deferred

    def buildProtocol(self, addr):
        p = self.protocol(self.reactor)
        if self.deferred:
            self.reactor.callLater(0, self.deferred.callback, p)
            del self.deferred
        p.factory = self
        return p

    def startedConnecting(self, connector):
        pass

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        reactor.stop()


def success(response):
    print 'Success!  Got response:'
    print '---'
    if response is None:
        print None
    else:
        print response
    print '---'


def fail(error):
    print 'Failed.  Error was:'
    print error


def connectionMade(irodsClient):
    c = IRODSCommand(irodsClient.sendConnect)
    c.deferred.addCallbacks(success, fail)
    irodsClient.queueCommand(c)
    c = IRODSAPICommand(711)
    c.deferred.addCallbacks(success, fail)
    irodsClient.queueCommand(c)
    c = IRODSAPICommand(711)
    c.deferred.addCallbacks(success, fail)
    irodsClient.queueCommand(c)
    c = IRODSCommand(irodsClient.obj_stat, '/ARCS/home/russell.sim')
    c.deferred.addCallbacks(success, fail)
    irodsClient.queueCommand(c)
    c = IRODSCommand(irodsClient.list_collections, '/ARCS/home/russell.sim')
    c.deferred.addCallbacks(success, fail)
    irodsClient.queueCommand(c)
    c = IRODSCommand(irodsClient.sendDisconnect)
    c.deferred.addCallbacks(success, fail)
    irodsClient.queueCommand(c)
    c = IRODSCommand(reactor.stop)
    irodsClient.queueCommand(c)


def main():
    d = defer.Deferred()
    d.addCallback(connectionMade)
    i = IRODSClientFactory(reactor, d)
    reactor.connectTCP('arcs-df.vpac.org', 1247, i)
    reactor.run()


