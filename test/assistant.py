import sys
import threading
import tkinter as tk

import  speech_recognition as sr
import pyttsx3 as tts

from neuralintents import GenericAssistant

class Assistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.speaker = tts.init()
        self.speaker.setProperty("rate", 150)
        
        self.assistant = GenericAssistant("intents.json", intent_methods={"file":self.create_file})
        
        self.assistant.train_model()
        
        self.root = tk.Tk()
        self.label = tk.Label(text="R", font=("Arial", 120, "bold"))
        self.label.pack()
        
        threading.Thread(target=self.run_assistant).start()
        
        self.root.mainloop()
    
    def create_file(self):
        with open("somefile.txt", "w") as f:
            f.write("Hellow")
        
    def run_assistant(self):
        while True:
            try:
                with sr.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.recognizer.listen(mic)
                    
                    text = self.recognizer.recognize_google(audio, language='id')
                    # text = text.lower()
                    
                    if "hey razel" in text:
                        self.label.config(fg="red")
                        audio = self.recognizer.listen(mic)
                        text = self.recognizer.recognize_google(audio, language='id')
                        text = text.lower()
                        if text == "stop":
                            self.speaker.say("bye")
                            self.speaker.runAndWait()
                            self.speaker.stop()
                            self.root.destroy()
                            sys.exit()
                        else:
                            if text is not None:
                                response = self.assistant.request(text)
                                if response is not None:
                                    self.speaker.say(response)
                                    self.speaker.runAndWait()
                                self.label.config(fg="black")
            # except:
            #     self.label.config(fg="black")
            #     continue
            except sr.UnknownValueError:
                self.label.config(fg="black")
                continue
            except sr.RequestError:
                self.label.config(fg="black")
                self.speaker.say("Sorry, I couldn't connect to the internet.")
                self.speaker.runAndWait()
                continue
            
Assistant()