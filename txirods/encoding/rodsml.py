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

from string import Template
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

class SimpleXMLHandler(ContentHandler):
    def __init__(self):
        self.data = {}
        self.__tag = ''
        self.__buffer = ''

    def startDocument(self):
        pass

    def startElement(self, name, attrs):
        self.__buffer = ''
        self.__tag = name

    def characters(self, content):
        if self.__tag:
            self.__buffer = self.__buffer + content

    def endElement(self, name):
        if self.__tag:
            try:
                self.data[self.__tag] = int(self.__buffer)
            except ValueError:
                self.data[self.__tag] = self.__buffer
            self.__tag = ''
            self.__buffer = ''

    def endDocument(self):
        pass


def SimpleXMLParser(data):
    parser = make_parser()
    handler = SimpleXMLHandler()
    parser.setContentHandler(handler)
    parser.feed(data)
    return handler.data


version_pi = Template("""<Version_PI>
<status>$status</status>
<relVersion>$relVersion</relVersion>
<apiVersion>$apiVersion</apiVersion>
<reconnPort>$reconnPort</reconnPort>
<reconnAddr>$reconnAddr</reconnAddr>
<cookie>$cookie</cookie>
</Version_PI>\n""")

