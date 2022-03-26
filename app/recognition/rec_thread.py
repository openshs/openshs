from time import sleep
from gtts import gTTS
import speech_recognition as sr
import threading
import os
from pygame import mixer
from datetime import datetime
import json
import traceback

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
        except: 
            self.keep_running = False
            print(traceback.format_exc())

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
            s_listen = False
            try:
                s_listen = self.should_listen()
                if not s_listen: sleep(0.01)
            except:
                print("Error loading temp.json file")
                print(traceback.format_exc())
                self.keep_running = False; break
            
            if prev_listen != s_listen and s_listen: self.playStart()
            
            if s_listen: 
                expression = self.listen()
                s_listen = self.should_listen()
                if self.keep_running and s_listen:
                    self.analyze(expression)
            
            if prev_listen != s_listen and not s_listen: self.playEnd()
            prev_listen = s_listen
        print('Assitant: Ending execution')
    
    """
        Finish the execution of the thread by making use of a bool flag
    """
    def end(self):
        self.keep_running = False

    """
        Check the "listen" parameter in the "temp.json" file 
    """
    def should_listen(self) -> bool:
        path = os.path.join('config','temp.json')
        try:
            # Reading current temp.json
            with open(path, "r") as json_file:
                json_object = json.load(json_file)
            return json_object['listen']
        except:
            print("Error reading listen field in json")
            return False
    
    """
        Recognizes input audio over microphone and passes it 
        to text
    """
    def listen(self):
        # Reading data from the microphone
        with sr.Microphone() as source:
            print('<Listening>')
            try:
                audio = self.recognizer.listen(source, phrase_time_limit=4, timeout=1)
            except sr.WaitTimeoutError: return '-'
        try:
            return self.recognizer.recognize_google(audio, 
                language='es-ES')
        except: return '-'
    
    """
        Play the temporary file in mp3 format
    """
    def playTemp(self):
        mixer.init()
        mixer.music.load(os.path.join('temp','tmp.mp3'))
        mixer.music.play()
        while mixer.music.get_busy(): sleep(0.01)
        mixer.quit()
        #os.remove('tmp.mp3')

    """
        Play the startup file in mp3 format
    """
    def playStart(self):
        mixer.init()
        mixer.music.load(os.path.join('recognition','sounds','start.mp3'))
        mixer.music.play()
        while mixer.music.get_busy(): sleep(0.01)
        mixer.quit()
    
    """
        Play the end file in mp3 format
    """
    def playEnd(self):
        mixer.init()
        mixer.music.load(os.path.join('recognition','sounds','end.mp3'))
        mixer.music.play()
        while mixer.music.get_busy(): sleep(0.01)
        mixer.quit()
    
    """
        Using gTTS library changes text to speech and saves it into a
        temporary file
    """
    def say(self, text:str):
        tts = gTTS(text=text, lang=self.language, slow=False)
        tts.save(os.path.join('temp','tmp.mp3'))
        self.playTemp()

    """
        Analyzes a text according to the configuration defined 
        in the recognition.json file and reacts
    """  
    def analyze(self, text:str):
        # In case an expression is not received, nothing should be done
        if text == '-': return
        
        text = text.lower()
        
        if self.custom_config["name"] in text:
            # Assistant´s name is removed
            text = text.replace(self.custom_config["name"], '')
            
            # Extract requests dictionary
            requests = self.custom_config["requests"]

            if 'hora' in text and len(text.split(' ')) <= 5:
                time=datetime.now().strftime('%H:%M')
                self.say(f'Son las {time}')
                return
            for req in requests:
                tags = requests[req]['tags']
                if all(t in text for t in tags):
                    if requests[req]['type'] == 'command':
                        self.execute(requests[req]["cmd"])
                    if 'response' in requests[req]:
                        self.say(requests[req]['response'])
                    return
            self.say('Creo que dijiste, '+text)
    
    """
        According on the command that is passed as input it will do 
        implemented functions
    """
    def execute(self, cmd: str):
        path = os.path.join('config','devices.json')
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
        

