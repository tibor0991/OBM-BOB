from multiprocessing import Process, Manager
from sensor import Sensor, No_bias
from settings import Settings
from systemcommand import SystemCommand
from updater import Updater
import time

class System():
	fileName = 'settings.cfg'
	def __init__(self):
		try:
			self.currentSettings = Settings.loadSettings(System.fileName)
		except(IOError):
			print 'No settings file found, reverting to default settings...'
			self.currentSettings = Settings()
			self.currentSettings.saveSettings(self.fileName)
						
		self.manager = Manager()
		self.sharedData = self.manager.dict()
		self.sharedData.update({
			'pad' : 'on',
			'sensors' : self.manager.list([Sensor(4), Sensor(17)]),
			'temp' : 0,
			'hum' : 0,
			'alarms' : self.manager.dict() #if map empty => all green
		})		
		
		self.sharedData.update(self.currentSettings.set_d)
		
		#self.sharedData.update({ 'biases' : self.manager.list(self.currentSettings.set_d['biases'])})
		
	def dumpSettings(self):
		while 1:
			self.currentSettings.updateSettings(self.sharedData)
			self.currentSettings.saveSettings(self.fileName)
			time.sleep(300)

	def start(self):
		self.processes = [SystemCommand(self.sharedData), Updater(self.sharedData), Process(target=self.dumpSettings)]
		for p in self.processes: 
			p.start()
		self.manager.join()
		
		
		
		