import socket
import json
import threading
import time


class ChordNode:
    def __init__(self, node_id, port, successor=None):
        self.id = node_id
        self.port = port
        self.finger_table = {}
        self.successor = successor
        self.videos = []

    
    # Note: I think this is able to identify a file between 16 and 112, not 0 and 2^7. 
    def find_successor(self, key, origin_port):
        if self.id < key <= self.successor.id:
            threading.Thread(target=self.send_message, args=(origin_port, {'found': (self.successor.id, self.successor.port)})).start()
            # TODO: send file to origin (ABR)
            # self.video_play()
            # self.send_video_result(origin_port)
            # send.send_video(self, origin_port)
        else:
            preceding_node = self.closest_preceding_node(key)
            threading.Thread(target=self.send_message, args=(preceding_node[1], {'key': key, 'origin_port': origin_port})).start()

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
        client_ip, client_port = addr
        while True: 
            data = client_socket.recv(2048).decode('utf-8')
            if not data:
                break
            #process_video(data)
            message = json.loads(data)
            if message.get('key'):
                print(f"Node {self.id} received message: {message['key']}")
                self.find_successor(key=message['key'], origin_port=message['origin_port']) 

            elif message.get('found'):
                print(f"Node {self.id} received found message. The file is in node: {message['found'][0]} with port id {message['found'][1]}")
                self.send_message(message['found'][1], {"request_video": 'src/ABR/videos/manifest-1.json',
                                                        "origin_port": self.port})
                print(f"Node {self.id} sent video request message to Node {message['found'][1]}")

            elif message.get('request_video'):
                sabre_result = self.send_video(video_file = message['request_video'])
                self.send_message(message['origin_port'], sabre_result)
                # send the result of running sabre.py to Marcus's flask app
                self.send_message(50001, sabre_result)

            else:
                pass

        client_socket.close()
    
    # Send message to other nodes. Sends message and close the connection asap
    def send_message(self, dest_port, message, http=False):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', dest_port))
        client_socket.sendall(json.dumps(message).encode('utf-8'))
        print(f"Node {self.id} sent message to Node {dest_port - 40000}: {message}")
        client_socket.close()
        
    def send_video(self, video_file = None):
        from ..ABR.sabre import run_sabre
        from ..ABR.sabreArgs import SabreArgs
        sabre_args = SabreArgs()
        if video_file:
            sabre_args.movie = video_file
        result = run_sabre(sabre_args)
        return result

    def produce_json_to_send(self):
        pass
    
    def play_video(self, dest_port):
        pass


   