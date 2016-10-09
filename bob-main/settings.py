import sensor
import pickle

class Settings:
	def __init__(self):	
		self.set_d = {
			'name' : 'bob',
			'setPoint' : 36.5,
			'biases' : [ sensor.No_bias(), sensor.No_bias()],
			'lamp' : 'off',
			'tolerance' : 0.5
		}
		
	def saveSettings(self, filepath):
		pickle.dump(self, open(filepath, 'wb'), pickle.HIGHEST_PROTOCOL)
		
	@staticmethod
	def loadSettings(filepath):
		return pickle.load(open(filepath, 'rb'))
		
	def updateSettings(self, dict):
		sett_keys = self.set_d.keys()
		for key in sett_keys:
			self.set_d[key] = dict[key]

if __name__ == '__main__':
	print "Pickle test:"
	oldsettings = Settings()
	
	print 'Old: ', oldsettings.toString()
	oldsettings.saveSettings('test')
		
	newsettings = Settings.loadSettings('test')
	newsettings.set_d['setPoint'] = 37
		