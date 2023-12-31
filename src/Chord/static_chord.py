import socket
import json
import threading
import time

class ChordNode:
    def __init__(self, node_id, port, m=7, successor=None):
        self.id = node_id
        self.port = port
        self.finger_table = {}
        self.successor = successor
        self.videos = []
        self.m = m 

    def compute_relative_id(self, id):
        "treat the current node as 0, and find the relative ID of id on the circle"
        relative_id = (id - self.id)
        if relative_id < 0:
            relative_id += 2**self.m
        return relative_id

    
    def find_successor(self, key, origin_port, filename):
        if self.compute_relative_id(self.id) < self.compute_relative_id(key) <= self.compute_relative_id(self.successor.id):
            threading.Thread(target=self.send_message, args=(origin_port, {'found': (self.successor.id, self.successor.port, filename)})).start()
        else:
            preceding_node = self.closest_preceding_node(key)
            threading.Thread(target=self.send_message, args=(preceding_node[1], {'key': key, 'origin_port': origin_port, 'file': filename})).start()
    
    def closest_preceding_node(self, key):
        for lookup in reversed(self.finger_table.keys()):
            node_id = self.finger_table[lookup][0]
            # print(f'checking finger table entry: {self.finger_table[lookup]} in range {self.id} - {key}')
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

        # Lets node severs run forever
        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=self.handle_connection, args=(client_socket, addr)).start()

    # Once the communication is established, handle the connection and close it asap 
    def handle_connection(self, client_socket, addr):
        while True: 
            try:
                data = client_socket.recv(2048).decode('utf-8')
            except (socket.error, ConnectionResetError) as e:
                print(f"Error receiving data from the client: {e}")
                break

            if not data:
                break
            
            try:
                message = json.loads(data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON data: {e}")
                break
            
            if message.get('key'):
                print(f"Node {self.id} received message: {message['key']}")
                self.find_successor(key=message['key'], origin_port=message['origin_port'], filename =message['file']) 

            elif message.get('found'):
                print(f"Node {self.id} received found message. The file is in node: {message['found'][0]} with port id {message['found'][1]}")
                self.send_message(message['found'][1], {"request_video": message['found'][2],
                                                        "origin_port": self.port})
                print(f"Node {self.id} sent video request message to Node {message['found'][1]}")

            elif message.get('request_video'):
                sabre_result = self.send_video(video_file = message['request_video'])
                self.send_message(message['origin_port'], sabre_result)
                # send the result of running sabre.py to Marcus's flask app
                self.send_message(50002, sabre_result)

            else:
                pass
            
        client_socket.close()
    
    # Send message to other nodes. Sends message and close the connection asap
    def send_message(self, dest_port, message, http=False):
        print(f"Node {self.id} attempts to sent message to Node {dest_port - 40000}: {message}")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: 
            client_socket.connect(('localhost', dest_port))
            client_socket.sendall(json.dumps(message).encode('utf-8'))
            print(f"Node {self.id} sent message to Node {dest_port - 40000}: {message}")
        except (socket.error, ConnectionResetError) as e:
            print(f"Connection to port {dest_port} refused. Server not available. Exception {e} thrown")
        finally:
            client_socket.close()
        
    def send_video(self, video_file = None):
        from ..ABR.sabre import run_sabre
        from ..ABR.sabreArgs import SabreArgs
        sabre_args = SabreArgs()
        if video_file:
            sabre_args.movie = video_file
        result = run_sabre(sabre_args)
        return result


   