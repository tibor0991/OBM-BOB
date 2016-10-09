from Adafruit_LED_Backpack import SevenSegment
import socket
import time
import sys
sys.path.append('.') #this is the path relative to bob_init.sh
from common.sender import sender

setpoint_d = SevenSegment.SevenSegment(address=0x71, busnum=1)
temp_d = SevenSegment.SevenSegment(address=0x70, busnum=1)
setpoint_m = 'get setPoint'
temp_m = 'get temp'
setpoint_s = ''
temp_s = ''

setpoint = (setpoint_d, setpoint_m, setpoint_s)
temp = (temp_d, temp_m, temp_s)
list = [ setpoint, temp ]

for d, __, __ in list:
	d.begin()
	d.clear()
	d.write_display()

while 1:
	for led, msg, ans in list:
		ans = sender.sendMessage(msg)
		led.print_float(float(ans))
		led.write_display()
	time.sleep(1)