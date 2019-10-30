import json
from dicttoxml import dicttoxml
import xml.dom.minidom
from xml.dom.minidom import parseString


class FileSaver():
    def __init__(self, result):
        self.result = result

    def save(self):
        raise NotImplementedError


class JsonSaver(FileSaver):
    def __init__(self, result):
        super().__init__(result)

    def save(self):
        with open("result.json", "w") as write_file:
            json.dump(self.result, write_file, sort_keys=True, indent=4)


class XmlSaver(FileSaver):
    def __init__(self, result):
        super().__init__(result)

    def save(self):
        xml = dicttoxml(self.result).decode('utf-8')
        dom = parseString(xml)
        with open("result.xml", "w") as xml_file:
            dom.writexml(xml_file, indent='\n', addindent='\t')
