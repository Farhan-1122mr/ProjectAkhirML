import serial
import pynmea2
from gpiozero import DistanceSensor, Buzzer, Button, OutputDevice
#from gpiozero.pins.pigpio import PiGPIOFactory
#import warnings
#warnings.filterwarnings("ignore")

class Sensor():
    def __init__(self):        
        #gps
        self.gps_serial = serial.Serial('/dev/ttyAMA0',
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE)

    def get_obstacle(self):
        #ultrasonic
        ultrasonic = DistanceSensor(echo=23, trigger=24)

        #buzzer
        buzzer = Buzzer(16)
        
        #button
        button = Button(25)
        
        while not button.is_pressed:
        #while True:
            print(f"obstacle: {ultrasonic.distance}")
            #print(f"distance: {dist:.1f}") 
            if ultrasonic.distance < 0.7:
            #if button.is_pressed:
                buzzer.on()
                print("in range")
            else:
                buzzer.off()
                print("out of range")
        
        return
         
    def get_location(self):
        try:
            dataout = pynmea2.NMEAStreamReader()
            data = self.gps_serial.readline()
            while data is None or (data[0:6] != b"$GPRMC" and data[0:6] != b"$GPGGA" and data[0:6] != b"$GPGLL"):
                data = self.gps_serial.readline()
            try:
                msg = pynmea2.parse(data.decode('utf-8'))
                lat = msg.latitude
                lng = msg.longitude
                print(f"Latitude: {lat}, Longitude: {lng}")
                return lat, lng
            except:
                print(f"decode error")
                return 0.0, 0.0
        except:
            print("GPS error")
            return 0.0, 0.0
                
if __name__=='__main__':
        sensor=Sensor()
        sensor.get_obstacle()
        

