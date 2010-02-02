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

from txirods.clients.ils import PrettyPrinter

class PrettyPrinterTestCase(unittest.TestCase):

    def test_prettyprinter(self):
        p = PrettyPrinter()

        coll_result = [{'COL_COLL_MODIFY_TIME': '01264890484', 'COL_COLL_NAME': '/tempZone/home/rods/test', 'COL_COLL_OWNER_NAME': 'rods', 'COL_COLL_INFO1': '', 'COL_COLL_INFO2': '', 'COL_COLL_TYPE': '', 'COL_COLL_CREATE_TIME': '01264890484'}, {'COL_COLL_MODIFY_TIME': '01264893058', 'COL_COLL_NAME': '/tempZone/home/rods/test1', 'COL_COLL_OWNER_NAME': 'rods', 'COL_COLL_INFO1': '', 'COL_COLL_INFO2': '', 'COL_COLL_TYPE': '', 'COL_COLL_CREATE_TIME': '01264893058'}, {'COL_COLL_MODIFY_TIME': '01264893092', 'COL_COLL_NAME': '/tempZone/home/rods/test2', 'COL_COLL_OWNER_NAME': 'rods', 'COL_COLL_INFO1': '', 'COL_COLL_INFO2': '', 'COL_COLL_TYPE': '', 'COL_COLL_CREATE_TIME': '01264893092'}]
        p.coll_table(coll_result)
        self.assertEqual(p.lens, {'MODE': 0, 'MODIFIED': 11, 'NAME': 25, 'OWNER': 4, 'SIZE': 0, 'TYPE': 1})
        self.assertEqual(p.data, [{'MODIFIED': '01264890484', 'NAME': 'test', 'OWNER': 'rods', 'SIZE': '0', 'TYPE': 'c'}, {'MODIFIED': '01264893058', 'NAME': 'test1', 'OWNER': 'rods', 'SIZE': '0', 'TYPE': 'c'}, {'MODIFIED': '01264893092', 'NAME': 'test2', 'OWNER': 'rods', 'SIZE': '0', 'TYPE': 'c'}])

        obj_result = [{'COL_DATA_NAME': 'setup.cfg', 'COL_D_MODIFY_TIME': '01264933946', 'COL_COLL_NAME': '/tempZone/home/rods', 'COL_D_DATA_ID': '10034', 'COL_DATA_SIZE': '43', 'COL_D_OWNER_NAME': 'rods', 'COL_DATA_MODE': '33261', 'COL_D_CREATE_TIME': '01264933946'}]
        self.assertEqual(p.lens, {'MODE': 0, 'MODIFIED': 11, 'NAME': 25, 'OWNER': 4, 'SIZE': 0, 'TYPE': 1})
        self.assertEqual(p.data, [{'MODIFIED': '01264890484', 'NAME': 'test', 'OWNER': 'rods', 'SIZE': '0', 'TYPE': 'c'}, {'MODIFIED': '01264893058', 'NAME': 'test1', 'OWNER': 'rods', 'SIZE': '0', 'TYPE': 'c'}, {'MODIFIED': '01264893092', 'NAME': 'test2', 'OWNER': 'rods', 'SIZE': '0', 'TYPE': 'c'}])




