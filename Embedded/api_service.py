import re
import json
import pygame
import pyrebase
import requests
import PIL.Image
from gtts import gTTS
from sensor import Sensor
from gpiozero import Button
from ast import literal_eval
import google.generativeai as genai
from voice_computing import VoiceComputing

class APIService(VoiceComputing):
    def __init__(self):	
        super().__init__()
        #Firebase config
        self.gps = Sensor()
        firebaseConfig = {
            "apiKey": "AIzaSyB-sRD6NtNY4-YmzL99uVLjhDmxrTEdZpU",
            "authDomain": "tracking-70c66.firebaseapp.com",
            "projectId": "tracking-70c66",
            "storageBucket": "tracking-70c66.appspot.com",
            "messagingSenderId": "151898302414",
            "appId": "1:151898302414:web:44c029dee4b32eaeeeed9f",
            "measurementId": "G-FWV78JWVX0",
            "databaseURL": "https://tracking-70c66-default-rtdb.firebaseio.com/"
        }

        firebase = pyrebase.initialize_app(firebaseConfig)
        self.firebase_db = firebase.database()
        self.firebase_api = "AIzaSyAPYbtvp0rqzLKTqgUxWyNlFWKE6nuGd2k"

        #Gemini config
        GOOGLE_API_KEY = "AIzaSyB1Guv3ISsit9Z5q_1BJUSZ7gWuOacFurw"
        genai.configure(api_key=GOOGLE_API_KEY)

        #Image-Captioning config
        caption_api = "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"
        self.caption_url = "https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning"
        self.caption_headers = {"Authorization": f"Bearer {caption_api}"}

    def get_directions(self, start_location, end_location):
        print("get direction")
        base_url = "https://maps.googleapis.com/maps/api/directions/json?"
        nav_request = "origin={}&destination={}&key={}&mode=walking&language=id".format(
            start_location,
            end_location,
            self.firebase_api
        )
        request = base_url + nav_request
        response = requests.get(request)
        directions = response.json()
        return directions
    
    def get_path(self, destination):
        #button = Button(16)
        button = False 
        print(f'destination: {destination}')
        end_location = destination
        while not button:
            try:
                lat, lng = self.gps.get_location()
                #lat, lng = -7.289064, 112.765995
                if (lat == 0.0) and (lng == 0.0):
                    print("Sinyal GPS hilang")
                    self.text2speech("Sinyal GPS hilang", "error_gps")
                    break

                start_location = f"{lat},+{lng}"
                print(start_location)
                directions = self.get_directions(start_location, end_location)
                for i, step in enumerate(directions['routes'][0]['legs'][0]['steps']):
                    instruction = re.sub('<.*?>', '', step['html_instructions'])
                    if str(instruction.split(" ")[0][:5]) == "Ambil":
                        instruction = "Mari memulai perjalanan!"
                    elif str(instruction.split(" ")[0][:5]) == "Belok":
                        instruction = f'''{' '.join(instruction.split(" ")[:2])}, lalu'''
                    elif str(' '.join(instruction.split(" ")[:2])) == "Di bundaran,":
                        instruction = f'''Anda akan memasuki bundaran, mohon minta arahan untuk mengambil {str(' '.join(instruction.split(" ")[3:6]))}, lalu '''
                    else:
                        instruction = f'''Anda akan memasuki tikungan, mohon meminta arahan petunjuk selama anda berjalan'''

                    instruction += f" maju selama {step['duration']['text']}"
                    print(instruction)
                    self.text2speech(instruction, "direction")
                    if button:
                        break
            except TypeError as e:
                print(f"Gagal menentukan arah")
                self.text2speech(f"Gagal menentukan arah", "error_direction")
                break

    def get_answer(self, question):
        quest = "saya adalah orang buta yang membutuhkan bantuan, tolong jelaskan secara singkat  "
        quest += question
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(quest)
        answer = response.text.replace("*", "")
        print(answer)
        try:
            self.text2speech(answer, "answer", True)
        except Exception as e:
            print(f"error: {e}")

    def get_caption(self):
        with open("captured_image.jpg", "rb") as f:
            data = f.read()
        response = requests.post(self.caption_url, headers=self.caption_headers, data=data)
        text = response.json()[0]['generated_text']
        print(text)

    def get_vision(self):
        print("get vision")
        img = PIL.Image.open("captured_image.jpg")
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(["ini adalah apa yang ada di hadapan orang buta, jelaskan dengan baik agar dia mengetahui apa yang ada dihadapannya", img])
        answer = response.text.replace("*", "")
        print(answer)
        self.text2speech(answer, "caption", True)

if __name__ == '__main__':
    api_service = APIService()
    # prompt = "tolong antarkan saya ke indomie cak su"
    # func = literal_eval(api_service.get_answer(f"between these 2 functions: (get_path (gets the path to a destination), get_answer(gets the answer for a certain prompt)), which function will suit best as the input of {prompt}. if 'get_answer' is the best option, reply with just: ['get_answer'], otherwise if get_path is the best function for the prompt, reply with just this:['get_path', <the destination given in the prompt>]'. don't give any additional answer or reply, i just want the array definition"))
    # print(func)
    
    # if func[0] == 'get_answer':
    #     print('enter answer')
    #     api_service.get_answer(prompt)
    # elif func[0] == 'get_path':
    #     api_service.get_path(destination=func[1])
        
    #api_service.get_path("ITS Surabaya")
    api_service.get_vision()
    #api_service.get_answer("siapa nama presiden indonesia")
