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
from posixpath import join as rjoin
from posixpath import isabs as risabs
from posixpath import normpath as rnormpath

from twisted.python import log, filepath
from twisted.internet import reactor, defer
from twisted.protocols import basic

from txirods.clients.base import IRODSClientController
from txirods import errors


class PutController(IRODSClientController):

    usage = """usage: %prog [options] SOURCE...
  or:  %prog [options] SOURCE... DIRECTORY
  or:  %prog [options] SOURCE DEST"""

    def configure(self, opts, args):
        IRODSClientController.configure(self, opts, args)

        self.paths = []
        for path in args:
            fp = filepath.FilePath(path)
            if fp.isdir():
                if not opts.recursive:
                    print "omitting directory `%s'" % path
                    continue
            self.paths.append(fp)

        if not self.paths:
            sys.exit(0)

        # If the last path element isn't local it might be remote
        if not self.paths[-1].exists():
            dest = self.paths.pop()
            if not risabs(dest):
                dest = rnormpath(rjoin(self.config.irodsCwd, dest))
            self.dest = dest
        else:
            self.dest = self.config.irodsCwd

    def parseArguments(self, optp):
        optp.add_option("-r", "--recursive", action='store_true',
                        help="copy directories recursively")
        IRODSClientController.parseArguments(self, optp)

    @defer.inlineCallbacks
    def sendCommands(self, data):
        try:
            data = yield self.client.objStat(self.dest)
        except errors.USER_FILE_DOES_NOT_EXIST:
            log.err()
            if len(self.paths) == 1:
                pass
            else:
                log.err()
        except:
            log.err()
            yield self.client.sendDisconnect()
            return

        if data.objType == 'DATA_OBJ_T':
            log.err("remote file %s already exists" % self.dest)
            yield self.client.sendDisconnect()
            return

        def copy(source, parent=''):
            if source.isdir():
                try:
                    yield self.client.mkcoll(rjoin(self.dest, parent,
                                                   source.basename()))
                except:
                    log.err()
                    return

                for child in source.children():
                    copy(child, rjoin(parent, source.basename()))
            else:
                try:
                    yield self.sendPut(source, rjoin(self.dest, parent,
                                                     source.basename()))
                except:
                    log.err()
                    return

        for source in self.paths:
            copy(source)

        yield self.client.sendDisconnect()

    def sendPut(self, localfile, remotepath):
        """
        Queue a put command

        :param localfile: the request that is to be processed
        :type :class:`~twisted.python.filepath.FilePath`:
        :param remotepath: the remote path to write the file to
        :type :str
        :rtype:class:`~twisted.internet.defer.Deferred`:
        """
        size = localfile.getsize()
        fp = localfile.open('rb')
        producer_cb = lambda x: basic.FileSender().beginFileTransfer(fp, self.client.transport)
        d = self.client.put(defer.Deferred().addCallback(producer_cb), remotepath, size)
        d.addBoth(self.cb_cleanUp, fp)
        d.addErrback(self.printStacktrace)
        return d

    def cb_cleanUp(self, data, fp):
        fp.close()
        return data


def main(*args):
    PutController(reactor)
    reactor.run()
