import json
import random
import time
import sys
import logging

log_dict = {}

log_dict['ip'] = '192.168.1.2'
log_dict['value_type'] = 'temp'
log_dict['log'] = []

for i in range(0, int(sys.argv[1])):
	entry_dict = {}
	entry_dict['date'] = time.strftime('%d/%m/%y')
	entry_dict['time'] = time.strftime('%H:%M:%S')
	entry_dict['value'] = '%.1f' % (36.5+(random.random() * 6 - 3))
	log_dict['log'].append(entry_dict)

test_log = open('bob'+sys.argv[1]+'.log', 'a')
test_log.write(json.dumps(log_dict))
test_log.close()