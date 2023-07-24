"""
Example of using the rf24_mesh module to operate the nRF24L01 transceiver as
a Mesh network master node.
"""
from pyrf24 import RF24, RF24Network, RF24Mesh


radio = RF24(22, 0)
network = RF24Network(radio)
mesh = RF24Mesh(radio, network)
mesh.node_id = 0
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
            print(f"Received message {header.to_string()}")
except KeyboardInterrupt:
    print("powering down radio and exiting.")
    radio.power = False
