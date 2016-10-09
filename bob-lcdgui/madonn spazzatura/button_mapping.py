import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0, 0))

#895 = OK
#638 = LEFT
#511 = UP
#383 = RIGHT
#766 = DOWN
#255 = BACK
#128 = RESET

def tol(input):
	t = 2
	return xrange(input-t, input+t)

button_map = { 
	tol(895) : 'OK',
	tol(766) : 'DOWN',
	tol(638) : 'LEFT',
	tol(511) : 'UP',
	tol(383) : 'RIGHT',
	tol(255) : 'BACK',
	tol(128) : 'RESET',
	-1 : 'NULL'
}

def read_button():
	button = button_map.get(mcp.read_adc(0))
	return button