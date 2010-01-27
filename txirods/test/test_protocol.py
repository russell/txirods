from twisted.trial import unittest
from twisted.web import server, error
from twisted.internet import reactor, defer
from construct import Container
from txirods import messages
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
        r = protocol.Request()
        handler = header.IRODSHeaderHandler(r)
        parser.setContentHandler(handler)
        parser.feed(self.request)
        self.assertEqual(r.msg_type, 'RODS_CONNECT')
        self.assertEqual(r.msg_len, 111)
        self.assertEqual(r.err_len, 2)
        self.assertEqual(r.bs_len, 3)
        self.assertEqual(r.intinfo, 4)


    def test_iter_header_parse(self):
        from xml.sax import make_parser
        parser = make_parser()
        r = protocol.Request()
        handler = header.IRODSHeaderHandler(r)
        parser.setContentHandler(handler)
        for byte in self.request:
            parser.feed(byte)
        self.assertEqual(r.msg_type, 'RODS_CONNECT')
        self.assertEqual(r.msg_len, 111)
        self.assertEqual(r.err_len, 2)
        self.assertEqual(r.bs_len, 3)
        self.assertEqual(r.intinfo, 4)


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
</StartupPack_PI>"""

    def test_simple_header_parse(self):
        return
        b = StringTransport()
        a = protocol.IRODSChannel()
        a.makeConnection(b)
        a.dataReceived(self.request)
        a.connectionLost(IOError("all one"))
        self.assertEqual(a.header_len, 0)
        self.assertEqual(a.request.msg_len, 338)
        self.assertEqual(a.request.err_len, 0)
        self.assertEqual(a.request.bs_len, 0)
        self.assertEqual(a.request.msg_type, "RODS_CONNECT")

    def test_iter_header_parse(self):
        b = StringTransport()
        a = protocol.IRODSChannel()
        a.makeConnection(b)
        for byte in self.request:
            a.dataReceived(byte)
        a.connectionLost(IOError("all one"))
        self.assertEqual(a.header_len, 0)
        self.assertEqual(a.request.msg_len, 338)
        self.assertEqual(a.request.err_len, 0)
        self.assertEqual(a.request.bs_len, 0)
        self.assertEqual(a.request.msg_type, "RODS_CONNECT")

