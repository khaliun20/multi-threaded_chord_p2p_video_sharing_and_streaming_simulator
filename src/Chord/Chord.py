import socket
import json
import threading

class ChordNode:
    def __init__(self, id, m):
        self.id = id
        self.m = m
        self.finger_table = [None] * m
        self.successor = self.finger_table[0]
        self.predecessor = None

    def create_finger_table(self):

    def find_predecessor(self, key):
        # Simplified find_predecessor method
        pass

    def find_successor(self, id: int):
        if self.id < id <= self.successor:
            return self.successor
        else:
            n = self.closest_preceding_node(id)
            # Assuming a method for a remote procedure call to find_successor on node n
            return n.find_successor(id)
        # Simplified find_successor method
        pass

    def notify(self, new_node):
        # Simplified notify method
        pass

    def join(self, existing_node):
        # Join the Chord ring by updating finger table entries
        predecessor = existing_node.find_predecessor(self.node_id)
        self.finger_table[0] = existing_node.find_successor(self.node_id)

        for i in range(1, self.m):
            entry_id = (self.node_id + 2**i) % (2**self.m)
            self.finger_table[i] = existing_node.find_successor(entry_id)

        # Notify existing nodes about the new node
        existing_node.notify(self)

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', self.node_id))
        server_socket.listen()

        print(f"Node {self.node_id} listening on port {self.node_id}")

        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=self.handle_connection, args=(client_socket,)).start()

    def handle_connection(self, client_socket):
        data = client_socket.recv(1024).decode('utf-8')
        request = json.loads(data)

        if request['type'] == 'find_successor':
            key = request['key']
            successor = self.find_successor(key)
            response = {'successor': successor.node_id if successor else None}
            client_socket.send(json.dumps(response).encode('utf-8'))

        client_socket.close()

# Function to create a new Chord node when a new node joins
def create_chord_node(node_id, existing_node):
    new_node = ChordNode(node_id)
    threading.Thread(target=new_node.start_server).start()
    new_node.join(existing_node)
    return new_node

# Example Usage
if __name__ == "__main__":
    node4 = ChordNode(4)
    node8 = ChordNode(8)

    threading.Thread(target=node4.start_server).start()
    threading.Thread(target=node8.start_server).start()

    new_node = create_chord_node(1, node8)

    # Print the Chord ring
    print_ring([node4, node8, new_node])
