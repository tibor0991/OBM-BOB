import os
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
	os.system('sudo ./bob_init.sh')
	
client = mqtt.Client()
client.on_message = on_message

try:
	client.connect('test.mosquitto.org', 1883, 60)
except:
	client.connect('broker.hivemq.com', 1883, 60)

client.subscribe('obm/bob/emergency-restart')

client.loop_forever()