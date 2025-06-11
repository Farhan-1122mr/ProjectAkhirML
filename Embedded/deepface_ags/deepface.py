from camera import Cam
from constant import TIMESLEEPTHREAD
from recog import DeepfaceHandler
from ags import AGS

import argparse
import functools
import subprocess
import time

class Deepface:
    def __init__(self, debug, withNCS=False, cpuFlag=True, ramFlag=True, diskFlag=True):
        if debug:
            self.camera = Cam(debug=True)
            self.deepface = DeepfaceHandler(withNCS)
            self.ags = AGS(cpuFlag, ramFlag, diskFlag, debug=False)
        else:
            self.camera = Cam(debug=False)
            self.deepface = DeepfaceHandler(withNCS)
            self.ags = AGS(cpuFlag, ramFlag, diskFlag, debug=False)

        self.runable = True
        #self.start()

    @functools.lru_cache(maxsize = None)
    def start(self):
        self.ags.start()

        self.deepface.start()

        self.camera.setTimeToCapture(0)
        self.camera.startCapture()

        try:
            while self.runable:
                self.camera.stream()

                self.camera.setTimeToCapture(self.ags.getTimeToCapture())
                self.deepface.setAgsTimeout(self.ags.getTimeToProcess())

                if self.ags.getCPUWarning():
                    self.deepface.setAgsTimeout(10)

                if self.ags.getRAMWarning():
                    self.runable = False

                if self.ags.getDiskWarning():
                    DiskClearing = subprocess.run(["sudo", "sh", "freeSpace.sh"], stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True)
                    print(DiskClearing.stdout)
                    time.sleep(5)
                    
                # if self.yolo.getYoloResult() is not None:
                    # if self.yolo.getYoloResult()>0 and self.yolo.getYoloResult()<2:
                        # if self.relay is not None: self.relay.appendYoloRes(True)
                    # elif self.yolo.getYoloResult()<=0:
                        # if self.relay is not None: self.relay.appendYoloRes(False)
                    
                time.sleep(TIMESLEEPTHREAD)

            self.RAMrestart()
        except KeyboardInterrupt or OSError:
            self.stop()

    def RAMrestart(self):
        if not self.runable:
            self.stop()
            self.runable = True
            self.start.cache_clear()
            RAMClearing = subprocess.run(["sudo", "sh", "freeRAM.sh"], stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True)
            print(RAMClearing.stdout)
            self.start()

    def stop(self):
        self.ags.stop()
        self.deepface.stop()
        self.camera.stop()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--debug", help="to debug with webcam", action="store_true")
    parser.add_argument("-c", "--cpu", help="to watch CPU avaibality", action="store_true")
    parser.add_argument("-r", "--ram", help="to watch RAM avaibality", action="store_true")
    parser.add_argument("-d", "--disk", help="to watch Internal Storage avaibality", action="store_true")
    parser.add_argument("-n", "--ncs", help="work with Naural Computer Stick", action="store_true")
    args = parser.parse_args()
    Deepface(args.debug, args.ncs, args.cpu, args.ram, args.disk)
