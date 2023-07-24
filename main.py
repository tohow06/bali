import json
import random
import struct

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from pyrf24 import (
    RF24,
    RF24_PA_HIGH,
    RF24_PA_LOW,
    RF24_PA_MAX,
    RF24_PA_MIN,
    RF24Mesh,
    RF24Network,
)

MQTT_SERVER = "0.0.0.0"
MQTT_PORT = 1883
MQTT_ALIVE = 60
MQTT_TOPIC = "sensor/vibration"


def publish_to_red(id, value):
    pp = {"node_id": id, "value": value}
    # 發布一則 MQTT 訊息
    publish.single(
        topic=MQTT_TOPIC, payload=json.dumps(pp), hostname=MQTT_SERVER, port=MQTT_PORT
    )


radio = RF24(22, 0, 1000000)
network = RF24Network(radio)
mesh = RF24Mesh(radio, network)
mesh.node_id = 0
radio.begin()
radio.set_pa_level(RF24_PA_MIN, 0)

if not mesh.begin():
    # if mesh.begin() returns false for a master node,
    # then radio.begin() returned false.
    raise OSError("Radio hardware not responding.")
radio.print_pretty_details()

try:
    while True:
        mesh.update()
        mesh.dhcp()

        while network.available():
            header, payload = network.read()
            data = int.from_bytes(payload, "little")
            from_node_id = mesh.get_node_id(header.from_node)
            print(f"Received message {header.to_string()} data:{data}")
            print(f"from_node_id = {from_node_id}")
            publish_to_red(from_node_id, data)

except KeyboardInterrupt:
    print("powering down radio and exiting.")
    radio.power = False
