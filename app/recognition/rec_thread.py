from time import sleep
import pyttsx3 as voz
import speech_recognition as sr
import threading

from datetime import datetime

class Assistant(threading.Thread):
    def __init__(self):
        super().__init__(
            name="simulator_assistant_thread", 
            target=self.run
        )
        self.__voice = voz.init()
        voices=self.__voice.getProperty('voices')
        self.__voice.setProperty('voice', voices[0].id)
        self.__voice.setProperty('rate', 140)
        self.__recognizer = sr.Recognizer()
        self.__run = True

    def run(self):
        while self.__run:
            try:
                expression = self.listen()
                if self.__run:
                    self.__analyze(expression)
            except: pass
    
    def end(self):
        self.__run = False
    
    def listen(self):
        # Reading data from the microphone
        with sr.Microphone() as source:
            print('<Listening>')
            audio = self.__recognizer.listen(source, phrase_time_limit=3)
        
        try:
            return self.__recognizer.recognize_google(audio, language='es-ES')
        except:
            return 'Lo siento no te entendi'
    
    def say(self, text:str):
        self.__voice.say(text)
        self.__voice.runAndWait()

    def __analyze(self, text:str):
        print(f'Creo que dijiste "{text}"')

        text=text.lower()
        text=text.split(' ')

        if 'ordenador' in text:

            if 'hora' in text:
                time=datetime.now().strftime('%H:%M')
                self.say(f'Son las {time}')
        else : self.say(text)

asdsada = Assistant()
asdsada.start()
sleep(1)
asdsada.join()