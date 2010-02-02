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

import os
from os import path

homedir = os.getenv('USERPROFILE') or os.getenv('HOME')
dotirodsdir = path.join(homedir, ".irods")
dotirodsEnv = path.join(dotirodsdir, ".irodsEnv")
dotirodsA = path.join(dotirodsdir, ".irodsA")

class ConfigParser(object):
    """
    A really simple irods config parser
    """
    def read(self):
        o = open(dotirodsEnv)
        self.parse(o)
        o.close()

    def parse(self, string):
        for l in string:
            # skip comments
            if l.startswith('#'):
                continue
            l = l.strip()
            if l.startswith('irodsPort'):
                setattr(self, 'irodsPort', int(l[9:]))
                continue
            items = l.split("'")
            for i in ['irodsHost', 'irodsDefResource', 'irodsHome',
                      'irodsCwd', 'irodsUserName', 'irodsZone']:
                if not items[0].startswith(i):
                    continue
                setattr(self, items[0].strip(), items[1])


class AuthParser(object):
    """
    A really simple irods auth parser
    """
    def __init__(self):
        self.password = ''
    def read(self):
        o = open(dotirodsA)
        self.parse(o.readlines()[0])
        o.close()

    def parse(self, password):
        self.password = password

    def write(self):
        o = open(dotirodsA, 'w')
        o.write(self.password)
        o.close()

