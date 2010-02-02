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
import time
from os import path

from twisted.python import log
from txirods.client import IRODSClient
from txirods.config import ConfigParser, AuthParser
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator


def print_st(error):
    No_Results = -808000
    if error.value.errorNumber == -808000:
        # SQL No Results
        return None
    return error


def parse_sqlResult(data):
    if not data: return {}
    new_data = []
    for col in data.sqlResult:
        for r in range(data.rowCnt):
            if len(new_data) < data.rowCnt:
                new_data.append({})
            new_data[r][col.const] = col.value[r]
    return new_data


class PrettyPrinter(object):
    def __init__(self):
        self.lens = {'TYPE': 1, 'NAME': 0,
                     'OWNER': 0, 'MODIFIED': 0,
                     'MODE': 0, 'SIZE': 0}
        self.data = []

    def coll_table(self, data):
        if not data:
            return
        coll_map = {'COL_COLL_NAME': 'NAME',
                   'COL_COLL_MODIFY_TIME': 'MODIFIED',
                   'COL_COLL_OWNER_NAME': 'OWNER',
                  }
        for row in data:
            coll = {'TYPE': 'c', 'SIZE': '0'}
            for k, v in row.items():
                if coll_map.has_key(k):
                    k = coll_map[k]
                    coll[k] = v
                    if k == 'NAME':
                        coll[k] = path.basename(v)
                    l = len(v)
                    if l > self.lens[k]:
                        self.lens[k] = l
            self.data.append(coll)
        return data

    def obj_table(self, data):
        if not data:
            return
        obj_map = {'COL_DATA_NAME': 'NAME',
                   'COL_D_MODIFY_TIME': 'MODIFIED',
                   'COL_DATA_SIZE': 'SIZE',
                   'COL_D_OWNER_NAME': 'OWNER',
                   'COL_DATA_MODE': 'MODE',
                  }
        for row in data:
            obj = {'TYPE': ''}
            for k, v in row.items():
                if obj_map.has_key(k):
                    k = obj_map[k]
                    obj[k] = v
                    l = len(v)
                    if l > self.lens[k]:
                        self.lens[k] = l
            self.data.append(obj)
        return data

    def prettyprint(self, data):
        lens = self.lens
        data = self.data
        for row in data:
            print row['TYPE'].ljust(lens['TYPE']),
            print row['OWNER'].ljust(lens['OWNER']),
            print row['SIZE'].ljust(lens['SIZE']),
            print time.strftime('%Y-%m-%d %H:%M',
                                time.localtime(float(row['MODIFIED']))),
            print row['NAME'].ljust(lens['NAME'])
        return

def main(*args):
    # Late import, in case this project becomes a library, never to be run as main again.
    import optparse

    # Populate our options, -h/--help is already there for you.
    optp = optparse.OptionParser()
    optp.add_option('-v', '--verbose', dest='verbose', action='count',
                    help="Increase verbosity (specify multiple times for more)")
    optp.add_option("-V", "--version", action='store_true',
                    help="print version number and exit")
    # Parse the arguments (defaults to parsing sys.argv).
    opts, args = optp.parse_args()

    # Here would be a good place to check what came in on the command line and
    # call optp.error("Useful message") to exit if all it not well.
    c = ConfigParser()
    c.read()
    pwd = c.irodsCwd
    user = c.irodsUserName
    zone = c.irodsZone

    a = AuthParser()
    a.read()

    log_level = logging.WARNING # default
    if opts.verbose == 1:
        log_level = logging.INFO
    elif opts.verbose >= 2:
        log_level = logging.DEBUG
        log.startLogging(sys.stdout)

    # Set up basic configuration, out to stderr with a reasonable default format.
    logging.basicConfig(level=log_level)

    def connectionFailed(f):
        print "Connection Failed:", f
        reactor.stop()

    def connectionMade(irodsClient):
        d = irodsClient.sendConnect(proxy_user=user, proxy_zone=zone, client_zone=zone, client_user=user)
        d.addErrback(print_st)

        def successfullyAuthed(data):
            d = irodsClient.objStat(pwd)
            d.addCallbacks(exists, print_st)
            d.addErrback(disconnect)
            return data

        def exists(data):
            printer = PrettyPrinter()
            d = irodsClient.listCollections(pwd)
            d.addErrback(print_st)
            d.addCallback(parse_sqlResult)
            d.addCallback(printer.coll_table)

            d = irodsClient.listObjects(pwd)
            d.addErrback(print_st)
            d.addCallback(parse_sqlResult)
            d.addCallback(printer.obj_table)
            d.addCallback(printer.prettyprint)

            disconnect(data)

        def disconnect(data):
            d = irodsClient.sendDisconnect()
            d.addCallback(lambda result: reactor.stop())
            return data

        d = irodsClient.sendAuthChallenge(a.password)
        d.addCallbacks(successfullyAuthed, disconnect)

    creator = ClientCreator(reactor, IRODSClient)
    creator.connectTCP('localhost', 1247).addCallback(connectionMade).addErrback(connectionFailed)
    reactor.run()
    return


