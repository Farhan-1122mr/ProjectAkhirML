DEVICEDEBUGCAMERA   = 0
#DEVICESTGCAMERA     = 'rtsp://admin:pass.4.me@192.168.18.252:554/cam/realmonitor?channel=1&subtype=0'
DEVICESTGCAMERA     = 'rtsp://admin:cctv1234@192.168.18.33:554/cam/realmonitor?channel=1&subtype=0'
TIME                = 1
IMG_PATH            = './image/'
TIMESLEEPTHREAD     = 0.1

YOLO_SCALE          = 0.00392
YOLO_IMGSIZE        = (640,640)
YOLO_CONFI          = 0.45
YOLO_WEIGHT         = './model/yolov5s.onnx' #changed
YOLO_CFG            = './model/yolov4-tiny.cfg'  #changed

FULL_RESOURCE       = 100
FULL_RESOURCE_DISK  = 70
CONST_CPU           = 80      #Batas usage CPU jika lebih do something
CONST_RAM           = 28      #Batas usage RAM jika lebih do something pemilihan
CONST_DISK          = 50      #Batas usage Disk jika lebih do something

MAX_RELAY_LIST      = 5
RELAIS_1_GPIO       = 17
