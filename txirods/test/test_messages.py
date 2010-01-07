#############################################################################
#
# Copyright (c) 2010 Victorian Partnership for Advanced Computing Ltd and
# Contributors.
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

from twisted.trial import unittest
from twisted.web import server, error
from twisted.internet import reactor, defer
from construct import Container
from txirods import messages



class MessageTestCase(unittest.TestCase):

    def testGenQueryMarshall(self):
        genquery_marshalled = "\x00\x00\x01\xf4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00%@#ANULLSTR$%\x00%@#ANULLSTR$%\x00\x00\x00\x00\x07\x00\x00\x01\xf5\x00\x00\x01\x93\x00\x00\x01\x91\x00\x00\x01\xa5\x00\x00\x01\x97\x00\x00\x01\xa4\x00\x00\x01\xa3\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x01\xf5 = '/ARCS/home/russell.sim'\x00"
        genquery_parsed = messages.genQueryInp.parse(genquery_marshalled)
        genquery_unmarshalled = Container(continueInx = 0, inxIvalPair = Container(inx = [501, 403, 401, 421, 407, 420, 419], len = 7, value = [1, 1, 1, 1, 1, 1, 1]), inxValPair = Container(inx = [501], len = 1, value = [" = '/ARCS/home/russell.sim'"]), keyValPair = Container(keyWords = None, len = 0, values = None), maxRows = 500, options = 32, partialStartIndex = 0)

        self.assertTrue(genquery_parsed == genquery_unmarshalled)

        genquery_generated = messages.genQueryInp.build(genquery_unmarshalled)

        self.assertTrue(genquery_generated == genquery_marshalled)




