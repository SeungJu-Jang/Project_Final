#-*-coding:utf-8-*-

import RPi.GPIO as GPIO
from pyzbar.pyzbar import decode
from ftplib import FTP
import os
import numpy as np
import cv2 
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
fourcc = cv2.VideoWriter_fourcc(*'X264')

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

trig=23
echo=24

GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)

def dec(frame):
     x=decode(frame)
     for i in x:
        (x, y, w, h) = i.rect
        cv2.rectangle(frame,(x, y),(x + w, y + h),(0, 0, 255),2)
        barcodeData = i.data.decode("utf-8")
        barcodeType = i.type
        return(barcodeData,barcodeType,1)
     return('','',0)
    
def QRcode():
    for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
        image=frame.array
        x,y,p=dec(image)
        cv2.imshow("Image",image)
        
        if not x:
            time.sleep(0.02)
        else:
            print(x)
            print(y)
            time.sleep(0.02)
        #if cv2.waitKey(2) & 0xFF == ord('q'):
            #break
        rawCapture.truncate(0)
        return(x)

def SuperSonic():   
    GPIO.output(trig,False)
    time.sleep(0.5)
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)
    while GPIO.input(echo) == 0:
        pulse_start = time.time()
    while GPIO.input(echo) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17000
    distance = round(distance, 2)
                
    #time.sleep(0.02)
    return(distance)

camera=PiCamera()
camera.resolution=(1296,730)
camera.framerate=20
rawCapture=PiRGBArray(camera)

GPIO.output(trig, False)

time.sleep(3)
cv2.namedWindow("Image",cv2.WINDOW_NORMAL)

print("start")



try:
    while True:
        distance = SuperSonic()
        if distance > 4 :
            if distance < 12 :
                print("%.1f cm" % distance)
                QRcode()

except KeyboardInterrupt :
    print("bye")
    GPIO.cleanup()
    #cap.release()
    cv2.destroyAllWindows()
