
############## Pub ####################
import paho.mqtt.client as mqtt

# *********************************************************************
# MQTT_tb Config

MQTT_tb_SERVER = "172.16.10.200"
MQTT_tb_PORT = 1883
MQTT_tb_ALIVE = 60
MQTT_tb_TOPIC = "v1/devices/me/telemetry"
ACCESS_TOKEN = "THISISMYACCESSTOKEN"
# *********************************************************************

# *********************************************************************
# MQTT Config

MQTT_SERVER = "172.16.11.48"
MQTT_PORT = 1883
MQTT_ALIVE = 60
MQTT_TOPIC_Temperature = "sensor/temperature"
MQTT_TOPIC_Humidity = "sensor/humidity"
MQTT_TOPIC_Light = "sensor/light"
# *********************************************************************

mqtt_tb_client = mqtt.Client()
mqtt_tb_client.username_pw_set(ACCESS_TOKEN)
mqtt_tb_client.connect(MQTT_tb_SERVER, MQTT_tb_PORT, MQTT_tb_ALIVE)
mqtt_tb_client.loop_start()

myHumidity = 0
myTemperature = 0
myLight = 0

def on_message(client, userdata, message):
        print("Message Recieved: "+message.payload.decode())
        print("Received message '" + str(message.payload) + "' on topic '"
                + message.topic + "' with QoS " + str(message.qos))

        global myTemperature, myHumidity, myLight
        print(time.asctime( time.localtime(time.time()) ))
        if message.topic == "sensor/temperature":
                myTemperature = message.payload.decode()
        elif message.topic == "sensor/humidity":
                myHumidity = message.payload.decode()
        elif message.topic == "sensor/light":
                myLight = message.payload.decode()
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)
mqtt_client.on_message = on_message
mqtt_client.subscribe(MQTT_TOPIC_Temperature, qos=2)
mqtt_client.subscribe(MQTT_TOPIC_Humidity, qos=2)
mqtt_client.subscribe(MQTT_TOPIC_Light, qos=2)
mqtt_client.loop_start()

import time
import json
import random
import math

nowTime = time.time()

try:
        while True:
                
                if (time.time() - nowTime) > 10:
                        myTime = time.asctime( time.localtime(time.time()) )
                        myVal = 20*math.sin(2*math.pi*(1/(60))*time.time())+5*math.sin(2*math.pi*(3/60)*time.time())
        #               print(myVal)
                        payload = {"time": myTime, "temperature": myTemperature, "humidity": myHumidity, "light": myLight}
                        # print(payload)
                        mqtt_tb_client.publish(topic=MQTT_tb_TOPIC, payload=json.dumps(payload), qos=2)
                        nowTime = time.time()


except KeyboardInterrupt:
        pass

mqtt_client.loop_stop()
mqtt_client.disconnect()
