# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import sys
import threading
from socket import *
import Queue
import time
from pyzbar.pyzbar import decode
from ftplib import FTP
import os
import numpy as np
import cv2 
from picamera.array import PiRGBArray
from picamera import PiCamera
import pymysql
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#GLOBAL_VARIABLE_SET_UP
#queue1 = Queue.Queue()
queue2 = Queue.Queue()

talchul=True
RST = None

#GPIO_SET_UP
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

m_1e=0
m_1a=5
m_1b=6

m_2e=26
m_2a=13
m_2b=19

sw1=21

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

DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
GPIO.setup(sw1 , GPIO.IN)

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = -2
top = padding
bottom = height-padding

x = 0

font = ImageFont.truetype('/fonts/truetype/nanum/NanumBarunGothic.ttf', 20)

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
            time.sleep(0.00001)

        if x:
            print(x)
            print(y)
            #LED_QR()
            break
        rawCapture.truncate(0)
    camera.close()
    cv2.destroyAllWindows()
    return(x)

def DBRoll(codeset):
    con = pymysql.connect(host="192.168.0.2", user="user", password="1541",db='mydb', charset='utf8')
    #b=str('cnb249')
    cur = con.cursor()
    inner = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
    data_li=str(codeset)
    #data_li=list(data)
    data_li1=data_li.split(',')[0]
    data_li_str=str(data_li1)
    data_li2=data_li.split(',')[1]
    data_li_int=int(data_li2)
    data_li3=data_li.split(',')[2]
    data_goods_num=int(data_li3)
    print(data_li_int)
    print(type(data_li_int))
    
    print(data_li1 + "앞에거 ")
    print(data_li2 + "뒤에거")
    
    sql='ALTER TABLE pro_info MODIFY inventory int'
    cur.execute(sql)

    sql="select inventory from pro_info where codenum=%s"
    numb=cur.execute(sql,(data_li_str))
    data=[list(data_use) for data_use in cur.fetchall()]
    
    for i in range(numb):
        for j in range(0,1):
            inventory=data[i]
            #print(type(inventory[0]))
            #print(inventory)
            if inventory[0] - data_li_int >= 0:
                inventory[0] -= data_li_int #바코드 스캔시 감소되게 처리
            else:
                print("재고 처리가 반영되지 않았습니다.")
    sql="update pro_info set inventory=%s where codenum=%s" #초기 10 -1 한 9값을 재고에서 초기화 하는 부분
    cur.execute(sql,(inventory[0], data_li_str))
    con.commit()
    
    sql='insert into timetable(date1, idproducts, out_goods) values(%s, %s, %s)'
    cur.execute(sql,(inner,data_goods_num,data_li_int))
    con.commit()
    
    sql='ALTER TABLE pro_info MODIFY inventory varchar(20)'
    cur.execute(sql)
    con.commit()
    con.close()
    print("DBupdated")
        
def Motor_In(ok):
    if ok > 4 and ok < 8:
        #LED_Motor()
        setMotor(CH1, 100, MotorOn)
        setMotor(CH2, 100, MotorOn)
        print("MotorRoll")
        time.sleep(1.7)
        setMotor(CH1, 80, MotorStop)
        setMotor(CH2, 80, MotorStop)
        print("MotorStop")
        #LED_QR()
        codeset=QRcodeRoll()
        cv2.destroyAllWindows()
        #LED_DB()
        DBRoll(codeset)
        
        queue2.put(2)

def Motor_Out():

    ko = queue2.get()

    setMotor(CH1, 100, MotorOn)
    setMotor(CH2, 100, MotorOn)
    print("MotorRoll2")
    time.sleep(2)
    for ko in range(ko,0,-1):
        time.sleep(ko)
        print(ko)
    setMotor(CH1, 80, MotorStop)
    setMotor(CH2, 80, MotorStop)
    print("MotorStop2")
        
def SuperSonic():
    global talchul
    while talchul:
        
        if talchul:
            pass
        if talchul == False:
            break
        
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
            if distance < 8 :
                #LED_SONIC()
                print("%.1f cm" % distance)
                Motor_In(distance)
                distance=0
                #queue1.put(distance)
    
def Socket_PC():
    global talchul
    while talchul:
        
        if talchul:
            pass
        if talchul == False:
            break

        clientSock = socket(AF_INET, SOCK_STREAM)
        clientSock.connect(('129.168.0.19', 8080))

        print('연결 확인 됐습니다.')
        clientSock.send('I am a client'.encode('utf-8'))

        print('메시지를 전송했습니다.')

        data = clientSock.recv(1024)
        print('받은 데이터 : ', data.decode('utf-8'))
        
        dataget=data.decode("utf-8")
    
        if dataget =="ON":
            print(dataget)
            # get off
        if dataget == "OFF":
            print(dataget)
            #get on
        if dataget == "Q":
            print("q")
    
    print("server off")
    
        
def Exit_Ready():
    global talchul
    while talchul:
        
        if talchul:
            pass
        if talchul == False:
            break
        
        if GPIO.input(sw1)==0:
            print("ready to die~")
            time.sleep(1)
            talchul = not talchul
            print("talchul : .... %d for gannasekei" % talchul)
            #server_socket.close()
    BYEBYE()
        
def BYEBYE():
    #client_socket.close() 
    print("gannasekei")
    
    #GPIO.cleanup()
    #sys.exit()
    
def YEOUL():
    image = Image.open('1585205842394.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
    disp.image(image)
    disp.display()
    #time.sleep(2)  

pwmA=setpinConfig(m_1e, m_1a, m_1b)
pwmB=setpinConfig(m_2e, m_2a, m_2b)

GPIO.output(trig, False)
time.sleep(3)

print("start")
        
#t0=threading.Thread(target=part1)

T_Roll=threading.Thread(target=SuperSonic)
T_Mort=threading.Thread(target=Motor_Out)
#t2.daemon=True
#T_Sock=threading.Thread(target=Socket_PC)
#t3.daemon=True
T_Exit=threading.Thread(target=Exit_Ready)

def main():
    YEOUL()
    print("main!!! start")
    T_Roll.start()
    T_Mort.start()

    T_Exit.start()
    
    T_Roll.join()
    print("t2. join")
    T_Mort.join()

    T_Exit.join()
    print("t4. join")
    GPIO.cleanup()

if __name__ == "__main__":
    main()