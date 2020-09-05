import json
from codecs import open


class TR:
    def __init__(self):
        with open('languages/tr-tr.json', encoding='utf-8') as file:
            self.dict = json.load(file)

    def __dict__(self):
        return self.dict
