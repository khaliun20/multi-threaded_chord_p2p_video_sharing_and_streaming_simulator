from utils import random_string, consistent_hash
from ChordNode import ChordNode

class Network:
    """
    This class assumes there is a centralized system that initializes the network but is not used for routing,
    in a full chord implementation this would not be needed
    """
    def __init__(self, total_nodes, m):
        self.total_nodes = total_nodes
        self.m = m
        self.nodes = self.create_nodes()
        self.create_tables()
        self.used_hashes = []


    def create_nodes(self):
        nodes = []
        for i in range(self.total_nodes):
            id = consistent_hash(random_string(), 8)
            while id in self.used_hashes:
                id = consistent_hash(random_string(), 8)
            self.used_hashes.append(id)
            nodes.append(ChordNode(id, self.m))
        return nodes

    def create_tables(self):
        for node in self.nodes:
            node.create_finger_table()

    def upload_file(self, file_name):
        """
        add a file to the network
        """
        file_key = consistent_hash(file_name, 8)
        while file_key in self.used_hashes:
            file_key = consistent_hash(random_string(), 8)
        self.used_hashes.append(file_key)


        pass

