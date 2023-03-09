from multiprocessing import Process
import playsound
from gtts import gTTS
import os
from time import sleep

class ThreadController:
    def __init__(self):
        self.response = ''
        self.response_process = Process(target=self.get_voice_response)
        
    def start_voice_response(self):
        self.response_process.start()
        
    def stop_voice_response(self):
        self.response_process.terminate()
        
    def set_voice_response(self, response):
        self.response = response
        
    def get_voice_response(self):
        output = gTTS(text=self.response, lang='id', slow=False)
        output.save('audio/audio.mp3')
        playsound.playsound('audio/audio.mp3', True)
        os.remove('audio/audio.mp3')
        # self.stop_voice_response()
        
    