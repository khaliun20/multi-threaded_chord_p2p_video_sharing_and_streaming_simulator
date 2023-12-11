import socket
import json
import threading
from pprint import pprint
import time
import subprocess





PORT = 40000

class Video:
    def __init__(self, file_hash, file_path):
        self.file_hash = file_hash
        self.file_path = file_path


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
    
    # Populate finger table of new node
    def find_value(self, nodes, ports, key):
        for i in range(len(nodes)):
            successor_id = (nodes[i] + 2**self.m) % (2**self.m)
            if key <= successor_id:
                return (nodes[i], ports[i])
            if key > nodes[-1]:
                return (nodes[0], ports[0])
        return (nodes[i], ports[i])
    
    # Note: I think this is able to identify a file between 16 and 112, not 0 and 2^7. 
    def find_successor(self, key, origin_port):
        if self.id < key <= self.successor[0]:
            threading.Thread(target=self.send_message, args=(origin_port, {'found': self.successor[0]})).start()
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

        # Lets node severs run forever
        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=self.handle_connection, args=(client_socket, addr)).start()

    # Once the communication is established, handle the connection and close it asap 
    def handle_connection(self, client_socket, addr):
        client_ip, client_port = addr
        while True: 
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            message = json.loads(data)
            if message.get('key'):
                print(f"Node {self.id} received message: {message['key']}")
                self.find_successor(key=message['key'], origin_port=message['origin_port']) 

            elif message.get('found'):
                print(f"Node {self.id} received found message. The file is in node: {message['found']}")

            elif message.get('video'): 
                # process the vdeo (data) 
                pass
            else:
                pass
            
        client_socket.close()
    
    # Send message to other nodes. Sends message and close the connection asap
    def send_message(self, dest_port, message):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', dest_port))
        client_socket.sendall(json.dumps(message).encode('utf-8'))
        print(f"Node {self.id} sent message to Node {dest_port - PORT}: {message}")
        client_socket.close()

class ChordNode_WithVideo(ChordNode):
    def __init__(self, node_id, port, m, successor=None, video_hash = None, video_path = None):
        super().__init__(node_id, port, m, successor)

        self.video = Video(video_hash, video_path)
        
    def play_video(self):
        try:
            command_to_run = ["python3", "../ABR/sabre.py"]
            result = subprocess.run(command_to_run, capture_output=True, text=True)
            if result.returncode == 0:
                print(result.stdout)
            else:
                print(f"Error running subprocess. Exit code: {result.returncode}")
                print(result.stderr)


        except Exception as e:
            print(e)

    def produce_json_to_send(self):
        pass
    
    def send_video(self, dest_port):
        # filepath = ABR.Chord
        # create socket connection 
        # send video file to dest_port

        pass



if __name__ == "__main__":
    
    ################ Placeholder ###############
    # We can make the nodes CLI later on
    nodes = [16, 32, 45, 80, 96, 112]
    ports = [PORT + node_id for node_id in nodes]
    m = 7
    node_with_video = 45
    file_hash = 42
    file_path = "video.mp4"
    ##############################################


    chord_nodes = []

    # Initialize nodes
    for i in range(len(nodes)):
        node_id = nodes[i]
        port = ports[i]
        if i == len(nodes) - 1:
            successor = (nodes[0], ports[0])
        else:
            successor = (nodes[i + 1], ports[i + 1])
        print(f"Node {node_id} successor is {successor}")
        
        # Pick the node with the file. Here we pick node 80
        if node_id == node_with_video:
            chord_node = ChordNode_WithVideo(node_id, port, m, successor, file_hash, file_path)
            print(chord_node.video.file_path)
            print(chord_node.video.file_hash)
            chord_node.play_video()

            
        else:
            chord_node = ChordNode(node_id, port, m, successor)
        chord_node.initialize_finger_table(nodes, ports)
        print(f"Node {chord_node.id} initialized finger table: {chord_node.finger_table}")
        
        # Start nodes
        threading.Thread(target=chord_node.start_server).start()
        chord_nodes.append(chord_node)
    

    time.sleep(2)

    # Simulation starts here
    chord_nodes[5].find_successor(file_hash, chord_nodes[5].port)

   