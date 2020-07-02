#auther : akash
import netifaces
import paho.mqtt.client as mqtt
import time
import requests
from bs4 import BeautifulSoup

a=netifaces.interfaces()
prev =0
broker="test.mosquitto.org"  # Or any MQTT brocker
port=1883                    # MQTT port
client_name="clientName"     # Client Name
pub_topic="secret"           # It should be Unique Other wise anyone with this topic will get your ip .
client = mqtt.Client(client_name)
client.connect(broker, port, 60)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish (client,userdata,result):
	print("data published : "+str(message))
	
while True:
	URL = 'https://whatismyipaddress.com/ds-check'
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, 'html.parser')
	results = soup.find(id='ipv6')
	d=results.prettify().splitlines()
	print("http://["+d[2].strip()+"]:8096")
	f="http://["+d[2].strip()+"]:8096"
	client.publish(pub_topic,str(f))
	for i in a:
		addrs=netifaces.ifaddresses(i)
		b=addrs[netifaces.AF_INET6]
		c = b[0]
		if len(c["addr"]) == 38:
			d = "http://["+c["addr"]+"]:8096"
			print(d)
			client.publish(pub_topic,str(d))
			time.sleep(.5)
			client.on_publish = on_publish
			time.sleep(.5)
			prev = c["addr"]
	time.sleep(5)

client.loop_forever()

