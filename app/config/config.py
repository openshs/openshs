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
            self.start_time = json_object['start_time']
            self.verbose = json_object['verbose']
            self.contexts = json_object['contexts']
        except:
            print("Error loading config.json file")
            self.start_time = None
            self.verbose = datetime.now()
            self.contexts = []

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
        Method to save the configuration in the config.json file
    """
    def save(self):
        aux = {}
        aux['start_time'] = self.start_time
        aux['verbose'] = self.verbose
        aux['contexts'] = self.contexts

        json_object = json.dumps(aux, indent = 4)
        # Writing to sample.json
        with open(self.CONFIG_PATH, "w") as json_file:
            json_file.write(json_object)