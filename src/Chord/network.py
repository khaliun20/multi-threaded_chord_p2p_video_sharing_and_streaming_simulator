from utils import random_string, consistent_hash
from ChordNode import ChordNode

PORT = 40000


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


if __name__ == "__main__":
    create_nodes()
    ################ Placeholder ###############
    # Use consistent hashing and CLI
    nodes = [16, 32, 45, 80, 96, 112]
    ports = [PORT + node_id for node_id in nodes]
    m = 7
    node_with_video = 45
    file_hash = 42
    file_path = "video.mp4"
    #############################################

    for i in range(len(nodes)):
        node_id = nodes[i]
        port = ports[i]
        # Assigning immediate successors
        if i == len(nodes) - 1:
            successor = (nodes[0], ports[0])
        else:
            successor = (nodes[i + 1], ports[i + 1])

        if  node_id == node_with_video:
            chord_node = ChordNode_WithVideo(node_id, port, m, successor, file_hash, file_path)
            chord_node.play_video()
