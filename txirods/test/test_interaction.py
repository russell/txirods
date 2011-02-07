#############################################################################
#
# Copyright (c) 2011 Russell Sim <russell.sim@gmail.com> and Contributors.
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
#import unittest
from twisted.trial import unittest
from scripttest import TestFileEnvironment
base_path = os.path.join(os.getcwd(), 'interactive_tests')
env = TestFileEnvironment(base_path, cwd=os.getcwd())


class InteractionTestCase(unittest.TestCase):
    if not 'TXIRODS_TEST' in os.environ:
        skip = "interactive tests disabled, to enable export TXIRODS_TEST"

    def test_simple_collection(self):
        filename = 'testdir'
        env.run('./bin/imkdir %s' % filename)
        env.run('./bin/ils %s' % filename)
        env.run('./bin/irmdir %s' % filename)

    def test_upload(self):
        filename = 'testfile'
        dirname = 'testdir'
        env.run('dd if=/dev/random of=%s bs=1M count=2' % filename,
                expect_stderr=True)
        env.run('./bin/imkdir %s' % dirname)
        env.run('./bin/iput %s %s' % (filename, dirname))
        self.assertTrue('testfile' in str(env.run('./bin/ils %s' % dirname)))
        env.run('./bin/irm -r %s' % dirname)

if __name__ == "__main__":
    unittest.runtests()
