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
from os import path

from twisted.internet import reactor
from txirods.clients.base import IRODSClientController


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


class LsController(IRODSClientController):

    def sendConnect(self):
        user = self.config.irodsUserName
        zone = self.config.irodsZone
        d = self.client.sendConnect(proxy_user=user, proxy_zone=zone,
                                    client_zone=zone, client_user=user)
        d.addCallbacks(self.sendAuth, self.printStacktrace)
        d.addErrback(self.sendDisconnect)

    def sendAuth(self, data):
        d = self.client.sendAuthChallenge(self.credentials.password)
        d.addCallbacks(self.sendStat, self.sendDisconnect)

    def sendStat(self, data):
        pwd = self.config.irodsCwd
        d = self.client.objStat(pwd)
        d.addCallbacks(self.sendListContents, self.printStacktrace)
        return data

    def sendListContents(self, data):
        pwd = self.config.irodsCwd
        printer = PrettyPrinter()
        d = self.client.listCollections(pwd)
        d.addErrback(self.printStacktrace)
        d.addCallback(self.parseSqlResult)
        d.addCallback(printer.coll_table)

        d = self.client.listObjects(pwd)
        d.addErrback(self.printStacktrace)
        d.addCallback(self.parseSqlResult)
        d.addCallback(printer.obj_table)
        d.addCallback(printer.prettyprint)
        self.sendDisconnect(data)
        return data


def main(*args):
    controller = LsController(reactor)

    reactor.run()
    return
