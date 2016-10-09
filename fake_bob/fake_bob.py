import socket
import paho.mqtt.client as mqtt
import sys
import time

def on_connect(client, userdata, flags, rc):
	pass

def on_message(client, userdata, msg):
	print(msg.topic+' '+str(msg.payload))
	
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('broker.hivemq.com', 1883, 60)

while True:
	topic = 'obm/bob/192.168.137.137/values/status'
	data = '{"ip": "192.168.137.241", "data": {"hum": 81, "lamp": false, "tipoalim": true, "livbatt": 100, "temp": 22.5}, "name": "fake bob"}'
	client.publish(topic, data, retain=True)
	time.sleep(5)