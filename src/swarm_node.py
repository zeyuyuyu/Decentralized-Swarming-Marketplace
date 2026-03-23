import random
import time
import network

class SwarmNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.neighbors = []
        self.mesh_network = MeshNetwork(self)

    def connect_to_neighbor(self, neighbor_node):
        self.neighbors.append(neighbor_node)
        neighbor_node.neighbors.append(self)
        self.mesh_network.add_connection(neighbor_node.mesh_network)

    def broadcast_message(self, message):
        for neighbor in self.neighbors:
            neighbor.mesh_network.receive_message(message)

class MeshNetwork:
    def __init__(self, node):
        self.node = node
        self.connections = []
        self.message_queue = []

    def add_connection(self, other_network):
        self.connections.append(other_network)
        other_network.connections.append(self)

    def receive_message(self, message):
        self.message_queue.append(message)
        self.process_messages()

    def process_messages(self):
        while self.message_queue:
            message = self.message_queue.pop(0)
            self.node.handle_message(message)
            for connection in self.connections:
                connection.receive_message(message)

    def run(self):
        while True:
            self.process_messages()
            time.sleep(random.uniform(0.1, 0.5))
