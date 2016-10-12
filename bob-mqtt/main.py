import socket
import paho.mqtt.client as mqtt
import sys
sys.path.append('.') #this is the path relative to bob_init.sh
from common.sender import sender
import time
import json


id = sender.sendMessage('get ip')
log_request = 'obm/bob/{}/logs/request'.format(id)
log_reply = 'obm/bob/{}/logs/reply'.format(id)
lights = 'obm/bob/{}/lights'.format(id)
alarm_topic = 'obm/bob/{}/alarms'.format(id)
status_topic = 'obm/bob/{}/values/status'.format(id)

def on_message(client, userdata, msg):
	#print msg.topic, str(msg.payload)
	#process the lights command
	if msg.topic == lights:
		sender.sendMessage('set lamp '+str(msg.payload))
		
	if msg.topic == log_request:
		#take the start and the end
		#send it as 'get log _start_ _end_ '
		log_req_dict = json.loads(str(msg.payload))
		log_message = sender.sendMessage('request-log '+log_req_dict['value_type']+' '+log_req_dict['start']+' '+log_req_dict['end'])
		client.publish(log_reply, log_message)

client = mqtt.Client()
client.on_message = on_message

try:
	client.connect('test.mosquitto.org', 1883, 60)
except:
	client.connect('broker.hivemq.com', 1883, 60)

client.subscribe([(log_request,0), (lights,0)])
client.loop_start()
try:
	while True:
		#publishes the status JSON
		status_data = sender.sendMessage('get status')
		
		client.publish(status_topic, status_data, retain=True)
		
		#send alarms
		alarm_data = sender.sendMessage('get alarms')
		
		alarm_dict = {}
		alarm_codes = [str(key) for key in json.loads(alarm_data).keys()]
		
		if alarm_codes:
			alarm_dict['alarms'] = alarm_codes
			alarm_dict['ip'] = id
			client.publish(alarm_topic, json.dumps(alarm_dict))
		time.sleep(10)
except:
	print 'bob-mqtt interrupted'
finally:
	client.loop_stop()