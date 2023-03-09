from model.dialog_model import Dialog

import threading
import openai
import speech_recognition as sr
import playsound
from gtts import gTTS
import random
import os

class MainController:
    def __init__(self, view, repository):
        self.view = view
        self.repository = repository
        openai.api_key = repository.data['key']
        self.intro = repository.data['greeting'][random.randrange(len(repository.data['greeting']))]
        
    def voice_response(self, response):
        output = gTTS(text=response, lang='id', slow=False)
        output.save('audio/audio.mp3')
        playsound.playsound('audio/audio.mp3', True)
        os.remove('audio/audio.mp3')
        
    def create_view(self):
        self.view.button_send.configure(command=self.send_dialog)
        self.view.button_rec.configure(command=self.rec_dialog)
        self.view.insert_dialog_list(self.repository.record)
        threading.Thread(target=self.intro_thread).start()
        
    def send_dialog(self):
        threading.Thread(target=self.send_dialog_thread).start()
    
    def rec_dialog(self):
        self.view.insert_dialog(Dialog('assistant', self.intro))
        self.voice_response(self.intro)
        
    def intro_thread(self):
        self.view.insert_dialog(Dialog('assistant', self.intro))
        self.voice_response(self.intro)
        
    def send_dialog_thread(self):
        message = Dialog('user',self.view.entry.get())
        self.view.entry.delete(0, len(message.content))
        self.view.insert_dialog(message)
        self.repository.record.append(message)
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages = self.repository.record_to_json()
        )
        reply = Dialog('assistant',chat_completion.choices[0].message.content)
        self.view.insert_dialog(reply)
        self.repository.record.append(reply)
        self.voice_response(reply.content)
        self.repository.save_json()