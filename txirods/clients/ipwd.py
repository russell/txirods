import sys
import logging

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
    log.err(error)
    # Gulp!
    return None


def main():
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

    log_level = logging.WARNING # default
    if opts.verbose == 1:
        log_level = logging.INFO
    elif opts.verbose >= 2:
        log_level = logging.DEBUG
        log.startLogging(sys.stdout)

    # Set up basic configuration, out to stderr with a reasonable default format.
    logging.basicConfig(level=log_level)

    def success(response):
        print pwd

    def connectionFailed(f):
        print "Connection Failed:", f
        reactor.stop()

    def connectionMade(irodsClient):
        d = irodsClient.sendConnect(proxy_user='rods', proxy_zone='tempZone', client_zone='tempZone', client_user='rods')
        d.addErrback(print_st)

        d = irodsClient.sendAuthChallenge('rods')
        d.addErrback(print_st)

        d = irodsClient.objStat(pwd)
        d.addCallbacks(success, print_st)

        d = irodsClient.sendDisconnect()
        d.addCallback(lambda result: reactor.stop())

    creator = ClientCreator(reactor, IRODSClient)
    creator.connectTCP('localhost', 1247).addCallback(connectionMade).addErrback(connectionFailed)
    reactor.run()
    return

