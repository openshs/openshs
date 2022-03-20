from socket import timeout
from time import sleep
from gtts import gTTS
import speech_recognition as sr
import threading
import os
from pygame import mixer
from datetime import datetime
import json
import traceback

def run():
    keep_running = True
    recognizer = sr.Recognizer()
    language = "es"
    counter = 0


    print('Assitant: Starting execution')
    # In case the file does not exist, a default configuration is loaded
    prev_listen = False
    while keep_running:
        s_listen = False
        try:
            s_listen = should_listen(counter)
            if not s_listen: sleep(0.01)
        except:
            print("Error loading temp.json file")
            print(traceback.format_exc())
            keep_running = False; break
        
        if prev_listen != s_listen and s_listen: playStart()
        
        if s_listen: 
            expression = listen(recognizer)
            s_listen = should_listen(counter)
            if keep_running and s_listen:
                analyze(expression)
        
        if prev_listen != s_listen and not s_listen: playEnd()
        prev_listen = s_listen
        counter += 1
        if counter > 10: playEnd(); keep_running=False
    print('Assitant: Ending execution')
    
def should_listen(counter) -> bool:
    return counter <= 10

def listen(recognizer: sr.Recognizer):
    # Reading data from the microphone
    with sr.Microphone() as source:
        print('<Listening>')
        try:
            audio = recognizer.listen(source, phrase_time_limit=4, timeout=2)
        except sr.WaitTimeoutError: return '-'
    try:
        return recognizer.recognize_google(audio, 
            language='es-ES')
    except: return '-'

def playTemp():
    mixer.init()
    mixer.music.load(os.path.join('tmp.mp3'))
    mixer.music.play()
    while mixer.music.get_busy(): sleep(0.01)
    mixer.quit()
    #os.remove('tmp.mp3')

def playStart():
    mixer.init()
    mixer.music.load(os.path.join('sounds','start.mp3'))
    mixer.music.play()
    while mixer.music.get_busy(): sleep(0.01)
    mixer.quit()

"""
    Play the end file in mp3 format
"""
def playEnd():
    mixer.init()
    mixer.music.load(os.path.join('sounds','end.mp3'))
    mixer.music.play()
    while mixer.music.get_busy(): sleep(0.01)
    mixer.quit()

def say(text:str, language):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save('tmp.mp3')
    playTemp()

def analyze(text:str):
    # In case an expression is not received, nothing should be done
    if text == '-': return
    
    text=text.lower()
    
    say((f'Creo que dijiste "{text}"'), 'es')
    
run()