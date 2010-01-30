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


