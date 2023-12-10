import socket
import json
import threading

class ChordNode:
    def __init__(self, id, port, m, successor = None):
        self.id = id
        self.port = port

        self.m = m
        # self.finger_table = [None] * m
        self.finger_table = [{}] * m # {'ID': _,'port': _}
        
        if successor == None:
            raise NotImplementedError()
        
        self.successor = successor

        # self.predecessor = None
    
    # def create_finger_table(self): 
    #     pass

    # def find_predecessor(self, key):
    #     # Simplified find_predecessor method
    #     pass

    def closest_preceding_node(self, id: int):
        """ Search the finger table for the highest predecessor of id.
            Note: assumes that there is no collision between finger_table[i] and id."""
        for i in range(self.m, 1, -1):
            if (self.finger_table[i]['ID'] in range(self.id, id)): 
                return self.finger_table[i] # dictionary 
        return {'ID' : self.id, 'port' : self.port}
    
    def find_successor(self, id: int):
        """Node n to find the successor of id"""
        if self.id < id <= self.successor['ID']:
            return self.successor #TODO: Define this
        else:
            preceding_node = self.closest_preceding_node(id)    
            # return dict: {'successor': response['sucessor'] , 'sucessor_port': response['sucessor_port']}
            return self.request_successor(preceding_node['port'], id) 

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', self.port))
        server_socket.listen()

        print(f"Node {self.id} listening on port {self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=self.handle_connection, args=(client_socket,)).start()

    def request_successor(self, n_port_id: int,  key: int): 
        """Request the successor from node with node.id = n"""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', n_port_id))
        request = b"""{"type": "find_successor", "key": {}""".format(key)
        client_socket.sendall(request) #expects a response with {'successor' : successor.node_id}
        response = json.loads(client_socket.recv(1024).decode('utf-8'))
        # return dictionary of successor_node_id, successor_port_id
        return {'ID': response['sucessor'] , 'port': response['sucessor_port']}

    def handle_connection(self, client_socket):
        data = client_socket.recv(1024).decode('utf-8')
    
        request = json.loads(data)

        if request['type'] == 'get_video':
            response = request['video_id']
            client_socket.send(json.dumps(response).encode('utf-8'))

        if request['type'] == 'find_successor':
            key = request['key']
            successor = self.find_successor(key) # dictionary
            response = {'ID': successor['ID'] if successor else None,
                        'port': successor['port'] if successor else None}
            client_socket.send(json.dumps(response).encode('utf-8'))

        client_socket.close()

    # def notify(self, new_node):
    #     # Simplified notify method
    #     pass

    # def join(self, existing_node):
    #     # Join the Chord ring by updating finger table entries
    #     predecessor = existing_node.find_predecessor(self.node_id)
    #     self.finger_table[0] = existing_node.find_successor(self.node_id)

    #     for i in range(1, self.m):
    #         entry_id = (self.node_id + 2**i) % (2**self.m)
    #         self.finger_table[i] = existing_node.find_successor(entry_id)

    #     # Notify existing nodes about the new node
    #     existing_node.notify(self)

# Example Usage
if __name__ == "__main__":
    port4 = 40000
    port8 = 60000
    node4 = ChordNode(4, port4, m=2 ,successor={'ID': 8, 'port': 60000})
    node8 = ChordNode(8, port8, m=2 ,successor={'ID': 4, 'port': 40000})
    
    threading.Thread(target=node4.start_server).start()
    threading.Thread(target=node8.start_server).start()

# def create_chord_node(node_id, existing_node):
#     new_node = ChordNode(node_id)
#     threading.Thread(target=new_node.start_server).start()
#     new_node.join(existing_node)
#     return new_node
#     new_node = create_chord_node(1, node8)

