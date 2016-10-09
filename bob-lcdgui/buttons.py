import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from multiprocessing import Process, Value
import time


#895 = OK
#638 = LEFT
#511 = UP
#383 = RIGHT
#766 = DOWN
#255 = BACK
#128 = RESET

def tol(val):
	t = 2
	return xrange(val-t, val+t)

button_map = { 
	895 : 'OK',
	766 : 'DOWN',
	638 : 'LEFT',
	511 : 'UP',
	383 : 'RIGHT',
	255 : 'BACK',
	128 : 'RESET',
	-1 : 'NULL'
}

class ButtonReader:
	def __init__(self):
		self.buffer = Value('i', 0)
		reader_p = Process(target=self.run)
		reader_p.start()
	
	def run(self):
		self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0,0))
		while True:
			button = self.read_button()
			self.buffer.value = button
			if button_map.get(self.buffer.value) is not None:
				time.sleep(0.25)
		
	def getButton(self):
		r_button = button_map.get(self.buffer.value)
		self.buffer.value = 0
		return r_button

	def read_button(self):
		value = self.mcp.read_adc(0)
		#return button_map.get(value)
		return value
		
		
if __name__ == '__main__':
	test = ButtonReader()
	
	while True:
		print test.getButton()