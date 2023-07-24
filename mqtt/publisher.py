import paho.mqtt.client as mqtt
import json
import random

MQTT_SERVER = "192.168.100.13"
MQTT_PORT = 1883
MQTT_ALIVE = 60
MQTT_TOPIC = "msg/info"

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)


def publish():
    payload = {"data1": random.random(), "data2": random.random()}
    print(f"payload: {payload}")
    mqtt_client.publish(MQTT_TOPIC, json.dumps(payload), qos=1)
    mqtt_client.loop(2, 10)


no = 1

while no < 51:
    publish()
    no = no + 1
