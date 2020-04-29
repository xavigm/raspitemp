#!/usr/bin/python3

import RPi.GPIO as GPIO
import time


led = 16

GPIO.setmode(GPIO.BOARD)
GPIO.setup(led, GPIO.OUT)

GPIO.output(led, GPIO.HIGH)

time.sleep(0.5)

GPIO.output(led, GPIO.LOW)


GPIO.cleanup()