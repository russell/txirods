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
from StringIO import StringIO

from twisted.trial import unittest
from txirods import config


class ConfigParserTestCase(unittest.TestCase):

    def test_parse(self):
        config_file = """# iRODS personal configuration file.
#
# This file was automatically created during iRODS installation.
#   Created Sun Jan 24 10:05:17 2010
#
# iRODS server host name:
irodsHost 'ginger'
# iRODS server port number:
irodsPort 1247

# Default storage resource name:
irodsDefResource 'demoResc'
# Home directory in iRODS:
irodsHome '/tempZone/home/rods'
# Current directory in iRODS:
irodsCwd '/tempZone/home/rods'
# Account name:
irodsUserName 'rods'
# Zone:
irodsZone 'tempZone'
"""
        c = config.ConfigParser()
        cfg = StringIO(config_file)
        c.parse(cfg)
        self.assertEqual(c.irodsHost, 'ginger')
        self.assertEqual(c.irodsPort, 1247)
        self.assertEqual(c.irodsDefResource, 'demoResc')
        self.assertEqual(c.irodsHome, '/tempZone/home/rods')
        self.assertEqual(c.irodsCwd, '/tempZone/home/rods')
        self.assertEqual(c.irodsUserName, 'rods')
        self.assertEqual(c.irodsZone, 'tempZone')


