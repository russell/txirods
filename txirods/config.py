
class ConfigParser(object):
    """
    A really simple irods config parser
    """
    def open(self, filename):
        o = open(filename)
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


