import json


class FileReader():
    def __init__(self, path):
        self.path = path

    def read(self):
        raise NotImplementedError


class JsonReader(FileReader):
    def __init__(self, path):
        super().__init__(path)

    def read(self):
        try:
            with open(self.path, "r") as read_file:
                return json.load(read_file)

        except FileNotFoundError:
            return "File {} not found!".format(self.path)
