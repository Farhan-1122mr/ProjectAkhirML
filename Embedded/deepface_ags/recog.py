from threading import Thread
from datetime import datetime

import torch.hub
import watchdog.events
import watchdog.observers
import pandas as pd
import cv2 as cv
import numpy as np
import time

from deepface import DeepFace
from tensorflow.python.ops.init_ops_v2 import identity
from ultralytics import YOLO
from constant import *


class Deepface:
    def __init__(self, withNCS, stream=False):
        self.stream = stream
        self.images = []
        self.result = 0
        self.timeout = None
        self.resumeTime = None
        self.backends = ["opencv", "ssd", "dlib", "mtcnn", "retinaface"]
        self.models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
        self.metrics = ["cosine", "euclidean", "euclidean_l2"]


    def detect(self, image):
        if not self.isContinueProcess():
            return 2
        elif self.isContinueProcess():
            self.timeout = None
            self.resumeTime = None
            try:
                self.prepareImg(image=image)
                people = DeepFace.find(img_path=image,
                                       db_path="./database",
                                       model_name=self.models[2],
                                       distance_metric=self.metrics[1])

                # Print the identities of the recognized people
                for person in people:
                    identity = person['identity'][0].split('/')[2]
                    print(identity)

                analyzefile = pd.DataFrame({
                    'timeProcessed': [datetime.now().strftime("%d-%m-%Y_%H:%M:%S")],
                    'filename': [image],
                    'identity': [identity],
                })
                analyzefile.to_csv('./dataLog/detectLog.csv', mode='a', index=False, header=False)
                            
                return 0
            except Exception as e:
                print(str(e))
                return 0

    def confiAvg(self, confidences):
        if len(confidences) != 0:
            return sum(confidences)/len(confidences)
        return 0

    def prepareImg(self, image):
        if not self.stream:
            image = cv.imread(image)
        if image is None:
            print('[]\tDeepface image not read correctly')

    def isContinueProcess(self):
        if self.resumeTime is not None:
            now = datetime.now()
            diff = now - self.resumeTime
            diff = diff.total_seconds()
            if diff >= self.timeout:
                return True
        return False

    def setTimeoutDeepface(self, num):
        if self.resumeTime is None:
            self.resumeTime = datetime.now()
            self.timeout = num
            print("[]\tDeepface process delay for {} s".format(num))

class EventHandler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self, withNCS):
        self.deepfaceDetector = Deepface(withNCS)
        self.deepfaceRes = None
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.png'],
                                                             ignore_directories=True, case_sensitive=False)
  
    def on_created(self, event):
        time.sleep(TIMESLEEPTHREAD)
        result = self.deepfaceDetector.detect("./"+str(event.src_path[2:]))
        self.setDeepfaceResult(result)
        print("[]\tDeepface Res in "+str(event.src_path[2:])+" : ", self.getDeepfaceResult())

    def setDeepfaceResult(self, result):
        self.deepfaceRes = result

    def getDeepfaceResult(self):
        return self.deepfaceRes

    def setTimeoutDeepface(self, num):
        self.deepfaceDetector.setTimeoutDeepface(num)

class DeepfaceHandler(watchdog.observers.Observer):
    def __init__(self, withNCS):
        print("[]\tDeepface Starting.....")
        self.isStopped = False
        self.event_handler = EventHandler(withNCS)
        self.observer = watchdog.observers.Observer()
        self.handlerThread = Thread(target=self.run, name="DeepfaceHandler")

    def setAgsTimeout(self, num):
        self.event_handler.setTimeoutDeepface(num)
        
    def setWatchdogTimeout(self, num):
        self.watchdogTimeout = num

    def run(self):
        self.observer.schedule(self.event_handler, path=IMG_PATH, recursive=True)
        self.observer.start()
        try:
            while True:
                if self.isStopped:
                    break
                time.sleep(TIMESLEEPTHREAD)
        except KeyboardInterrupt:
            pass

    def start(self):
        self.handlerThread.start()

    def stop(self):
        self.isStopped = True
        self.observer.stop()
        time.sleep(TIMESLEEPTHREAD)
        self.observer.join()
        self.handlerThread.join()
        print("[]\tDeepface Stopping.....")

    def getDeepfaceResult(self):
        return self.event_handler.getDeepfaceResult()
    
if __name__=="__main__":

    detector = Deepface(False)
    print(detector.detect("./image/coba.jpg"))
