# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import sys
import threading
import Queue
import time
from pyzbar.pyzbar import decode
from ftplib import FTP
import os
import numpy as np
import cv2 
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import pymysql

queue1 = Queue.Queue()
queue2 = Queue.Queue()

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

trig=23
echo=24

GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)

print("Plz Wait")

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
    pwm=GPIO.PWM(EN, 100)
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
        
def QRcodeRoll():
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    
    camera=PiCamera()
    camera.resolution=(1296,730)
    camera.framerate=20
    rawCapture=PiRGBArray(camera)

    cv2.namedWindow("Image",cv2.WINDOW_NORMAL)
    print("QR start")

    for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
        image=frame.array
        x,y,p=dec(image)
        cv2.imshow("Image",image)
        
        
        if not x:
            time.sleep(0.1)

        if x:
            print(x)
            print(y)
            break
        rawCapture.truncate(0)
    camera.close()
    cv2.destroyAllWindows()
    return(x)

def DBRoll(codeset):
    con = pymysql.connect(host="192.168.0.02", user="root", password="1q2w3e",db='db_1', charset='utf8')
    
    #megaebyunsoo
    #codeset
    
    data=str(codeset.decode("utf-8"))
    data_li=list(data)
    print("상품번호" + data_li[0])
    print("상품개수" + data_li[2])
    
    cur = con.cursor()

    #cur.execute("""INSERT INTO test (name, """ + name)")

    #sql="INSERT INTO test1(num) VALUES(%s)"
    sql="select inventory from test1 where goods_numb =%s"
    numb=cur.execute(sql,(data_li[0]))
    con_data=[list(data_use) for data_use in cur.fetchall()]
    for j in range(numb):
        for i in range(0,1):
            inventory=con_data[j]
        inventory[0]-=int(data_li[2])
    con.commit()
    
    sql="update test1 set inventory=%s where goods_numb=%s"
    cur.execute(sql,(inventory[0], data_li[0]))
    con.commit()
    con.close()
        
def part1():
    while True:
        ok = queue1.get()
        if not queue1:
            print("nono")
        if ok > 4 and ok < 10:
            setMotor(CH1, 100, MotorOn)
            setMotor(CH2, 100, MotorOn)
            print("MotorRoll")
            time.sleep(1.7)
            setMotor(CH1, 80, MotorStop)
            setMotor(CH2, 80, MotorStop)
            time.sleep(0.1)
            print("MotorStop")
            codeset=QRcodeRoll()
            cv2.destroyAllWindows()
            DBRoll(codeset)
            time.sleep(0.2)
            queue2.put(2)

def part2():
    while True:
        ko = queue2.get()
        if not queue2:
            print("nono")

        setMotor(CH1, 100, MotorOn)
        setMotor(CH2, 100, MotorOn)
        print("MotorRoll2")
        for ko in range(ko,0,-1):
            time.sleep(ko)
            print(ko)
        setMotor(CH1, 80, MotorStop)
        setMotor(CH2, 80, MotorStop)
        time.sleep(0.5)
        print("MotorStop2")
        
def sensorpart():
    while True:
        time.sleep(1)
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
        distance = round(distance, 3)
        if distance > 4 :
            if distance < 10 :
                print("%.1f cm" % distance)
                queue1.put(distance)
                
pwmA=setpinConfig(m_1e, m_1a, m_1b)
pwmB=setpinConfig(m_2e, m_2a, m_2b)

GPIO.output(trig, False)
time.sleep(3)

print("start")
        
t0=threading.Thread(target=part1)
t1=threading.Thread(target=part2)
t2=threading.Thread(target=sensorpart)

t0.start()
t1.start()
t2.start()