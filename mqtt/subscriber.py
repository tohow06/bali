import paho.mqtt.client as mqtt
import json

MQTT_SERVER = "192.168.100.13"
MQTT_PORT = 1883
MQTT_ALIVE = 60
MQTT_TOPIC = "msg/info"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    # print(f"{msg.topic}: {msg.payload.decode('utf-8')}"
    print(
        f"{msg.topic} - data1: {json.loads(msg.payload)['data1']}, data2: {json.loads(msg.payload)['data2']}"
    )


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)
mqtt_client.loop_forever()
