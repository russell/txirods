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
from txirods import protocol
from txirods import header
from twisted.test.proto_helpers import StringTransport


class IRODSHeaderParserTestCase(unittest.TestCase):

    request = """<MsgHeader_PI>
<type>RODS_CONNECT</type>
<msgLen>111</msgLen>
<errorLen>2</errorLen>
<bsLen>3</bsLen>
<intInfo>4</intInfo>
</MsgHeader_PI>
"""

    def test_simple_header_parse(self):
        from xml.sax import make_parser
        parser = make_parser()
        r = protocol.Response()
        handler = header.IRODSHeaderHandler(r)
        parser.setContentHandler(handler)
        parser.feed(self.request)
        self.assertEqual(r.msg_type, 'RODS_CONNECT')
        self.assertEqual(r.msg_len, 111)
        self.assertEqual(r.err_len, 2)
        self.assertEqual(r.bs_len, 3)
        self.assertEqual(r.int_info, 4)

    def test_iter_header_parse(self):
        from xml.sax import make_parser
        parser = make_parser()
        r = protocol.Response()
        handler = header.IRODSHeaderHandler(r)
        parser.setContentHandler(handler)
        for byte in self.request:
            parser.feed(byte)
        self.assertEqual(r.msg_type, 'RODS_CONNECT')
        self.assertEqual(r.msg_len, 111)
        self.assertEqual(r.err_len, 2)
        self.assertEqual(r.bs_len, 3)
        self.assertEqual(r.int_info, 4)


class IRODSProtocolTestCase(unittest.TestCase):

    request = """\0\0\0\x8b<MsgHeader_PI>
<type>RODS_CONNECT</type>
<msgLen>338</msgLen>
<errorLen>0</errorLen>
<bsLen>0</bsLen>
<intInfo>0</intInfo>
</MsgHeader_PI>
<StartupPack_PI>
<irodsProt>0</irodsProt>
<reconnFlag>0</reconnFlag>
<connectCnt>0</connectCnt>
<proxyUser>russell.sim</proxyUser>
<proxyRcatZone>ARCS</proxyRcatZone>
<clientUser>russell.sim</clientUser>
<clientRcatZone>ARCS</clientRcatZone>
<relVersion>rods2.1</relVersion>
<apiVersion>d</apiVersion>
<option></option>
</StartupPack_PI>
"""

    def test_simple_header_parse(self):
        return
        b = StringTransport()
        a = protocol.IRODSChannel()
        a.makeConnection(b)
        a.dataReceived(self.request)
        a.connectionLost(IOError("all done"))
        self.assertEqual(a.header_len, 0)
        self.assertEqual(a.response.msg_len, 338)
        self.assertEqual(a.response.err_len, 0)
        self.assertEqual(a.response.bs_len, 0)
        self.assertEqual(a.response.msg_type, "RODS_CONNECT")
        self.assertEqual(a.message_len, 0)
        self.assertEqual(a._processed_header, False)

    def test_iter_header_parse(self):
        b = StringTransport()
        a = protocol.IRODSChannel()
        a.makeConnection(b)
        for byte in self.request:
            a.dataReceived(byte)
        a.connectionLost(IOError("all done"))
        self.assertEqual(a.header_len, 0)
        self.assertEqual(a.response.msg_len, 338)
        self.assertEqual(a.response.err_len, 0)
        self.assertEqual(a.response.bs_len, 0)
        self.assertEqual(a.response.msg_type, "RODS_CONNECT")
        self.assertEqual(a.message_len, 0)
        self.assertEqual(a._processed_header, False)

    several_requests = """\0\0\0\x8b<MsgHeader_PI>
<type>RODS_CONNECT</type>
<msgLen>338</msgLen>
<errorLen>0</errorLen>
<bsLen>0</bsLen>
<intInfo>0</intInfo>
</MsgHeader_PI>
<StartupPack_PI>
<irodsProt>0</irodsProt>
<reconnFlag>0</reconnFlag>
<connectCnt>0</connectCnt>
<proxyUser>russell.sim</proxyUser>
<proxyRcatZone>ARCS</proxyRcatZone>
<clientUser>russell.sim</clientUser>
<clientRcatZone>ARCS</clientRcatZone>
<relVersion>rods2.1</relVersion>
<apiVersion>d</apiVersion>
<option></option>
</StartupPack_PI>
\0\0\0\x8b<MsgHeader_PI>
<type>RODS_VERSION</type>
<msgLen>178</msgLen>
<errorLen>0</errorLen>
<bsLen>0</bsLen>
<intInfo>0</intInfo>
</MsgHeader_PI>
<Version_PI>
<status>0</status>
<relVersion>rods2.1</relVersion>
<apiVersion>d</apiVersion>
<reconnPort>0</reconnPort>
<reconnAddr></reconnAddr>
<cookie>0</cookie>
</Version_PI>
"""

    def test_several_simple_header_parse(self):
        return
        b = StringTransport()
        a = protocol.IRODSChannel()
        a.makeConnection(b)
        a.dataReceived(self.several_requests)
        a.connectionLost(IOError("all done"))
        self.assertEqual(a.header_len, 0)
        self.assertEqual(a.response.msg_len, 178)
        self.assertEqual(a.response.err_len, 0)
        self.assertEqual(a.response.bs_len, 0)
        self.assertEqual(a.response.msg_type, "RODS_VERSION")
        self.assertEqual(a.message_len, 0)
        self.assertEqual(a._processed_header, False)

    def test_several_iter_header_parse(self):
        b = StringTransport()
        a = protocol.IRODSChannel()
        a.makeConnection(b)
        for byte in self.several_requests:
            a.dataReceived(byte)
        a.connectionLost(IOError("all done"))
        self.assertEqual(a.header_len, 0)
        self.assertEqual(a.response.msg_len, 178)
        self.assertEqual(a.response.err_len, 0)
        self.assertEqual(a.response.bs_len, 0)
        self.assertEqual(a.response.msg_type, "RODS_VERSION")
        self.assertEqual(a.message_len, 0)
        self.assertEqual(a._processed_header, False)
