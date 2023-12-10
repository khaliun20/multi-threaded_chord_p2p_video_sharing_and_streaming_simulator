import socket
import json
import threading
import time
class ChordNode:
    def __init__(self, id, port, m, finger_table):
        self.id = id
        self.port = port
        self.m = m
        self.finger_table = finger_table #{key: (closest_to_key, port_id)} -> ex: {46: (99, 800)}

    def join_chord(self, existing_node_id, existing_node_port):        # Send a join request to the existing node 
        join_request = {'type': 'join', 'node_id': self.id, 'port': self.port}
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', existing_node_port))  # Assuming both nodes are on localhost
        print(f"Node 8 Connected to Node 4 on port {existing_node_port}")
        client_socket.sendall(json.dumps(join_request).encode('utf-8'))
        print(f"Node 8 Sent join Request to Node 4: {join_request}")
        join_response = json.loads(client_socket.recv(1024).decode('utf-8'))
        if join_response['type'] == 'accepted':
            print(f"Node 8 received join response from Node 4: {join_response}")
            # TODO:Update/Generate own finger table
            self.update_finger_tables(existing_node_id, existing_node_port)
            #print(f"Node 8 updated finger table: {self.finger_table}")
        client_socket.close()

    def update_finger_tables(self, existing_node_id, existing_node_port): 
        pass
       

    def process_join_request(self):
        # Process join request
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', self.port))
        server_socket.listen()
        print(f"Node {self.id} listening on port {self.port}")
        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=self.handle_connection, args=(client_socket,)).start()

    def closest_preceding_node(self, key):
    # Loop through the keys in finger_table in reverse order
        closest_key = None
        for id in reversed(self.finger_table.keys()):
            # If the key is between my_id and target_id
            if self.id < id < key:
                closest_key = id
                return self.finger_table[id]
        return self.finger_table[max(self.finger_table, key=int)]
  

    def find_predecessor(self, key):
        pass


    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', self.port))
        server_socket.listen()

        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=self.handle_connection, args=(client_socket,)).start()
    
    def handle_connection(self, client_socket):
        data = client_socket.recv(1024).decode('utf-8')
        request = json.loads(data)
        if request['type'] == 'join':
            node_id = request['node_id']
            node_port = request['port']
            print(f"Node {self.id} received join request from Node {node_id}")
           
            # Update own finger table
            for key, value in self.finger_table.items():
                #if received node, 8 is smaller than first entry in the table, 5 5 is smaller than own id (4)
                if self.id < key < node_id:
                    self.finger_table[key] = (node_id, node_port)
                    print(f"Node {self.id} updated finger table for key {key}: {self.finger_table}")
            # TODO: If no update needed for current node, then find the successor???
                

            join_response = {'type': 'accepted'}
            client_socket.sendall(json.dumps(join_response).encode('utf-8'))
            #print(f"Node {self.id} sent join response to Node {node_id}")
            
        client_socket.close()

if __name__ == "__main__":
    m = 4
    """ INIT NODE"""
    node4_init_finger_table = {}
    for i in range(0, m):
        entry_id = (4 + 2**i) % (2**m)
        node4_init_finger_table[entry_id] = (4, 40004)
    node4 = ChordNode(4, 40004, m, node4_init_finger_table)
    threading.Thread(target=node4.start_server).start()
    print(f"Node 4 Started server on port: {node4.port} with finger table: {node4.finger_table}")
    
    time.sleep(1)

    """ SECOND NODE JOIN """
    node8_init_finger_table = {}
    for i in range (m):
        entry_id = (8 + 2**i) % (2**m)
        node8_init_finger_table[entry_id] = (None,None)
    node8 = ChordNode(8, 40008, m,node8_init_finger_table)
    threading.Thread(target=node8.join_chord, args=(node4.id, node4.port)).start()
    threading.Thread(target=node8.start_server).start()
    
    

