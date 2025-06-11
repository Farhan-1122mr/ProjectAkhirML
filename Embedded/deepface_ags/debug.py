# import threading
# from datetime import datetime
# import time

# def printit():
#   threading.Timer(5.0, printit).start()
#   print("Hello, World! ", datetime.now())

# printit()
# while True:
#     print("MAIN")
#     time.sleep(2)
  
# import cv2 

# key = cv2. waitKey(1)
# webcam = cv2.VideoCapture(0)
# while True:
#     try:
#         check, frame = webcam.read()
#         print(check) #prints true as long as the webcam is running
#         print(frame) #prints matrix values of each framecd 
#         cv2.imshow("Capturing", frame)
#         key = cv2.waitKey(1)
#         if key == ord('s'): 
#             cv2.imwrite(filename='saved_img.jpg', img=frame)
#             webcam.release()
#             img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
#             img_new = cv2.imshow("Captured Image", img_new)
#             cv2.waitKey(1650)
#             cv2.destroyAllWindows()
#             print("Processing image...")
#             img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
#             print("Converting RGB image to grayscale...")
#             gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
#             print("Converted RGB image to grayscale...")
#             print("Resizing image to 28x28 scale...")
#             img_ = cv2.resize(gray,(28,28))
#             print("Resized...")
#             img_resized = cv2.imwrite(filename='saved_img-final.jpg', img=img_)
#             print("Image saved!")
        
#             break
#         elif key == ord('q'):
#             print("Turning off camera.")
#             webcam.release()
#             print("Camera off.")
#             print("Program ended.")
#             cv2.destroyAllWindows()
#             break
        
#     except(KeyboardInterrupt):
#         print("Turning off camera.")
#         webcam.release()
#         print("Camera off.")
#         print("Program ended.")
#         cv2.destroyAllWindows()
#         break

# import cv2 as cv
# from yolo import YOLO

# cap = cv.VideoCapture(0)
# yolo = YOLO(stream=True)
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
    
#     cv.imshow('frame', frame)

#     # print("type of frame var -> " + str(type(frame)))
#     # print(frame)

#     detect = yolo.detect(frame)

#     # print(str(detect))

#     c = cv.waitKey(5)
#     if c == 27:
#         break

# cap.release()
# cv.destroyAllWindows()

import cv2
cap=cv2.VideoCapture("rtsp://admin:cctv1234@192.168.1.100:554/h264Preview_01_main")

ret,frame = cap.read()
while ret:
    ret,frame = cap.read()
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()