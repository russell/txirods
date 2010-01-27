
from xml.sax.handler import ContentHandler

class IRODSHeaderHandler(ContentHandler):
    def __init__(self, request):
        self.request = request
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
                setattr(self.request, self.__tag, int(self.__buffer))
            else:
                setattr(self.request, self.__tag, self.__buffer)
            self.__tag = ''
            self.__buffer = ''

    def endDocument(self):
        pass

