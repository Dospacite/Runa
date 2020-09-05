from codecs import open
from benedict import benedict
import json


class JSON:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, encoding='utf-8') as file:
            self.dict = benedict(json.load(file))

    def set_value(self, path, value):
        self.dict[path] = value
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.dict, file, ensure_ascii=False, indent=2)

    def set_value_at_index(self, path, index, key, value):
        self.dict[path][index][key] = value
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.dict, file, ensure_ascii=False, indent=2)

    def delete_key(self, path):
        del self.dict[path]
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.dict, file, ensure_ascii=False, indent=2)

    def add_value(self, path, value):
        if not self.dict.get(path):
            self.dict[path] = []
        self.dict[path].append(value)
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.dict, file, ensure_ascii=False, indent=2)

    def remove_value(self, path, value):
        try:
            self.dict[path].remove(value)
        except ValueError:
            pass
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.dict, file, ensure_ascii=False, indent=2)
