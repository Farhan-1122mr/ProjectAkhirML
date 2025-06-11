import os
import cv2
import threading
import traceback
# from sensor import Sensor
from api_service import APIService
# from deepface_ags.deepface import Deepface
from voice_computing import VoiceComputing

class Neutrack(APIService):
    def __init__(self):
        super().__init__()
        self.thread_direction = None
        self.thread_ultrasonic = None

        # self.sensor = Sensor()
        # self.deepface = Deepface()
        self.api_service = APIService()

    def speech_recog(self, command, tipe):
        self.text2speech(command, tipe)
        text = self.speech2text()
        return text

    def choice_mode(self):
        try:
            mode = self.speech_recog("Masukkan mode yang anda inginkan", "mode")
            print(f"mode: {mode}")
            self.text2speech(mode, "choice")
            if "tunjukkan jalan" in mode:
                self.directions()
            elif "asisten" in mode:
                self.assistant()
            elif "halo dunia" in mode:
                self.perception()
            elif "siapakah kamu" in mode:
                # self.deepface.start()
                pass
            elif "teman baru" in mode:
                name = self.speech_recog("Masukkan nama teman anda", "firend")
                self.get_img(name)
            else:
                print("Maaf, mode tidak ditemukan.")
                self.text2speech("Maaf, mode tidak ditemukan.", "repeat_mode")
                self.choice_mode()
        except:
            print("Maaf suara Anda kurang jelas")
            self.text2speech("Maaf suara Anda kurang jelas", "error_mode")
            self.choice_mode()
        finally:
            self.choice_mode()

    def get_img(self, name):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera.")
            self.text2speech("Error: Could not open camera.")
            self.choice_mode()
        
        ret, frame = cap.read()
        if ret:
            if name == "captured_image":
                cv2.imwrite(f'{name}.jpg', frame)
                print(f"Image saved as '{name}.jpg'")
            else:
                count = 0
                folder = f'/deepface_ags/database/{name}'
                count = len([file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))])
                if os.path.exists(folder):
                    cv2.imwrite(f'/deepface_ags/database/{name}/{name}_{count+1}.jpg', frame)
                    print(f"Image saved as '{name}_{count}.jpg'")
                else:
                    os.makedirs(folder)
                    cv2.imwrite(f'/deepface_ags/database/{name}/{name}_{count+1}.jpg', frame)
                    print(f"Image saved as '{name}.jpg'")                

        cap.release()
        cv2.destroyAllWindows()

    def directions(self):
        try:
            destination = self.speech_recog("Masukkan tujuan Anda", "destination")
            print(f"tujuan: {destination}")

            # self.thread_ultrasonic = threading.Thread(target=self.sensor.get_obstacle)
            self.thread_direction = threading.Thread(target=self.get_path, args=(destination,))

            self.thread_direction.start()
            # self.thread_ultrasonic.start()

            self.thread_direction.join()
            # self.thread_ultrasonic.join()
        except Exception as e:
            print(f"An error occurred: ", e)
            traceback.print_exc()
            print("Maaf tujuan Anda tidak ditemukan")
            self.text2speech("Maaf tujuan Anda tidak ditemukan", "error_direction")
            self.directions()
        
    def assistant(self):
        question = self.speech_recog("Masukkan pertanyaan Anda", "assistant")
        print(f"pertanyaan: {question}")
        quest = f"pertanyaan Anda adalah "
        quest += question
        self.text2speech(quest, "question")
        self.get_answer(question)
        
    def perception(self):
        try: 
            self.get_img("captured_image")
            self.get_vision()
        except Exception as e:
            print(f"An error occurred: ", e)

if __name__=='__main__':
    main = Neutrack() 
    main.choice_mode()
