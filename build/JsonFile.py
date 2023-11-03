import os
import json


class JsonFile:

    def __init__(self, file):
        self.file = file
        if os.path.exists(self.file):
            with open(self.file, 'r') as read_file:
                data = json.load(read_file)
                self.__set_data(data)
        else:
            self.__set_data({})

    def __get_data(self):
        return self.__data

    def __set_data(self, data):
        self.__data = data
    data = property(__get_data, __set_data)

    def save(self):
        with open(self.file, 'w', encoding='utf-8') as f:
            json.dump(self.__data, f, ensure_ascii=False, indent=2)
