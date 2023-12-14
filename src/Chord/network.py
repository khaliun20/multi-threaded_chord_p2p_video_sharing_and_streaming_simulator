from .utils import random_string, consistent_hash
from .static_chord import ChordNode
import threading
import time

import argparse

PORT = 40000


class Network:
    """
    This class assumes there is a centralized system that initializes the network but is not used for routing,
    in a full chord implementation this would not be needed
    """
    def __init__(self, total_nodes, m):
        self.m = m
        self.used_hashes = []
        self.nodes = self.create_nodes(total_nodes)
        self.node_ids = [node.id for node in self.nodes]
        self.ports = self.create_ports()
        self.create_tables()
        self.assign_successors()
        self.start_nodes()
        [print(node.finger_table) for node in self.nodes]

    def create_nodes(self, total_nodes):
        nodes = []
        for i in range(total_nodes):
            node_id = consistent_hash(random_string(), self.m)
            while node_id in self.used_hashes:
                node_id = consistent_hash(random_string(), self.m)
            self.used_hashes.append(node_id)
            nodes.append(ChordNode(node_id, PORT + node_id, self.m))
        nodes.sort(key=lambda x: x.id)
        return nodes

    def create_ports(self):
        return [PORT + node_id.id for node_id in self.nodes]

    def create_tables(self):
        for k in range(len(self.node_ids)):
            for i in range(self.m):
                entry_id = (self.node_ids[k] + 2 ** i) % (2 ** self.m)
                self.nodes[k].finger_table[entry_id] = self.find_value(entry_id)
    def find_value(self, key):
        for node_id, port in zip(self.node_ids, self.ports):
            if node_id >= key:
                return node_id, port
        # If not found, return the first node (wrap-around)
        return self.node_ids[0], self.ports[0]

    def assign_successors(self):
        for i in range(len(self.nodes)):
            if i == len(self.nodes) - 1:
                successor = self.nodes[0]
            else:
                successor = self.nodes[i + 1]
            self.nodes[i].successor = successor

    def start_nodes(self):
        for node in self.nodes:
            threading.Thread(target=node.start_server).start()

    def hash_file(self, filename):
        file_key = consistent_hash(filename, self.m)
        max_key = self.node_ids[-1]
        min_key = self.node_ids[0]
        # no more bug!
        while file_key in self.used_hashes and file_key > max_key and file_key < min_key:
            file_key = consistent_hash(random_string(), self.m)
        self.used_hashes.append(file_key)
        return file_key

    def find_file(self, filename):
        finder = self.nodes[1]
        hashed_file = self.hash_file(filename)
        finder.find_successor(hashed_file, finder.port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chord Network')
    parser.add_argument('--total_nodes', type=int, default=6, help='total number of nodes in the network')
    parser.add_argument('--m', type=int, default=7, help='size of the ring')
    args = parser.parse_args()
    network = Network(args.total_nodes, args.m)
    time.sleep(2)
    network.find_file("manifest")
