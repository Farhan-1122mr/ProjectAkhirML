import time
import wave
import pygame
import base64
import pyaudio
import requests
from gtts import gTTS
from gpiozero import Button
from typing import Optional

class VoiceComputing():
    def __init__(self):
        pygame.mixer.init()
        self.stt_url = "https://api.prosa.ai/v2/speech/stt"
        self.stt_api = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ik5XSTBNemRsTXprdE5tSmtNaTAwTTJZMkxXSTNaamN0T1dVMU5URmxObVF4Wm1KaSIsInR5cCI6IkpXVCJ9.eyJhcHBsaWNhdGlvbl9pZCI6MzkxODA2LCJsaWNlbnNlX2tleSI6IjZiZjFkYmQ5LTk4Y2UtNGY1ZC1iNTY4LTU1YTYwZmRhZTI5ZSIsInVuaXF1ZV9rZXkiOiJjM2IyMTQxOC03MjkzLTRlYzAtOWIzYi0zYThlNDRhNGJlYmIiLCJwcm9kdWN0X2lkIjo1LCJhdWQiOiJhcGktc2VydmljZSIsInN1YiI6ImM4MGY4YWU0LTMwODctNGU4Yy04MTZmLTlkYmVmNGVkMGVjYiIsImlzcyI6ImNvbnNvbGUiLCJpYXQiOjE3MjU3ODQ5MzB9.RAXGzkGoEFlvTpa2LLudC1FS4I31O7CJdJWgEWirQm0iA8LRXpK5aFZgefSOXYg_qgfykz3WftamHKoUe9rtIqQhM2fGk75vpZt7BnnVtC-ITlXn7LmCn4mL621tt_l4m5VpMb65HEJHrSP_rT2VV0F0XFM_ODJi-MhfwDVoVF_0bOrLnXc1Rnp09R1MMSYn0PhZorjmdzGTqEQvhN5QcHNuqLewzcsm2tjmF7kt0udEv_R--M2tzUbX3rW0TyKKE60YpmUuGu2fE9Gu2ruZU-zY53FElDUiVEfzWmv3MCqmfxuK3m8ufzJYkpAKG8j4gEHEZ7LtbahgC9-qwjHjmQ"

    def text2speech(self, message, tipe, long_text=False):
        button = Button(25)
        if long_text:
            pygame.mixer.music.load("wait.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                if button.is_pressed:
                    break
                continue

        tts = gTTS(text=message, lang='id')
        speech_file = f"{tipe}.mp3"
        tts.save(speech_file)

        pygame.mixer.music.load(speech_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

    def speech2text(self, filename="voice_recog.wav") -> dict:
        self.filename = filename
        self.record_audio()
        job = self.submit_stt_request()

        if job["status"] == "complete":
            return job["result"]['data'][0]['transcript']
        
    def record_audio(self, duration: int = 5, fs: int = 44100):
        button = Button(25)
        p = pyaudio.PyAudio()

        button.wait_for_press()
        print("Recording...")
        
        # Open a new stream
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=fs,
                        input=True,
                        frames_per_buffer=1024)

        frames = []
        
        while button.is_pressed:
        #for _ in range(0, int(fs/1024 * duration)):
            data = stream.read(1024)
            frames.append(data)

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Save the recorded data as a WAV file
        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(fs)
            wf.writeframes(b''.join(frames))
        
        print("Recording finished.")

    def submit_stt_request(self) -> dict:
        with open(self.filename, "rb") as f:
            b64audio_data = base64.b64encode(f.read()).decode("utf-8")

        payload = {
            "config": {
                "model": "stt-general",
                "wait": True  # Blocks the request until the execution is finished
            },
            "request": {
                "data": b64audio_data
            }
        }

        response = requests.post(self.stt_url, json=payload, headers={
            "x-api-key": self.stt_api
        })

        return response.json()

if __name__ == '__main__':
    voice = VoiceComputing()
    # print(voice.speech2text())
    voice.text2speech("Mohon ditunggu sebentar, permintaan anda sedang diproses", "wait")
