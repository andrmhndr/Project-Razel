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
        self.recognizer = sr.Recognizer()
        self.main_color = '#1F6AA5'
        self.hover_color = '#144870'
        self.intro = repository.data['greeting'][random.randrange(len(repository.data['greeting']))]
        self.recording = False
        self.reply_cache = ''
        
    def voice_response(self, response):
        output = gTTS(text=response, lang='id', slow=False)
        output.save('audio/audio.mp3')
        playsound.playsound('audio/audio.mp3', True)
        os.remove('audio/audio.mp3')
        
    def create_view(self):
        self.view.button_send.configure(command=self.send_dialog)
        self.view.button_rec.configure(command=self.start_rec)
        self.view.insert_dialog_list(self.repository.record)
        threading.Thread(target=self.intro_thread).start()
        
    def send_dialog(self):
        threading.Thread(target=self.send_dialog_thread).start()
        
    def start_rec(self):
        self.view.entry.configure(state='disabled')
        self.view.button_send.configure(state='disabled')
        self.view.button_rec.configure(text='recording...', command=self.stop_rec, fg_color='#a51f1f', hover_color='#701414')
        self.recording = True
        threading.Thread(target=self.record_thread).start()
        
    def stop_rec(self):
        self.recording = False
        self.view.entry.configure(state='normal')
        self.view.button_send.configure(state='normal')
        self.view.button_rec.configure(text='record', command=self.start_rec, fg_color=self.main_color, hover_color=self.hover_color)
        
    def record_thread(self):
        while self.recording:
            print('recording...')
            try:
                with sr.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.1)
                    audio = self.recognizer.listen(mic)
                    
                    text = self.recognizer.recognize_google(audio, language='id-ID')
                    text = text.lower()
                    print(f'Recognized {text}')
                    
                    if text:
                        message = Dialog('user', text)
                        self.view.insert_dialog(message)
                        self.repository.record.append(message)
                        chat_completion = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo", messages = self.repository.record_to_json()
                        )
                        reply = Dialog('assistant', chat_completion.choices[0].message.content)
                        self.view.insert_dialog(reply)
                        self.repository.record.append(reply)
                        self.voice_response(reply.content)
                        self.repository.save_json()
                    
                    continue
                    
            except sr.UnknownValueError:
                print('tidak terdeteksi')
                continue
        
    def intro_thread(self):
        self.view.insert_dialog(Dialog('assistant', self.intro))
        self.voice_response(self.intro)
        
    def send_dialog_thread(self):
        message = Dialog('user',self.view.entry.get())
        self.view.entry.delete(0, 'end')
        self.update_button_state('disabled')
        self.view.insert_dialog(message)
        self.repository.record.append(message)
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages = self.repository.record_to_json()
        )
        reply = Dialog('assistant',chat_completion.choices[0].message.content)
        self.view.insert_dialog(reply)
        self.repository.record.append(reply)
        self.repository.save_json()
        if len(reply.content.split()) > 100:
            self.reply_cache = reply.content
            self.view.show_option(self.yes_option, self.no_option)
            self.voice_response("Text terlalu panjang, apakah anda ingin saya membacakannya ?")
            self.update_button_state('normal')
        else:
            self.voice_response(reply.content)
            self.update_button_state('normal')

    def yes_option(self):
        threading.Thread(target=self.read_cache)
        self.update_button_state('normal')
        self.view.exit_top_level()
        
    def no_option(self):
        self.view.exit_top_level()
        self.update_button_state('normal')
        
    def read_cache(self):
        self.voice_response(self.read_cache)
    
    def update_button_state(self, state):
        self.view.entry.configure(state=state)
        self.view.button_send.configure(state=state)
        self.view.button_rec.configure(state=state)