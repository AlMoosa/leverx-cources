import json
from dicttoxml import dicttoxml
import xml.dom.minidom
from xml.dom.minidom import parseString
import datetime
import decimal


class FileSaver():
    def __init__(self, result, filename):
        self.result = result
        self.filename = filename

    def save(self):
        raise NotImplementedError


class JsonSaver(FileSaver):
    def __init__(self, result, filename):
        super().__init__(result, filename)

    def myconverter(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.__str__()
        elif isinstance(obj, decimal.Decimal):
            return obj.__str__()

    def save(self):
        with open(self.filename, "w") as write_file:
            json.dump(self.result, write_file, sort_keys=True,
                      indent=4, default=self.myconverter)


class XmlSaver(FileSaver):
    def __init__(self, result, filename):
        super().__init__(result, filename)

    def save(self):
        xml = dicttoxml(self.result).decode('utf-8')
        dom = parseString(xml)
        with open(self.filename, "w") as xml_file:
            dom.writexml(xml_file, indent='\n', addindent='\t')
