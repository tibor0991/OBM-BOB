from multiprocessing import Process
from sensor import Sensor
from settings import Settings
import netifaces
import logging
import alarms
import data_logger

FAN_STEP = 0.05
FAN_DIFF = 0.1

class Updater(Process):
	def __init__(self, data):
		super(Updater, self).__init__()
		self.data = data
		
	def run(self):
		while 1:
			#read sensors 
			sensors = self.data['sensors']
			for sensor in sensors:
				sensor.readSensor()
			self.data['sensors'] = sensors #updates the sensors array
			
			sens_n = len(self.data['sensors'])			
			readings = [[],[]]
			for sensor, bias in zip(sensors, self.data['biases']):
				readings[0].append( sensor.getHumidity()/sens_n )
				readings[1].append( sensor.getTemperature(bias)/sens_n )
				
			self.data['hum'], self.data['temp'] = sum(readings[0]), sum(readings[1])+15.2
			
			#triggers the thermal pad
			if (self.data['temp'] < self.data['setPoint'] - self.data['tolerance']):
				self._turnPadOn()
				self.decreaseFans()
			elif (self.data['temp'] > self.data['setPoint'] + self.data['tolerance']):
				self._turnPadOff()
				self.increaseFans()
				
			#checks for error conditions
			if (self.data['temp'] < 35 and self.data['pad'] == 'on'):
				#send alarm
				updated_alarms = self.data['alarms']
				updated_alarms.update(alarms.TEMP_LOW)
				self.data['alarms'] = updated_alarms
			elif (self.data['temp'] > 38 and self.data['pad'] == 'off'):
				#send alarm too
				updated_alarms = self.data['alarms']
				updated_alarms.update(alarms.TEMP_HIGH)
				self.data['alarms'] = updated_alarms
			
			#update the machine's IP
			self.data['ip'] = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
			
			#save this reading in a logfile
			data_logger.addLogEntry(self.data['temp'], self.data['hum'])
			
	def _turnPadOn(self):
		self.data['pad'] = 'on'
		
	def _turnPadOff(self):
		self.data['pad'] = 'off'	
		
	def increaseFans(self):
		fan_out = self.data['fan_out'] + FAN_STEP
		if fan_out > 1.0: fan_out = 1.0
		self.data['fan_out'] = fan_out
		self.data['fan_in'] = fan_out - FAN_DIFF
		
	def decreaseFans(self):
		fan_in = self.data['fan_in'] - FAN_STEP
		if fan_in < 0.0: fan_in = 0.0
		self.data['fan_in'] = fan_in
		self.data['fan_out'] = fan_in + FAN_DIFF
		