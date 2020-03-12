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

m_1e=0
m_1a=5
m_1b=6

m_2e=26
m_2a=13
m_2b=19

MotorStop=0
MotorOn=1
MotorNo=2

CH1=0
CH2=1

OUTPUT=1
INPUT=0

HIGH=1
LOW=0

def dec(frame):
     x=decode(frame)
     for i in x:
        (x, y, w, h) = i.rect
        cv2.rectangle(frame,(x, y),(x + w, y + h),(0, 0, 255),2)
        barcodeData = i.data.decode("utf-8")
        barcodeType = i.type
        return(barcodeData,barcodeType,1)
     return('','',0)
    
def setpinConfig(EN, INA, INB):
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    pwm=GPIO.PWM(EN, 50)
    pwm.start(0)
    return pwm

def setMotorControl(pwm, INA, INB, speed, stat):
    pwm.ChangeDutyCycle(speed)
    
    if stat == MotorOn:
        GPIO.output(INA, HIGH)
        GPIO.output(INB, LOW)
    if stat == MotorNo:
        GPIO.output(INA, LOW)
        GPIO.output(INB, HIGH)
    if stat == MotorStop:
        GPIO.output(INA, LOW)
        GPIO.output(INB, LOW)
        
def setMotor(ch, speed, stat):
    if ch == CH1:
        setMotorControl(pwmA, m_1a, m_1b, speed, stat)
    if ch == CH2:
        setMotorControl(pwmB, m_2a, m_2b, speed, stat)
        
pwmA=setpinConfig(m_1e, m_1a, m_1b)
pwmB=setpinConfig(m_2e, m_2a, m_2b)

camera=PiCamera()
camera.resolution=(1296,730)
camera.framerate=20
rawCapture=PiRGBArray(camera)
time.sleep(3)
cv2.namedWindow("Image",cv2.WINDOW_NORMAL)


