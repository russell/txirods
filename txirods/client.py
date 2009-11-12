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

class IRODSCommand(Command):
    def __init__(self, command, *args, **kw):
        self.command = command
        self.args = args
        self.kw = kw
        self.deferred = defer.Deferred()

    def execute(self, irods):
        return self.command(irods, *self.args, **self.kw)


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
    def __init__(self):
        IRODS.__init__(self)
        self.actionQueue = []
        self._failed = 0
        self.command = None
        self.nextDeferred = None

        cmd = IRODSCommand(IRODS.sendConnect)
        self.actionQueue.append(cmd)
        cmd.deferred.addCallbacks(success, print_st)

        cmd = IRODSAPICommand(711)
        self.actionQueue.append(cmd)
        cmd.deferred.addCallbacks(success, print_st)

        cmd = IRODSAPICommand(711)
        self.actionQueue.append(cmd)
        cmd.deferred.addCallbacks(success, print_st)

    def connectionMade(self):
        self.sendNextCommand()

        IRODS.connectionMade(self)

    def sendNextInQueue(self, result):
        reactor.callLater(0, self.sendNextCommand)
        return result

    def sendNextCommand(self):
        #print "sendNextCommand " + str(self.actionQueue)
        if self.actionQueue:
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
            command.execute(self)

    def queueAPICommand(self, int_info):
        cmd = IRODSAPICommand(int_info)

        self.queueCommand(cmd)
        return cmd.deferred

    def queueIRODSCommand(self, command, *args, **kwargs):
        cmd = IRODSCommand(command, *args, **kwargs)

        self.queueCommand(cmd)
        return cmd.deferred


    def queueCommand(self, cmd):
        self.actionQueue.append(cmd)
        if (len(self.actionQueue) == 1 and self.transport is not None and self.nextDeferred is None):
            self.sendNextCommand()


class IRODSClientFactory(ClientFactory):
    protocol = IRODSClient

    def __init__(self, command):
        self.command = command

    def buildProtocol(self, addr):
        p = self.protocol()
        p.factory = self
        if isinstance(self.command, list):
            for c in self.command:
                p.queueCommand(c)
        else:
            p.queueCommand(self.command)
        return p

    def startedConnecting(self, connector):
        pass

    def clientConnectionLost(self, connector, reason):
        log.msg('Lost connection')
        reason.printTraceback()

    def clientConnectionFailed(self, connector, reason):
        log.err('Connection failed')
        reason.printTraceback()
        reactor.stop()


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
    # Should close connection cleanly
    try:
        reactor.stop()
    except:
        pass


def main():
    cmds = []
    cmd = IRODSCommand(IRODS.obj_stat, '/ARCS/home')
    cmd.deferred.addCallbacks(success, print_st)
    cmds.append(cmd)
    cmd = IRODSCommand(IRODS.list_objects, '/ARCS/home/russell.sim')
    cmd.deferred.addCallbacks(parse_sqlResult, print_st)
    cmd.deferred.addCallbacks(success, print_st)
    cmds.append(cmd)
    cmd = IRODSCommand(IRODS.list_collections, '/ARCS/home')
    cmd.deferred.addCallbacks(parse_sqlResult, print_st)
    cmd.deferred.addCallbacks(success, print_st)
    cmds.append(cmd)
    cmd = IRODSCommand(IRODS.sendDisconnect)
    cmd.deferred.addCallbacks(success, print_st)
    cmds.append(cmd)

    # XXX had to remove connector? no idea why
    def clientConnectionLost(self, reason):
        log.msg('Lost connection')
        reason.printTraceback()
        reactor.stop()

    i = IRODSClientFactory(cmds)
    i.clientConnectionLost = clientConnectionLost
    log.startLogging(sys.stdout)
    reactor.connectTCP('arcs-df.vpac.org', 1247, i)
    reactor.run()


