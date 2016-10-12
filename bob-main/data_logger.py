import time
import datetime

log_entry_format = '{0},{1:.1f},{2:.0f}\n'
log_filename = 'bob.log'

def addLogEntry(temp, hum):
	with open(log_filename, 'a') as log_file:
		log_entry = log_entry_format.format(time.strftime('%d/%m/%Y %H:%M:%S'), temp, hum)
		log_file.write(log_entry)
		log_file.close()
	
def readLog(value_type, start, end):
	with open(log_filename, 'r') as log_file:
		log_list = []
		stripped_lines = [line.strip('\n') for line in log_file]
		start_date = datetime.datetime.strptime(start, '%d/%m/%Y %H:%M:%S')
		end_date = datetime.datetime.strptime(end, '%d/%m/%Y %H:%M:%S')
		if value_type == 'temp':
			value_column = 1
		elif value_type == 'hum':
			value_column = 2
		else:
			print 'Unrecognized value type'
			return log_list
			
		for line in stripped_lines:
			split_line = line.split(',')
			line_date = datetime.datetime.strptime(split_line[0], '%d/%m/%Y %H:%M:%S')
			if start_date <= line_date <= end_date:
				log_list.append({'date': split_line[0], 'value': split_line[value_column]})
		return log_list
	
	
		
	
	
if __name__ == '__main__':
	import sys
	addLogEntry(time.strftime('%d/%m/%Y %H:%M:%S'), 36.5, 80)
	print readLog(sys.argv[1])