#-*-coding:utf-8-*-

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

m_1e=0
m_1a=5
m_1b=6

m_2e=26
m_2a=13
m_2b=19

trig=23
echo=24

MotorStop=0
MotorOn=1
MotorNo=2

CH1=0
CH2=1

OUTPUT=1
INPUT=0

HIGH=1
LOW=0

GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)

GPIO.output(trig, False)
time.sleep(2)

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

print("start")

try :
    while True :
        
        setMotor(CH1, 80, MotorStop)
        setMotor(CH2, 80, MotorStop)
           
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
        
        if distance > 4 :
            if distance < 12 :
                setMotor(CH1, 50, MotorOn)
                setMotor(CH2, 50, MotorOn)
        
        time.sleep(0.5)
           
           
        
except KeyboardInterrupt :
    print("bye")
    GPIO.cleanup()
