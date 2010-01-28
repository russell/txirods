
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



