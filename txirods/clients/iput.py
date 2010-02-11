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
import posixpath as rpath

from twisted.python import log, filepath, failure
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
            self.paths.pop()
            dest = args[-1]
            if not rpath.isabs(dest):
                dest = rpath.normpath(rpath.join(self.config.irodsCwd, dest))
            self.dest = dest
        else:
            self.dest = self.config.irodsCwd

    def parseArguments(self, optp):
        optp.add_option("-r", "--recursive", action='store_true',
                        help="copy directories recursively")
        IRODSClientController.parseArguments(self, optp)

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
        d = self.client.objStat(self.dest)
        d.addCallbacks(self.cb_checkRemotePath, self.cb_catchSingleFileUpload)
        d.addCallbacks(self.cb_startCopy, self.printStacktrace)
        d.addErrback(self.sendDisconnect)
        return data

    def cb_catchSingleFileUpload(self, failure):
        if len(self.paths) == 1:
            failure.trap(errors.USER_FILE_DOES_NOT_EXIST)
            return self.dest

    def cb_checkRemotePath(self, data):
        if data.objType == 'DATA_OBJ_T':
            return failure.Failure(Exception("remote file %s already exists" % self.dest))
        if data.objType == 'COLL_OBJ_T':
            return self.dest
        return failure.Failure(Exception("remote path exists, but not sure what it is"))

    def cb_startCopy(self, data):
        dest = data
        if self.paths == 1:
            d = self.sendPut(self.paths[0], dest)
            d.addBoth(self.sendDisconnect)
            return data

        cbs = []

        def queue_copy(source, parent=''):
            if source.isdir():
                for child in source.children():
                    cbs.append(self.client.mkcoll(rpath.join(dest, parent, source.basename())))
                    queue_copy(child, rpath.join(parent, source.basename()))
            else:
                cbs.append(self.sendPut(source, rpath.join(dest, parent, source.basename())))

        for source in self.paths:
            queue_copy(source)
        dl = defer.DeferredList(cbs)
        dl.addBoth(self.sendDisconnect)
        return data

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
    controller = PutController(reactor)

    reactor.run()
    return
