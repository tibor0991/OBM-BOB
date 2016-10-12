from command import CommandInterface
from multiprocessing import Process
import json
import data_logger

class SystemCommand(CommandInterface, Process):
	def __init__(self, data):
		super(SystemCommand, self).__init__()
		self.data = data
		
	def processCommand(self, cmd):
		cmd_args = cmd.split()
		"""
		commands:
		get <argument>: returns a single value (as string) from the System
		get status: returns a JSON that will be parsed by external apps
		set <argument>: sets the value of a single value in the System
		reset-alarms: resets alarms
		"""
		if cmd_args[0] == 'get':
			if cmd_args[1] == 'status':
				json_dict = self.prepareStatusJSON()
				return json.dumps(json_dict)
			elif cmd_args[1] == 'alarms':
				return json.dumps(self.data['alarms'])
			else:
				return str(self.data[cmd_args[1]])
		elif cmd_args[0] == 'set':
			self.data[cmd_args[1]] = type(self.data[cmd_args[1]])(cmd_args[2])
			return str(self.data[cmd_args[1]])
		elif cmd_args[0] == 'reset-alarms':
			self.data['alarms'] = {}
			return 'OK'
		elif cmd_args[0] == 'request-log':
			value_type = cmd_args[1]
			start = cmd_args[2]+' '+cmd_args[3]
			end = cmd_args[4]+' '+cmd_args[5]
			log = data_logger.readLog(value_type, start, end)
			log_dict = { 'value_type' : value_type, 'log' : log}
			print len(json.dumps(log_dict))
			return json.dumps(log_dict)
		else:
			print 'Unrecognized command: '+cmd
			return 'ERROR'

	def prepareStatusJSON(self):
		json_keys = ['name', 'ip']
		data_keys = ['temp', 'hum', 'lamp']
		data_dict = {}
		for d_key in data_keys:
			data_dict[d_key] = self.data[d_key]
		data_dict['temp'] = '%.1f' % data_dict['temp']
		data_dict['hum'] = int(data_dict['hum'])
		#dummy keys
		dummy_keys = { 'tipoalim': True, 'livbatt': 100}
		data_dict.update(dummy_keys)
		
		json_dict = {}
		for j_key in json_keys:
			json_dict[j_key] = self.data[j_key]
		json_dict['data'] = data_dict
		return json_dict