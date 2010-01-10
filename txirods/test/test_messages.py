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


    def testDataObjInpMarshall(self):
        dataobjinp_marshalled = '/ARCS/home/russell.sim\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00%@#ANULLSTR$%\x00'
        dataobjinp_parsed = messages.dataObjInp.parse(dataobjinp_marshalled)
        dataobjinp_unmarshalled = Container(keyValPair = Container(len = 0,
                                                keyWords = None,
                                                values = None),
                         createMode = 0,
                         dataSize = 0,
                         numThreads = 0,
                         objPath = '/ARCS/home/russell.sim',
                         offset = 0,
                         openFlags = 0,
                         oprType = 0,
                         specColl = None)

        self.assertTrue(dataobjinp_parsed == dataobjinp_unmarshalled)

        dataobjinp_generated = messages.dataObjInp.build(dataobjinp_unmarshalled)

        self.assertTrue(dataobjinp_generated == dataobjinp_marshalled)


    def testGenQueryOutMarshall(self):
        genqueryout_marshalled = '\x00\x00\x00\x04\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xf5\x00\x00\x00:/ARCS/home/ARCS-COLLAB/Projects/Design Research Institute\x00/ARCS/home/ARCS-COLLAB/Projects/Plone - DF integration\x00/ARCS/home/ARCS-COLLAB/Projects/TWiki AAF Integration\x00/ARCS/home/ARCS-COLLAB/Projects/UQ AWMC SCORe PWP Project\x00\x00\x00\x01\xf7\x00\x00\x00:anders.boman\x00anders.boman\x00anders.boman\x00anders.boman\x00\x00\x00\x01\xfc\x00\x00\x00:01256013640\x0001256013656\x0001256013683\x0001256013696\x00\x00\x00\x01\xfd\x00\x00\x00:01256013640\x0001256013656\x0001256013683\x0001256013696\x00\x00\x00\x01\xfe\x00\x00\x00:\x00\x00\x00\x00\x00\x00\x01\xff\x00\x00\x00:\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00:\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00'
        genqueryout_parsed = messages.genQueryOut.parse(genqueryout_marshalled)
        genqueryout_unmarshalled = Container(attriCnt = 7,
                                             continueInx = 0,
                                             rowCnt = 4,
                                             sqlResult = [Container(const = 'COL_COLL_NAME',
                                                                    len = 58,
                                                                    value = ['/ARCS/home/ARCS-COLLAB/Projects/Design Research Institute',
                                                                             '/ARCS/home/ARCS-COLLAB/Projects/Plone - DF integration',
                                                                             '/ARCS/home/ARCS-COLLAB/Projects/TWiki AAF Integration',
                                                                             '/ARCS/home/ARCS-COLLAB/Projects/UQ AWMC SCORe PWP Project']),
                                                          Container(const = 'COL_COLL_OWNER_NAME',
                                                                    len = 58,
                                                                    value = ['anders.boman',
                                                                             'anders.boman',
                                                                             'anders.boman',
                                                                             'anders.boman']),
                                                          Container(const = 'COL_COLL_CREATE_TIME',
                                                                    len = 58,
                                                                    value = ['01256013640',
                                                                             '01256013656',
                                                                             '01256013683',
                                                                             '01256013696']),
                                                          Container(const = 'COL_COLL_MODIFY_TIME',
                                                                    len = 58,
                                                                    value = ['01256013640',
                                                                             '01256013656',
                                                                             '01256013683',
                                                                             '01256013696']),
                                                          Container(const = 'COL_COLL_TYPE',
                                                                    len = 58,
                                                                    value = ['',
                                                                             '',
                                                                             '',
                                                                             '']),
                                                          Container(const = 'COL_COLL_INFO1',
                                                                    len = 58,
                                                                    value = ['',
                                                                             '',
                                                                             '',
                                                                             '']),
                                                          Container(const = 'COL_COLL_INFO2',
                                                                    len = 58,
                                                                    value = ['',
                                                                             '',
                                                                             '',
                                                                             ''])],
                                             totalRowCount = 0)

        self.assertTrue(genqueryout_parsed == genqueryout_unmarshalled)

        genqueryout_generated = messages.genQueryOut.build(genqueryout_unmarshalled)

        # TODO Currently broken because it doesn't pad with ANULLSTR
        #self.assertTrue(genqueryout_generated == genqueryout_marshalled)


