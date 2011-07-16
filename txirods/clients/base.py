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
import logging

from twisted.python import log
from twisted.internet import defer, error

from txirods import errors
from txirods.client import IRODSClientFactory
from txirods.config import ConfigParser, AuthParser


class IRODSLogger(log.DefaultObserver):
    stdout = sys.stdout

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = "\033[1m"
    ENDC = '\033[0m'

    def __init__(self, level):
        self.level = level

    def disableColors(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.BOLD = ''
        self.ENDC = ''

    def emit(self, eventDict):

        if eventDict.get("printed", False):
            text = " ".join([str(m) for m in eventDict["message"]]) + "\n"
            self.stdout.write(text)
            self.stdout.flush()
            return

        if self.level != logging.DEBUG and eventDict.get("debug", False):
            return

        if eventDict["isError"]:
            if 'failure' in eventDict:
                text = ((eventDict.get('why') or 'Unhandled Error')
                        + '\n' + eventDict['failure'].getTraceback())
            else:
                text = " ".join([str(m) for m in eventDict["message"]]) + "\n"
            self.stderr.write(self.FAIL + text + self.ENDC)
            self.stderr.flush()
        else:
            text = " ".join([str(m) for m in eventDict["message"]]) + "\n"

        if self.level == logging.DEBUG and eventDict.get("debug", False):
            self.stderr.write(self.HEADER + text + self.ENDC)
            self.stderr.flush()
            return

        if self.level <= logging.INFO:
            self.stderr.write(self.OKGREEN + text + self.ENDC)
            self.stderr.flush()

    def start(self):
        log.addObserver(self.emit)


class IRODSClientController(object):

    factory = IRODSClientFactory
    usage = "usage: %prog [options]"

    def __init__(self, reactor):
        self.reactor = reactor
        self.client = None

        import optparse
        optp = optparse.OptionParser(self.usage)
        # Parse the arguments (defaults to parsing sys.argv).
        self.parseArguments(optp)
        opts, args = optp.parse_args()

        self.parseConfig()

        self.configure(opts, args)
        self.connectTCP()

    def parseArguments(self, optp):
        optp.add_option('-v', '--verbose', dest='verbose', action='count',
                        help="Increase verbosity (specify multiple times for more)")
        optp.add_option("-V", "--version", action='store_true',
                        help="print version number and exit")

    def parseConfig(self):
        self.config = ConfigParser()
        self.config.read()

        self.credentials = AuthParser()
        self.credentials.read()

    def configure(self, opts, args):
        # Here would be a good place to check what came in on the command line
        # and call optp.error("Useful message") to exit if all it not well.
        log_level = logging.WARNING  # default
        if opts.verbose == 1:
            log_level = logging.INFO
        elif opts.verbose >= 2:
            log_level = logging.DEBUG
            #log.startLogging(sys.stdout)

        # Set up basic configuration, out to stderr with a
        # reasonable default format.
        observer = IRODSLogger(log_level)
        log.startLoggingWithObserver(observer.emit)

    def connectTCP(self):
        cb_connect = defer.Deferred()
        cb_connect.addCallbacks(self.connectClient, self.connectionFailed)

        cb_connection_lost = defer.Deferred()
        cb_connection_lost.addBoth(self.connectionLost)

        factory = self.factory(cb_connect, cb_connection_lost)

        host = self.config.irodsHost
        port = self.config.irodsPort
        self.reactor.connectTCP(host, port, factory)

    def connectClient(self, client):
        self.client = client
        self.sendConnect()

    def sendConnect(self):
        user = self.config.irodsUserName
        zone = self.config.irodsZone
        d = self.client.sendConnect(proxy_user=user, proxy_zone=zone,
                                    client_zone=zone, client_user=user)
        d.addCallbacks(self.sendAuth, self.printStacktrace)
        d.addErrback(self.sendDisconnect)

    def sendAuth(self, data):
        d = self.client.sendAuthChallenge(self.credentials.password)
        d.addCallbacks(self.sendCommands, self.sendDisconnect)

    def sendCommands(self, data):
        self.sendDisconnect()

    def parseSqlResult(self, data):
        if not data:
            return {}
        new_data = []
        for col in data.sqlResult:
            for r in range(data.rowCnt):
                if len(new_data) < data.rowCnt:
                    new_data.append({})
                new_data[r][col.const] = col.value[r]
        return new_data

    def printStacktrace(self, failure):
        failure.trap(errors.CAT_NO_ROWS_FOUND)
        return None

    def sendDisconnect(self, data):
        self.client.sendDisconnect()
        return data

    def connectionLost(self, reason):
        reason.trap(error.ConnectionDone)
        if not reason:
            print "Connection Lost:", reason
        self.reactor.stop()

    def connectionFailed(self, reason):
        print "Connection Failed:", reason
        self.reactor.stop()
