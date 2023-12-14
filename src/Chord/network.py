from utils import random_string, consistent_hash
from .static_chord import ChordNode

import argparse

PORT = 40000


class Network:
    """
    This class assumes there is a centralized system that initializes the network but is not used for routing,
    in a full chord implementation this would not be needed
    """
    def __init__(self, total_nodes, m):
        self.m = m
        self.nodes = self.create_nodes(total_nodes)
        self.ports = self.create_ports()
        self.create_tables()
        self.assign_successors()
        self.used_hashes = []

    def create_nodes(self, total_nodes):
        nodes = []
        for i in range(len(total_nodes)):
            id = consistent_hash(random_string(), 8)
            while id in self.used_hashes:
                id = consistent_hash(random_string(), 8)
            self.used_hashes.append(id)
            nodes.append(ChordNode(id, self.m))
        return nodes

    def create_ports(self):
        return [PORT + node_id.id for node_id in self.nodes]

    def create_tables(self):
        for node in self.nodes:
            node.initialize_finger_table(self.nodes, self.ports)



    def assign_successors(self):
        for i in range(len(self.nodes)):
            if i == len(self.nodes) - 1:
                successor = (self.nodes[0], self.ports[0])
            else:
                successor = (self.nodes[i + 1], self.ports[i + 1])
            self.nodes[i].successor = successor

    def upload_file(self, file_name):
        """
        add a file to the network
        """
        file_key = consistent_hash(file_name, 8)
        while file_key in self.used_hashes:
            file_key = consistent_hash(random_string(), 8)
        self.used_hashes.append(file_key)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chord Network')
    parser.add_argument('--total_nodes', type=int, default=6, help='total number of nodes in the network')
    parser.add_argument('--m', type=int, default=7, help='size of the ring')
    args = parser.parse_args()
    network = Network(args.total_nodes, args.m)
