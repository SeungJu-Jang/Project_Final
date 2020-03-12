#-*-coding:utf-8-*-

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

trig=23
echo=24

print("start")

GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
GPIO.setup(mort,GPIO.OUT)

GPIO.output(trig, False)
time.sleep(2)

try :
    while True :
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
                GPIO.output(mort, True)
                print("%.1f cm" % distance)
                
        time.sleep(0)

except KeyboardInterrupt :
    print("bye")
    GPIO.cleanup()
