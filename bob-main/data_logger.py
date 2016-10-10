import time

log_entry_format = '{0},{1:.1f},{2:.0f}\n'
log_filename = 'bob.log'

def addLogEntry(temp, hum):
	with open(log_filename, 'a') as log_file:
		log_entry = log_entry_format.format(time.strftime('%d/%m/%Y %H:%M:%S'), temp, hum)
		log_file.write(log_entry)
		log_file.close()
	
def readLog(value_type):
	with open(log_filename, 'r') as log_file:
		log_list = []
		stripped_lines = [line.strip('\n') for line in log_file]
		for line in stripped_lines:
			split_line = line.split(',')
			if value_type == 'temp':
				log_list.append({'date': split_line[0], 'value': split_line[1]})
			elif value_type == 'hum':
				log_list.append({'date': split_line[0], 'value': split_line[2]})
			else:
				print 'Unrecognized value type'
		return log_list
	
	
		
	
	
if __name__ == '__main__':
	import sys
	addLogEntry(time.strftime('%d/%m/%Y %H:%M:%S'), 36.5, 80)
	print readLog(sys.argv[1])