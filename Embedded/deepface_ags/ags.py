import psutil
from threading import Thread
import time
from datetime import datetime
import pandas as pd
from random import randint
from constant import *

class AGS():
    def __init__(self, withCPU, withRAM, withDisk, debug=True) -> None:
        self.withCPU = withCPU
        self.withRAM = withRAM
        self.withDisk = withDisk

        self.CPUThread = None
        self.RAMThread = None
        self.DiskThread = None

        self.CPUData = []
        self.RAMData = []
        self.DiskData = []

        self.RAMWarning = False
        self.CPUWarning = False
        self.DiskWarning = False
        self.RAMReachConst = False

        self.isWatchStopped = False

        self.counterUpthCPU = 1
        self.counterUpthRAM = 1
        self.counterUpthDisk = 1
        
        self.timeToCapture = 1
        self.timeToProcess = 1

        self._cpu = psutil.cpu_percent(0.1)
        self._ram = psutil.virtual_memory()[2]
        self._disk = psutil.disk_usage('/')[3]

    def getCurrentCPUStat(self):
        return self._cpu

    def getCurrentRAMStat(self):
        return self._ram

    def getCurrentDiskStat(self):
        return self._disk

    def getRAMWarning(self):
        return self.RAMWarning

    def getCPUWarning(self):
        return self.CPUWarning

    def getDiskWarning(self):
        return self.DiskWarning

    def getTimeToProcess(self):
        return self.timeToProcess
    
    def getTimeToCapture(self):
        return self.timeToCapture

    def setCurrentStat(self, cpu, ram, disk):
        self._cpu = cpu
        self._ram = ram
        self._disk = disk
    
    def getRAMReachConst(self):
        return self.RAMReachConst

    def watchCPU(self):
        print("[]\t(AGS) Watching CPU")
        CPUStartTime = time.time()
        while True:
            self._cpu = psutil.cpu_percent(0.1)
            if self._cpu:
                CPUTemp = None
                if self._cpu > CONST_CPU and self._cpu < FULL_RESOURCE:
                    if self.CPUWarning : self.CPUWarning = False
                    processDelay = randint(1,5)*self.counterUpthCPU
                    if processDelay > 20: self.timeToProcess = 20
                    else: self.timeToProcess = processDelay
                    self.counterUpthCPU = self.counterUpthCPU + 1
                elif self._cpu >= FULL_RESOURCE:
                    self.CPUWarning = True
                elif self._cpu < CONST_CPU:
                    if self.CPUWarning : self.CPUWarning = False
                    self.counterUpthCPU = 1
                CPUTemp = [datetime.now().strftime("%H:%M:%S"), time.time()-CPUStartTime, self._cpu]
                self.CPUData.append(CPUTemp)

            if self.isWatchStopped:
                break

            time.sleep(TIMESLEEPTHREAD)

    def watchRAM(self):
        print("[]\t(AGS) Watching RAM")
        RAMStartTime = time.time()
        while True:
            self._ram = psutil.virtual_memory()[2]
            if self._ram:
                RAMTemp = None
                if self._ram > CONST_RAM and self._ram < FULL_RESOURCE:
					# adaptasi menghapus gambar yang lama sampai dengan okupansi mencapai batas threshold
                    if not self.RAMReachConst: self.RAMReachConst = True
                    if self.RAMWarning : self.RAMWarning = False
                    captureDelay = 1 + (1 - (CONST_RAM/100)) * self.counterUpthRAM
                    if captureDelay > 6 : self.timeToCapture = 6
                    else: self.timeToCapture = captureDelay
                    self.counterUpthRAM = self.counterUpthRAM + 1
                elif self._ram >= FULL_RESOURCE:
                    self.RAMWarning = True
                elif self._ram < CONST_RAM:
                    self.counterUpthRAM = 1
                    if self.RAMWarning : self.RAMWarning = False
                    if self.RAMReachConst : self.RAMReachConst = False
                RAMTemp = [datetime.now().strftime("%H:%M:%S"), time.time()-RAMStartTime, self._ram]
                self.RAMData.append(RAMTemp)

            if self.isWatchStopped:
                break

            time.sleep(TIMESLEEPTHREAD)

    def watchDisk(self):
        print("[]\t(AGS) Watching Disk Space")
        DiskStartTime = time.time()
        while True:
            self._disk = psutil.disk_usage('/')[3]
            if self._disk:
                DiskTemp = None
                if self._disk > CONST_DISK and self._disk < FULL_RESOURCE_DISK:
                    if self.DiskWarning : self.DiskWarning = False
                    captureDelay = 1 + (1 - (CONST_DISK/100)) * self.counterUpthDisk
                    if captureDelay > 6 : self.timeToCapture = 6
                    else: self.timeToCapture = captureDelay
                    self.counterUpthDisk = self.counterUpthDisk + 1
                elif self._disk >= FULL_RESOURCE_DISK:
                    self.DiskWarning = True
                elif self._disk < CONST_DISK:
                    self.counterUpthDisk = 1
                    if self.DiskWarning : self.DiskWarning = False
                DiskTemp = [datetime.now().strftime("%H:%M:%S"), time.time()-DiskStartTime, self._disk]
                self.DiskData.append(DiskTemp)

            if self.isWatchStopped:
                break

            time.sleep(TIMESLEEPTHREAD)

    def start(self):
        print("[]\tAGS Starting .....")
        try:
            if self.withCPU: 
                self.CPUThread = Thread(target=self.watchCPU, name="CPU")
                self.CPUThread.start()
            if self.withRAM: 
                self.RAMThread = Thread(target=self.watchRAM, name="RAM")
                self.RAMThread.start()
            if self.withDisk: 
                self.DiskThread = Thread(target=self.watchDisk, name="DISK")
                self.DiskThread.start()
        except KeyboardInterrupt or OSError:
            self.stop()

    def stop(self):
        self.isWatchStopped = True
        time.sleep(TIMESLEEPTHREAD)
        if self.CPUThread is not None: self.CPUThread.join()
        if self.RAMThread is not None: self.RAMThread.join()
        if self.DiskThread is not None: self.DiskThread.join()

        CPUdf = pd.DataFrame(self.CPUData, columns=['Time', 'Time_Elapsed', 'CPU_Precentage'])
        CPUdf.to_csv('./dataLog/CPU.csv', index=True)

        RAMdf = pd.DataFrame(self.RAMData, columns=['Time', 'Time_Elapsed', 'RAM_Precentage'])
        RAMdf.to_csv('./dataLog/RAM.csv', index=True)

        Diskdf = pd.DataFrame(self.DiskData, columns=['Time', 'Time_Elapsed', 'Disk_Precentage'])
        Diskdf.to_csv('./dataLog/Disk.csv', index=True)
        print("[]\tAGS Stopping .....")

if __name__=="__main__":
    ags = AGS(True, True, False, debug=False)
    
    try:
        ags.start()
    except KeyboardInterrupt:
        ags.stop()
    finally:
        exit()
    
