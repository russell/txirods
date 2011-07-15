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

    def setUp(self):
        env.run('./bin/icd')
        self.testdir = 'testdir'
        self.testfile = "testfile"
        env.run('./bin/irm -r %s' % self.testdir, expect_stderr=True)

    def tearDown(self):
        env.run('./bin/irm -r %s' % self.testdir, expect_stderr=True)

    def test_simple_collection(self):
        env.run('./bin/imkdir %s' % self.testdir)
        env.run('./bin/ils %s' % self.testdir)

    def test_change_directory(self):
        env.run('./bin/imkdir %s' % self.testdir)
        pwd = env.run('./bin/ipwd')
        env.run('./bin/icd %s' % self.testdir)
        cwd = env.run('./bin/ipwd')
        self.assertTrue(cwd.stdout.startswith(pwd.stdout[:-1]))

    def test_upload(self):
        env.run('dd if=/dev/random of=%s bs=1M count=2' % self.testfile,
                expect_stderr=True)
        env.run('./bin/imkdir %s' % self.testdir)
        env.run('./bin/iput %s %s' % (self.testfile, self.testdir))
        self.assertTrue('testfile' in str(env.run('./bin/ils %s' % self.testdir)))

if __name__ == "__main__":
    unittest.runtests()
