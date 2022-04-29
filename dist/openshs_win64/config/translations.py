from translate import Translator
import json
import os

class Translations:
    def __init__(self) -> None:
        self.TRANSLATIONS_PATH = os.path.join('config','translations.json')
        # Reading current translations.json
        with open(self.TRANSLATIONS_PATH, "r", encoding='utf-8') as json_file:
            json_object = json.load(json_file)
        self.translations = json_object
        self.dict_lang = {
            'es': 'spanish',
            'en': 'english'
        }

    """
        Check the translation dictionary if there is a key with a supported 
        language (es, en)
    """
    def get_translation(self, key:str, lang:str) -> str:
        return self.translations[key][lang]
    
    def translate(self, from_lang:str, to_lang:str, text:str):
        translator = Translator(
            from_lang=self.dict_lang[from_lang],
            to_lang=self.dict_lang[to_lang]
        )
        return translator.translate(text)