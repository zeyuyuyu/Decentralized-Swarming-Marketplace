import time
import random
import hashlib

class SwarmNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.reputation = 100
        self.transaction_history = []

    def perform_transaction(self, other_node, amount):
        if self.reputation >= amount:
            self.reputation -= amount
            other_node.reputation += amount
            transaction = {
                'from': self.node_id,
                'to': other_node.node_id,
                'amount': amount,
                'timestamp': time.time()
            }
            self.transaction_history.append(transaction)
            other_node.transaction_history.append(transaction)
            return True
        else:
            return False

    def calculate_reputation(self):
        total_transactions = len(self.transaction_history)
        positive_transactions = 0
        for transaction in self.transaction_history:
            if transaction['to'] == self.node_id:
                positive_transactions += 1
        self.reputation = int(positive_transactions / total_transactions * 100)

    def generate_trust_score(self, other_node):
        trust_score = 0
        for transaction in other_node.transaction_history:
            if transaction['to'] == other_node.node_id:
                trust_score += 1
        return trust_score
