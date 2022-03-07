from time import sleep
from gtts import gTTS
import speech_recognition as sr
import threading
import os
from pygame import mixer
from datetime import datetime
import json

class Assistant(threading.Thread):
    def __init__(self):
        super().__init__(
            name="simulator_assistant_thread", 
            target=self.run
        )
        try:
            self.recognizer = sr.Recognizer()
            self.keep_running = True
            self.language = "es"
            path = os.path.join('config','recognition.json')
            # Reading current recognition.json
            with open(path, "r") as json_file:
                json_object = json.load(json_file)
            self.custom_config = json_object[self.language]
        except: self.keep_running = False

    """
        This method waits until the "listen" parameter in the temp.json file is set to true, 
        then listen to what the user says by microphone and act depending on what is 
        established
    """
    def run(self):
        print('Assitant: Starting execution')
        # In case the file does not exist, a default configuration is loaded
        prev_listen = False
        while self.keep_running:
            listen = False
            try:
                listen = self.should_listen()
                if not listen: sleep(0.01)
            except:
                print("Error loading temp.json file")
                self.keep_running = False; break
            
            #if prev_listen != listen and listen: self.playStart()
            
            if listen: 
                expression = self.listen()
                listen = self.should_listen()
                if self.keep_running and listen:
                    self.analyze(expression)
            
            #if prev_listen != listen and not listen: self.playEnd()
            prev_listen = listen
        print('Assitant: Ending execution')
    
    """
        Finish the execution of the thread by making use of a bool flag
    """
    def end(self):
        self.keep_running = False

    def should_listen(self) -> bool:
        path = os.path.join('config','temp.json')
        # Reading current temp.json
        with open(path, "r") as json_file:
            json_object = json.load(json_file)
        return json_object['listen']
    
    def listen(self):
        # Reading data from the microphone
        with sr.Microphone() as source:
            print('<Listening>')
            audio = self.recognizer.listen(source, phrase_time_limit=2)
        try:
            return self.recognizer.recognize_google(audio, language='es-ES')
        except: return '-'
    
    def playMP3(self):
        mixer.init()
        mixer.music.load('temp.mp3')
        mixer.music.play()
        while mixer.music.get_busy(): sleep(0.01)
        mixer.quit()
        #os.remove('temp.mp3')

    def playStart(self):
        mixer.init()
        mixer.music.load(os.path.join('recognition','sounds','start.mp3'))
        mixer.music.play()
        while mixer.music.get_busy(): sleep(0.01)
        mixer.quit()
    
    def playEnd(self):
        mixer.init()
        mixer.music.load(os.path.join('recognition','sounds','end.mp3'))
        mixer.music.play()
        while mixer.music.get_busy(): sleep(0.01)
        mixer.quit()
    
    def say(self, text:str):
        tts = gTTS(text=text, lang=self.language, slow=False)
        tts.save('temp.mp3')
        
        self.playMP3()
        
    def analyze(self, text:str):
        # In case an expression is not received, nothing should be done
        if text == '-': return
        
        text=text.lower()
        
        if self.custom_config["name"] in text:
            if 'hora' in text:
                time=datetime.now().strftime('%H:%M')
                self.say(f'Son las {time}')
            elif 'luces' in text and 'apaga' in text:
                self.execute(
                    self.custom_config["requests"]["lights_off"]["cmd"])
                self.say(
                    self.custom_config["requests"]["lights_off"]["response"])
            elif 'luces' in text and 'enciende' in text:
                self.execute(
                    self.custom_config["requests"]["lights_on"]["cmd"])
                self.say(
                    self.custom_config["requests"]["lights_on"]["response"])
            #for req in self.custom_config["requests"]:
            # TODO   

        else: self.say((f'Creo que dijiste "{text}"'))
    
    def execute(self, cmd: str):
        path = os.path.join('temp','devices.json')
        with open(path, "r") as json_file:
            devices = json.load(json_file)
        if cmd =="SHT-L":
            for dev in devices:
                aux = str(dev).lower()
                if 'light' in aux or 'lamp' in aux:
                    devices[dev] = 0
        elif cmd =="STT-L":
            for dev in devices:
                aux = str(dev).lower()
                if 'light' in aux or 'lamp' in aux:
                    devices[dev] = 1
        json_object = json.dumps(devices, indent = 4)
        with open(path, "w") as json_file:
            json_file.write(json_object)
        

