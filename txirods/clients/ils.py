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

import time
import posixpath as rpath

from twisted.internet import reactor, defer
from txirods.clients.base import IRODSClientController


class PrettyPrinter(object):
    def __init__(self, path='', newline=False):
        self.lens = {'TYPE': 1, 'NAME': 0,
                     'OWNER': 0, 'MODIFIED': 0,
                     'MODE': 0, 'SIZE': 0}
        self.data = []
        self.path = path
        self.newline = newline

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
                        coll[k] = rpath.basename(v)
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
        if self.newline:
            print ''
        if self.path:
            print self.path + ":"
        for row in data:
            print row['TYPE'].ljust(lens['TYPE']),
            print row['OWNER'].ljust(lens['OWNER']),
            print row['SIZE'].ljust(lens['SIZE']),
            print time.strftime('%Y-%m-%d %H:%M',
                                time.localtime(float(row['MODIFIED']))),
            print row['NAME'].ljust(lens['NAME'])
        return


class LsController(IRODSClientController):
    usage = """usage: %prog [options] [file]..."""

    def configure(self, opts, args):
        IRODSClientController.configure(self, opts, args)

        self.paths = list(set(args))
        self.paths.sort()

        if not args:
            self.paths.append(self.config.irodsCwd)

    def sendCommands(self, data):
        cbs = []

        for path in self.paths:
            newline = True
            if path == self.paths[0]:
                newline = False
            if not rpath.isabs(path):
                path = rpath.normpath(rpath.join(self.config.irodsCwd, path))
            d = self.client.objStat(path)
            d.addCallbacks(self.sendListContents, self.printStacktrace, [path, newline])
            cbs.append(d)

        dl = defer.DeferredList(cbs)
        dl.addBoth(self.sendDisconnect)
        return data

    def sendListContents(self, data, path, newline=False):
        if len(self.paths) == 1:
            printer = PrettyPrinter()
        else:
            printer = PrettyPrinter(path=path, newline=newline)

        d = self.client.listCollections(path)
        d.addErrback(self.printStacktrace)
        d.addCallback(self.parseSqlResult)
        d.addCallback(printer.coll_table)

        d = self.client.listObjects(path)
        d.addErrback(self.printStacktrace)
        d.addCallback(self.parseSqlResult)
        d.addCallback(printer.obj_table)
        d.addCallback(printer.prettyprint)
        return data


def main(*args):
    controller = LsController(reactor)

    reactor.run()
    return
