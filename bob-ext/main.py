import RPi.GPIO as GPIO
import sys
sys.path.append('.') #this is the path relative to bob_init.sh
from common.sender import sender
import time
import random

#here goes the code for the relay, the lights and the buzzer
#this file is for the external devices (that is, output devices rather than input ones)
GPIO.setmode(GPIO.BOARD)
PAD = 16
BUZZER = 12
LIGHTS = 18
FAN_IN = 13
FAN_OUT = 15

GPIO.setup([BUZZER, PAD, LIGHTS, FAN_IN, FAN_OUT], GPIO.OUT, initial=GPIO.LOW)

buzzer = GPIO.PWM(BUZZER, 2)
fan_in = GPIO.PWM(FAN_IN, 30)
fan_in.start(0.5)
fan_out = GPIO.PWM(FAN_OUT, 30)
fan_out.start(0.5)

try:
	while True:
		#grab the data you need
		
		#check for the pad
		pad_status = sender.sendMessage('get pad')
		if pad_status == 'on':
			GPIO.output(PAD, GPIO.HIGH)
		else:
			GPIO.output(PAD, GPIO.LOW)
			
		#check for the lights
		lights_status = sender.sendMessage('get lamp')
		if lights_status == 'on':
			GPIO.output(LIGHTS, GPIO.HIGH)
		else:
			GPIO.output(LIGHTS, GPIO.LOW)
			
		#check for the buzzer
		alarm_status = sender.sendMessage('get alarms')
		if not alarm_status == '{}':
			buzzer.start(0.5)
		else:
			buzzer.stop()
		
		#set the fan speed
		fan_in_dc = sender.sendMessage('get fan_in')
		fan_in.ChangeDutyCycle(fan_in_dc)
		
		fan_out_speed = sender.sendMessage('get fan_out')
		fan_out.ChangeDutyCycle(fan_out_dc)
		
except:
	print 'Exception occured'
finally:
	print 'Cleaning up'
	fan_in.stop()
	fan_out.stop()
	buzzer.stop()
	GPIO.cleanup()
