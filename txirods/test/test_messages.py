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

from twisted.trial import unittest
from twisted.web import server, error
from twisted.internet import reactor, defer
from construct import Container
from txirods.encoding import binary

from txirods.encoding.rodsml import SimpleXMLHandler


class XMLMessageTestCase(unittest.TestCase):

    def test_version_parse(self):
        data = """<Version_PI>
<status>0</status>
<relVersion>rods2.1</relVersion>
<apiVersion>d</apiVersion>
<reconnPort>0</reconnPort>
<reconnAddr></reconnAddr>
<cookie>0</cookie>
</Version_PI>
"""
        from xml.sax import make_parser
        parser = make_parser()
        v = SimpleXMLHandler()
        parser.setContentHandler(v)
        parser.feed(data)
        self.assertEqual(v.data, {u'apiVersion': u'd',
                                  u'cookie': 0,
                                  u'reconnAddr': '',
                                  u'reconnPort': 0,
                                  u'relVersion': u'rods2.1',
                                  u'status': 0})


class BinaryMessageTestCase(unittest.TestCase):

    def testCollInpMarshall(self):
        coll_marshalled = '/tempZone/home/rods/test8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01recursiveOpr\x00\x00'
        coll_parsed = binary.collInp21.parse(coll_marshalled)
        coll_unmarshalled = Container(collName = '/tempZone/home/rods/test8', flags = 0, keyValPair = Container(keyWords = ['recursiveOpr'], len = 1, values = ['']), oprType = 0)

        self.assertEqual(coll_parsed, coll_unmarshalled)

        coll_generated = binary.collInp21.build(coll_unmarshalled)

        self.assertEqual(coll_generated, coll_marshalled)

    def testGenQueryInpMarshall(self):
        genquery_marshalled = "\x00\x00\x01\xf4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00%@#ANULLSTR$%\x00%@#ANULLSTR$%\x00\x00\x00\x00\x07\x00\x00\x01\xf5\x00\x00\x01\x93\x00\x00\x01\x91\x00\x00\x01\xa5\x00\x00\x01\x97\x00\x00\x01\xa4\x00\x00\x01\xa3\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x01\xf5 = '/ARCS/home/russell.sim'\x00"
        genquery_parsed = binary.genQueryInp.parse(genquery_marshalled)
        genquery_unmarshalled = Container(continueInx = 0, inxIvalPair = Container(inx = ['COL_COLL_NAME', 'COL_DATA_NAME', 'COL_D_DATA_ID', 'COL_DATA_MODE', 'COL_DATA_SIZE', 'COL_D_MODIFY_TIME', 'COL_D_CREATE_TIME'], len = 7, value = [1, 1, 1, 1, 1, 1, 1]), inxValPair = Container(inx = ['COL_COLL_NAME'], len = 1, value = [" = '/ARCS/home/russell.sim'"]), keyValPair = Container(keyWords = [], len = 0, values = []), maxRows = 500, options = 32, partialStartIndex = 0)

        self.assertEqual(genquery_parsed, genquery_unmarshalled)

        genquery_generated = binary.genQueryInp.build(genquery_unmarshalled)

        self.assertEqual(genquery_generated, genquery_marshalled)

    def testDataObjInpMarshall(self):
        dataobjinp_marshalled = '/ARCS/home/russell.sim\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00%@#ANULLSTR$%\x00'
        dataobjinp_parsed = binary.dataObjInp.parse(dataobjinp_marshalled)
        dataobjinp_unmarshalled = Container(keyValPair = Container(len = 0,
                                                keyWords = [],
                                                values = []),
                         createMode = 0,
                         dataSize = 0,
                         numThreads = 0,
                         objPath = '/ARCS/home/russell.sim',
                         offset = 0,
                         openFlags = 0,
                         oprType = 0,
                         specColl = None)

        self.assertEqual(dataobjinp_parsed, dataobjinp_unmarshalled)

        dataobjinp_generated = binary.dataObjInp.build(dataobjinp_unmarshalled)

        self.assertEqual(dataobjinp_generated, dataobjinp_marshalled)

    def testGenQueryOutMarshall(self):
        genqueryout_marshalled = '\x00\x00\x00\x04\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xf5\x00\x00\x00:/ARCS/home/ARCS-COLLAB/Projects/Design Research Institute\x00/ARCS/home/ARCS-COLLAB/Projects/Plone - DF integration\x00/ARCS/home/ARCS-COLLAB/Projects/TWiki AAF Integration\x00/ARCS/home/ARCS-COLLAB/Projects/UQ AWMC SCORe PWP Project\x00\x00\x00\x01\xf7\x00\x00\x00:anders.boman\x00anders.boman\x00anders.boman\x00anders.boman\x00\x00\x00\x01\xfc\x00\x00\x00:01256013640\x0001256013656\x0001256013683\x0001256013696\x00\x00\x00\x01\xfd\x00\x00\x00:01256013640\x0001256013656\x0001256013683\x0001256013696\x00\x00\x00\x01\xfe\x00\x00\x00:\x00\x00\x00\x00\x00\x00\x01\xff\x00\x00\x00:\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00:\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00'
        genqueryout_parsed = binary.genQueryOut.parse(genqueryout_marshalled)
        genqueryout_unmarshalled = \
            Container(attriCnt = 7,
                      continueInx = 0,
                      rowCnt = 4,
                      sqlResult = [
                          Container(const = 'COL_COLL_NAME',
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

        self.assertEqual(genqueryout_parsed, genqueryout_unmarshalled)

        genqueryout_generated = \
                    binary.genQueryOut.build(genqueryout_unmarshalled)

        # TODO Currently broken because it doesn't pad with ANULLSTR
        #self.assertEqual(genqueryout_generated, genqueryout_marshalled)

    def testSimpleQueryInpMarshall(self):
        simplequery_marshalled = "select * from r_user_main where user_name=?\x00rods\x00%@#ANULLSTR$%\x00%@#ANULLSTR$%\x00%@#ANULLSTR$%\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        simplequery_parsed = binary.simpleQueryInp.parse(simplequery_marshalled)
        simplequery_unmarshalled = \
                Container(sql='select * from r_user_main where user_name=?',
                          arg1='rods',
                          arg2=None,
                          arg3=None,
                          arg4=None,
                          control=0,
                          form=0,
                          maxBufSize=0)

        self.assertEqual(simplequery_parsed, simplequery_unmarshalled)

        simplequery_generated = binary.simpleQueryInp.build(simplequery_unmarshalled)

        self.assertEqual(simplequery_generated, simplequery_marshalled)

    def testSimpleQueryOutMarshall(self):
        simplequery_marshalled = """\x00\x00\x00\x00user_id: 10007
user_name: rods
user_type_name: rodsadmin
zone_name: testZone
user_distin_name:
user_info:
r_comment:
create_ts: 01296541027
modify_ts: 01296541027
\x00"""
        simplequery_parsed = binary.simpleQueryOut.parse(simplequery_marshalled)
        simplequery_unmarshalled = \
                Container(control=0,
                          outBuf="""user_id: 10007
user_name: rods
user_type_name: rodsadmin
zone_name: testZone
user_distin_name:
user_info:
r_comment:
create_ts: 01296541027
modify_ts: 01296541027
""")

        self.assertEqual(simplequery_parsed, simplequery_unmarshalled)

        simplequery_generated = binary.simpleQueryOut.build(simplequery_unmarshalled)

        self.assertEqual(simplequery_generated, simplequery_marshalled)

    def testCollInp2Marshall(self):
        marshalled = """/testZone/home/rods/test\x00\x00\x00\x00\x00%@#ANULLSTR$%\x00%@#ANULLSTR$%\x00"""

        parsed = binary.collInp.parse(marshalled)
        unmarshalled = \
                Container(collName='/testZone/home/rods/test',
                          keyValPair=Container(
                              keyWords=[],
                              len=0, values=[]))

        self.assertEqual(parsed, unmarshalled)

        generated = binary.collInp.build(unmarshalled)

        self.assertEqual(generated, marshalled)
