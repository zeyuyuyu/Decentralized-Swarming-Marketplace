import swarm_node
import random

class ReputationManager:
    def __init__(self):
        self.reputations = {}

    def update_reputation(self, node_id, score):
        if node_id not in self.reputations:
            self.reputations[node_id] = 0
        self.reputations[node_id] += score

    def get_reputation(self, node_id):
        if node_id not in self.reputations:
            return 0
        return self.reputations[node_id]

class DecentralizedMarketplace:
    def __init__(self):
        self.nodes = []
        self.reputation_manager = ReputationManager()

    def add_node(self, node):
        self.nodes.append(node)

    def execute_transaction(self, buyer_id, seller_id, item):
        buyer_node = next((n for n in self.nodes if n.id == buyer_id), None)
        seller_node = next((n for n in self.nodes if n.id == seller_id), None)
        if buyer_node is None or seller_node is None:
            return False

        if buyer_node.reputation < item.price:
            return False

        buyer_node.reputation -= item.price
        seller_node.reputation += item.price
        self.reputation_manager.update_reputation(buyer_id, -item.price)
        self.reputation_manager.update_reputation(seller_id, item.price)
        return True

class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price

if __name__ == "__main__":
    marketplace = DecentralizedMarketplace()
    node1 = swarm_node.SwarmNode("node1", 100)
    node2 = swarm_node.SwarmNode("node2", 50)
    node3 = swarm_node.SwarmNode("node3", 75)
    marketplace.add_node(node1)
    marketplace.add_node(node2)
    marketplace.add_node(node3)

    item1 = Item("Widget", 25)
    item2 = Item("Gadget", 50)

    print(f"Node 1 reputation: {marketplace.reputation_manager.get_reputation('node1')}")
    print(f"Node 2 reputation: {marketplace.reputation_manager.get_reputation('node2')}")
    print(f"Node 3 reputation: {marketplace.reputation_manager.get_reputation('node3')}")

    marketplace.execute_transaction("node1", "node2", item1)
    marketplace.execute_transaction("node2", "node3", item2)

    print(f"\nNode 1 reputation: {marketplace.reputation_manager.get_reputation('node1')}")
    print(f"Node 2 reputation: {marketplace.reputation_manager.get_reputation('node2')}")
    print(f"Node 3 reputation: {marketplace.reputation_manager.get_reputation('node3')}")