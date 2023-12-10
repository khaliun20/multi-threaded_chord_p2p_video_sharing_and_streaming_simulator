import socket
import json
import threading
from pprint import pprint
import time
PORT = 40000

class ChordNode:
    def __init__(self, node_id, port, m, successor=None):
        self.id = node_id
        self.port = port
        self.finger_table = {}
        self.m = m
        self.successor = successor

    def initialize_finger_table(self, nodes, ports):
        for i in range(self.m):
            entry_id = (self.id + 2**i) % (2**self.m)
            self.finger_table[entry_id] = self.find_value(nodes, ports, entry_id)
    
    def find_value(self, nodes, ports, key):
        for i in range(len(nodes)):
            successor_id = (nodes[i] + 2**self.m) % (2**self.m)
            next_successor_id = (nodes[(i + 1) % len(nodes)] + 2**self.m) % (2**self.m)

            if key <= successor_id or (key == successor_id and key == next_successor_id):
                return (nodes[i], ports[i])
            if key > nodes[-1]:
                return (nodes[0], ports[0])

        return (nodes[i], ports[i])

    def find_successor(self, key, origin_port):
        if self.id < key <= self.successor[0]:
            threading.Thread(target=self.send_message, args=(origin_port, {'found': self.successor[0]})).start()
            # TODO: send file to origin (ABR)
        else:
            preceding_node = self.closest_preceding_node(key)
            threading.Thread(target=self.send_message, args=(preceding_node[1], {'key': key, 'origin_port': origin_port})).start()
    
    
    def closest_preceding_node(self, key):
        for lookup in reversed(self.finger_table.keys()):
            node_id = self.finger_table[lookup][0]
            #print(f'checking finger table entry: {self.finger_table[lookup]} in range {self.id} - {key}')
            if self.id < key:
                if self.id < node_id < key:
                    return self.finger_table[lookup]
            else:  # Wrap-around case
                if node_id > self.id or node_id < key:
                    return self.finger_table[lookup]
        ret_tup = (self.id, self.port)
        return ret_tup

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', self.port))
        server_socket.listen()

        print(f"Node {self.id} listening on port {self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=self.handle_connection, args=(client_socket, addr)).start()

    def handle_connection(self, client_socket, addr):
        client_ip, client_port = addr
        data = client_socket.recv(1024).decode('utf-8')
        message = json.loads(data)
        if message.get('key'):
            print(f"Node {self.id} received message: {message['key']}")
            self.find_successor(key=message['key'], origin_port=message['origin_port']) 

        elif message.get('found'):
            print(f"Node {self.id} received found message. The file is in node: {message['found']}")
        client_socket.close()

    def send_message(self, dest_port, message):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', dest_port))
        client_socket.sendall(json.dumps(message).encode('utf-8'))
        print(f"Node {self.id} sent message to Node {dest_port - PORT}: {message}")
        client_socket.close()

if __name__ == "__main__":
    nodes = [16, 32, 45, 80, 96, 112]
    ports = [PORT + node_id for node_id in nodes]
    m = 7

    chord_nodes = []

    for i in range(len(nodes)):
        node_id = nodes[i]
        port = ports[i]
        if i == len(nodes) - 1:
            successor = (nodes[0], ports[0])
        else:
            successor = (nodes[i + 1], ports[i + 1])
        print(f"Node {node_id} successor is {successor}")

        chord_node = ChordNode(node_id, port, m, successor)
        chord_node.initialize_finger_table(nodes, ports)
        threading.Thread(target=chord_node.start_server).start()
        chord_nodes.append(chord_node)
        print(f"Node {chord_node.id} initialized finger table: {chord_node.finger_table}")

    time.sleep(2)

    chord_nodes[4].find_successor(92, chord_nodes[4].port)

  
    #chord_nodes[4].send_message(chord_node[4].closest_preceding_node()"'key':'42'")

#   The finger table for this DHT is: 
# {16: [32, 32, 32, 32, 32, 80, 80],
#  32: [45, 45, 45, 45, 80, 80, 96],
#  45: [80, 80, 80, 80, 80, 80, 112],
#  80: [96, 96, 96, 96, 96, 112, 16],
#  96: [112, 112, 112, 112, 112, 16, 32],
#  112: [16, 16, 16, 16, 16, 16, 80]}

# File location for file key 42 is at node 45 

# Query path for file 42 with origin node 80 : [80, 16, 32, 45]
# Query path for file 42 with origin node 96 : [96, 32, 45]
# Query path for file 42 with origin node 45 : [45]