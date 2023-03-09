import speech_recognition as sr
import playsound
from gtts import gTTS
import pyttsx3
import os
import json
import random
import openai

# json
json_data = json.load(open('intents.json'))
greeting_patterns = json_data['greeting']['patterns']
greeting_responses = json_data['greeting']['responses']
ask_answer_positive = json_data['ask_to_describe']['positive']
ask_answer_negative = json_data['ask_to_describe']['negative']
api_key = json_data["key"]

# openai
openai.api_key = api_key
messages = [
    {"role":"system", "content":"you are a helpful assistant"},
]

# while True:
#     message = input("ask : ")
#     if message:
#         messages.append(
#             {"role":"user", "content":message},
#         )
#         chat_completion = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo", messages = messages
#         )
        
#     reply = chat_completion.choices[0].message.content
#     print(f"answer : {reply}")
#     messages.append({"role":"assistant", "content":reply})


recognizer = sr.Recognizer()
# voice_engine = pyttsx3.init()

    
def voice_response(response):
    output = gTTS(text=response, lang='id', slow=False)
    output.save('audio.mp3')
    playsound.playsound('audio.mp3', True)
    os.remove('audio.mp3')

voice_response(greeting_responses[random.randrange(len(greeting_responses))])

# status
running = True
ask_described = False
is_described = False
reply_cache = ""

while running:
    try:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.1)
            audio = recognizer.listen(mic)
            
            text = recognizer.recognize_google(audio, language='id-ID')
            text = text.lower()
            print(f'Recognized {text}')
            
            if ask_described:
                for positive in ask_answer_positive:
                    if positive in text:
                        is_described = True
                        ask_described = False
                for negative in ask_answer_negative:
                    if negative in text:
                        voice_response('baiklah')
                        ask_described = False
                if is_described:
                    voice_response('baiklah akan saya jelaskan')
                    voice_response(reply_cache)
                    is_described = False
            else:
                # for greet in greeting_patterns:
                #     if greet in text:
                #         voice_response(greeting_responses[random.randrange(len(greeting_responses))])
                #         pass
                
                message = text
                if message:
                    messages.append(
                        {"role":"user", "content":message},
                    )
                    chat_completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo", messages = messages
                    )
                    
                reply = chat_completion.choices[0].message.content
                print(f"answer : {reply}")
                messages.append({"role":"assistant", "content":reply})
                if len(reply.split()) > 100:
                    voice_response("text terlalu panjang, apakah perlu saya bacakan ?")
                    reply_cache = reply
                    ask_described = True
                else:
                    voice_response(reply)
                    
                if text == "saatnya tidur":
                    with open("sample.json","w") as outfile:
                        json.dump(messages, outfile)
                    running = False
                
            continue
            
    except sr.UnknownValueError:
        print('tidak terdeteksi')
        continue
    
    except Exception as e:
        print(e)
        continue
