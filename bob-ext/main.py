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

GPIO.setup([BUZZER, PAD, LIGHTS], GPIO.OUT, initial=GPIO.LOW)

buzzer_PWM = GPIO.PWM(BUZZER, 2)

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
			buzzer_PWM.start(0.5)
		else:
			buzzer_PWM.stop()
		pass
except:
	print 'Exception occured'
finally:
	print 'Cleaning up'
	GPIO.cleanup()
