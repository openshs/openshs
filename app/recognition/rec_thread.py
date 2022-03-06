from time import sleep
from gtts import gTTS
import speech_recognition as sr
import threading
from os import remove
from pygame import mixer
from datetime import datetime

class Assistant(threading.Thread):
    def __init__(self):
        super().__init__(
            name="simulator_assistant_thread", 
            target=self.run,
            daemon=True
        )

        self.recognizer = sr.Recognizer()
        
        self.finish = False

    def run(self):
        while not self.finish:
            expression = self.listen()
            if not self.finish:
                self.analyze(expression)
    
    def end(self):
        self.finish = True
    
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
        remove('temp.mp3')
        
    def say(self, text:str):
        print(text)
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
