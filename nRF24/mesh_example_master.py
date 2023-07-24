"""
Example of using the rf24_mesh module to operate the nRF24L01 transceiver as
a Mesh network master node.
"""
import struct
from pyrf24 import RF24, RF24Network, RF24Mesh
from pyrf24 import RF24_PA_MIN, RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX

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
            print(f"Received message {header.to_string()} data:{data}")
            print(f"from_node_id = {mesh.get_node_id(header.from_node)}")

except KeyboardInterrupt:
    print("powering down radio and exiting.")
    radio.power = False
