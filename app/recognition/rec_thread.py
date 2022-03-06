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
        self.recognizer = sr.Recognizer()
        self.keep_running = True

    """
        This method waits until the "listen" parameter in the temp.json file is true, 
        then listen to what the user says by microphone and act depending on what is 
        established
    """
    def run(self):
        print('Assitant: Starting execution')
        # In case the file does not exist, a default configuration is loaded
        while self.keep_running:
            listen = False
            try:
                listen = self.should_listen()
                if not listen: sleep(0.01)
            except:
                print("Error loading temp.json file")
                self.keep_running = False
                break
            
            if listen:
                expression = self.listen()
                listen = self.should_listen()
                if self.keep_running and listen:
                    self.analyze(expression)
        print('Assitant: Ending execution')
    
    def end(self):
        self.keep_running = False

    def should_listen(self) -> bool:
        CONFIG_PATH = os.path.join('config','temp.json')
        # Reading current temp.json
        with open(CONFIG_PATH, "r") as json_file:
            json_object = json.load(json_file)
        return json_object['listen']
    
    def listen(self):
        # Reading data from the microphone
        with sr.Microphone() as source:
            print('<Listening>')
            audio = self.recognizer.listen(source, phrase_time_limit=2)
        
        try:
            return self.recognizer.recognize_google(audio, language='es-ES')
        except:
            return 'Lo siento, puedes repetir?'
    
    def playMP3(self) :
        mixer.init()
        mixer.music.load('temp.mp3')
        mixer.music.play()
        while mixer.music.get_busy() :
            sleep(0.01)
        mixer.quit()
        os.remove('temp.mp3')
        
    def say(self, text:str):
        tts = gTTS(text=text, lang="es", slow=False)
        filename = 'temp.mp3'
        tts.save(filename)
        
        self.playMP3()
        
    def analyze(self, text:str):
        print(f'Creo que dijiste "{text}"')

        text=text.lower()
        text=text.split(' ')

        if 'ordenador' in text:

            if 'hora' in text:
                time=datetime.now().strftime('%H:%M')
                self.say(f'Son las {time}')
        else : self.say("Lo siento, puedes repetir?")
