import os.path
import json

class Config:
    def __init__(self) -> None:
        self.start_time = None
        self.verbose = False
        self.CONFIG_PATH = os.path.join('config','config.json')

    def save(self):
        aux = {}
        
        aux['start_time'] = self.start_time
        aux['verbose'] = self.verbose

        json_object = json.dumps(aux, indent = 4)
        # Writing to sample.json
        with open(self.CONFIG_PATH, "w") as json_file:
            json_file.write(json_object)
