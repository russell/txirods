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


from xml.sax.handler import ContentHandler

class IRODSHeaderHandler(ContentHandler):
    def __init__(self, headers):
        self.headers = headers
        self.__tag = ''
        self.__buffer = ''

    def startDocument(self):
        pass

    def startElement(self, name, attrs):
        self.__tag = ''
        self.__buffer = ''
        element_map = {'type': 'msg_type',
                       'msgLen': 'msg_len',
                       'errorLen': 'err_len',
                       'bsLen': 'bs_len',
                       'intInfo': 'intinfo' }
        if element_map.has_key(name):
            self.__tag = element_map[name]

    def characters(self, content):
        if self.__tag:
            self.__buffer = self.__buffer + content

    def endElement(self, name):
        if self.__tag:
            if self.__tag in ['msg_len', 'err_len', 'bs_len', 'intinfo']:
                setattr(self.headers, self.__tag, int(self.__buffer))
            else:
                setattr(self.headers, self.__tag, self.__buffer)
            self.__tag = ''
            self.__buffer = ''

    def endDocument(self):
        pass

