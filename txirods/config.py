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

    :var irodsHost: the iRODS host
    :var irodsPort: the iRODS port
    :var irodsDefResource: the default resource
    :var irodsHome: the users home directory
    :var irodsCwd: the current working directory
    :var irodsUserName: the user name
    :var irodsZone: the users home zone
    """
    def __init__(self):
        self.irodsHost = ''
        self.irodsPort = 0
        self.irodsDefResource = ''
        self.irodsHome = ''
        self.irodsCwd = ''
        self.irodsUserName = ''
        self.irodsZone = ''

    def read(self):
        """
        read the iRODS Env file
        """
        o = open(dotirodsEnv)
        self.parse(o)
        o.close()

    def parse(self, lines):
        """
        parse the lines from the iRODS Env file and store the values
        as attributes.

        :param lines: the lines from the iRODS Env file.
        :type lines: List of Str
        """
        for l in lines:
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

    def write(self):
        """
        write the iRODS Env file
        """
        o = open(dotirodsEnv, 'r+')
        out = self.generate(o)
        o.seek(0)
        o.writelines(out)
        o.close()

    def generate(self, lines):
        """
        generate a config file based on the origional config file

        :param lines: the lines from the iRODS Env file.
        :type lines: List of Str
        :rtype: List of Str
        """
        out = []
        to_write = ['irodsHost', 'irodsDefResource', 'irodsHome',
                    'irodsCwd', 'irodsUserName', 'irodsZone', 'irodsPort']
        for l in lines:
            ignore = True
            for t in to_write:
                if l.startswith(t):
                    if t == 'irodsPort':
                        out.append(t + " " + str(getattr(self, t, '')) + "\n")
                        ignore = False
                        break
                    else:
                        out.append(t + " '" + getattr(self, t, '') + "'\n")
                        ignore = False
                        break
            if ignore:
                out.append(l)
            ignore = True
        return out


class AuthParser(object):
    """
    A really simple irods auth parser
    """
    def __init__(self):
        self.password = ''

    def read(self):
        """
        read the iRODS .irodsA file
        """
        o = open(dotirodsA)
        self.parse(o.readlines()[0])
        o.close()

    def parse(self, line):
        """
        parse the iRODS .irodsA file contents

        :param line: the line from the iRODS Env file.
        :type line: Str
        """
        self.password = line

    def write(self):
        """
        write the iRODS .irodsA file
        """
        o = open(dotirodsA, 'w')
        o.write(self.password)
        o.close()

