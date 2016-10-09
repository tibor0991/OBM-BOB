import Adafruit_DHT

class No_bias:
	def __init__(self):
		pass
		
	def __call__(self, temp):
		return temp
		
class Linear_bias:
	def __init__(self, m, q):
		self.m = m
		self.q = q
		
	def applyBias(self, temp):
		return temp * self.m + self.q

class Quad_bias:
	"""
	Returns the modified temperature using a quadratic function
	written as "a * temp^2 + b * temp + c"
	"""
	def __init__(self, a, b, c):
		self.a = a
		self.b = b
		self.c = c
		
	def applyBias(self, temp):
		return self.a * (temp**2) + self.b * temp + self.c
	
	
class Sensor:
	def __init__(self, pin):
		self.temperature = 0
		self.humidity = 0
		self.pin = pin
		
	def getTemperature(self, bias):
		return bias(self.temperature)
		
	def getHumidity(self):
		return self.humidity
		
	def readSensor(self):
		hum, temp = Adafruit_DHT.read(Adafruit_DHT.DHT22, self.pin)
		if (type(hum) is not type(None)): 
			self.humidity, self.temperature = hum, temp
			
if __name__ == "__main__":
	print "sensor.py self-test"
	sens = Sensor(4)
	sens.readSensor()
	bias = No_bias()
	print sens.getHumidity(), sens.getTemperature(bias)