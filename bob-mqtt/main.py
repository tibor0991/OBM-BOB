import socket
import paho.mqtt.client as mqtt
import sys
sys.path.append('.') #this is the path relative to bob_init.sh
from common.sender import sender
import time
import json

def on_message(client, userdata, msg):
	print(msg.topic+' '+str(msg.payload))

log_request = 'obm/bob/+/logs/request'
log_reply = 'obm/bob/{}/logs/reply'

client = mqtt.Client()
client.on_message = on_message

client.connect('broker.hivemq.com', 1883, 60)

client.subscribe(log_request)


	
	

while True:
	id = sender.sendMessage('get ip')
	#publishes the status JSON
	status_data = sender.sendMessage('get status')
	status_topic = 'obm/bob/{}/values/status'.format(id)
	client.publish(status_topic, status_data, retain=True)
	
	#send alarms
	alarm_data = sender.sendMessage('get alarms')
	alarm_topic = 'obm/bob/{}/alarms'.format(id)
	alarm_dict = {}
	alarm_codes = json.loads(alarm_data).keys()
	if not alarm_codes:
		alarm_dict['alarms'] = alarm_codes
		alarm_dict['ip'] = id
		client.publish(alarm_topic, json.dumps(alarm_dict))
	
	#wait a message on the log/request channel
	
	
	
	
	
	time.sleep(10)