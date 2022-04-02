import os.path
import json
from datetime import datetime

class Config:
    def __init__(self) -> None:
        self.CONFIG_PATH = os.path.join('config','config.json')
        # In case the file does not exist, a default configuration is loaded
        try:
            # Reading current config.json
            with open(self.CONFIG_PATH, "r") as json_file:
                json_object = json.load(json_file)
            self.language = json_object['language']
            self.start_time = json_object['start_time']
            self.verbose = False
            self.contexts = json_object['contexts']
            self.interactive = json_object['interactive']
        except:
            print("Error loading config.json file")
            self.language = "es"
            self.start_time = datetime.now()
            self.verbose = False
            self.contexts = []
            self.interactive = []
        
        self.initTempConfig()

    """
        Initializes temp.json fields to default values
    """
    def initTempConfig(self):
        # Setting fields for temp.json file
        json_object = {
            'listen': False,
            'console_dev': ""
        }
        tempC = os.path.join('config','temp.json')
        json_object = json.dumps(json_object, indent = 4)
        with open(tempC, "w") as json_file:
            json_file.write(json_object)
    
    """
        Get the language parameter
    """
    def getLanguage(self):
        return self.language

    """
        Update the language parameter
    """
    def setLanguage(self, lg: str):
        self.language = lg

    """
        Get the start_time parameter
    """
    def getStartTime(self):
        return self.start_time

    """
        Update the start_time parameter
    """
    def setStartTime(self, st: int):
        self.start_time = st

    """
        Get the verbose parameter
    """
    def getVerbose(self):
        return self.verbose

    """
        Update the verbose parameter
    """
    def setVerbose(self, vbs: bool):
        self.verbose = vbs

    """
        Get the contexts parameter
    """
    def getContexts(self):
        return self.contexts

    """
        Add a new context
    """
    def addContexts(self, cnt: str):
        self.contexts.append(cnt)

    """
        Get the interactive contexts parameter
    """
    def getInteractive(self):
        return self.interactive

    """
        Add a new interactive context
    """
    def addInteractive(self, cnt: str):
        self.interactive.append(cnt)

    """
        Method to save the configuration in the config.json file
    """
    def save(self):
        aux = {}
        aux['language'] = self.language
        aux['start_time'] = self.start_time
        aux['verbose'] = self.verbose
        aux['contexts'] = self.contexts
        aux['interactive'] = self.interactive

        json_object = json.dumps(aux, indent = 4)
        with open(self.CONFIG_PATH, "w") as json_file:
            json_file.write(json_object)