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
import optparse

from twisted.python import log
from txirods.client import IRODSClientFactory
from txirods.config import ConfigParser, AuthParser
from twisted.internet import reactor, defer
from twisted.internet import error


def main(*args):
    class IRODSClientController(object):

        factory = IRODSClientFactory

        def __init__(self, reactor):
            self.reactor = reactor
            self.client = None

            optp = optparse.OptionParser()
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
            # Here would be a good place to check what came in on the command line and
            # call optp.error("Useful message") to exit if all it not well.
            log_level = logging.WARNING # default
            if opts.verbose == 1:
                log_level = logging.INFO
            elif opts.verbose >= 2:
                log_level = logging.DEBUG
                log.startLogging(sys.stdout)

            # Set up basic configuration, out to stderr with a reasonable default format.
            logging.basicConfig(level=log_level)


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

        def print_data(self, data):
            pwd = self.config.irodsCwd
            print pwd
            return data

        def printStacktrace(self, error):
            No_Results = -808000
            if error.value.errorNumber == -808000:
                # SQL No Results
                return None
            return error

        def sendConnect(self):
            user = self.config.irodsUserName
            zone = self.config.irodsZone
            d = self.client.sendConnect(proxy_user=user, proxy_zone=zone,
                                        client_zone=zone, client_user=user)
            d.addCallbacks(self.sendAuth, self.printStacktrace)
            d.addErrback(self.sendDisconnect)

        def sendAuth(self, data):
            d = self.client.sendAuthChallenge(self.credentials.password)
            d.addCallbacks(self.sendPwd, self.sendDisconnect)

        def sendPwd(self, data):
            pwd = self.config.irodsCwd
            d = self.client.objStat(pwd)
            d.addCallbacks(self.print_data, self.printStacktrace)
            self.sendDisconnect(data)
            return data

        def sendDisconnect(self, data):
            d = self.client.sendDisconnect()
            return data

        def connectionLost(self, reason):
            reason.trap(error.ConnectionDone)
            if not reason:
                print "Connection Lost:", reason
            reactor.stop()

        def connectionFailed(self, reason):
            print "Connection Failed:", reason
            reactor.stop()

    controller = IRODSClientController(reactor)

    reactor.run()
    return

