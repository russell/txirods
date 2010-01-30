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

