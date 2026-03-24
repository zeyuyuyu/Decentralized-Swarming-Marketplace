import random
import time

class SwarmNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.neighbors = []
        self.task_queue = []
        self.consensus_state = 'idle'
        self.consensus_round = 0
        self.consensus_vote = None

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def submit_task(self, task):
        self.task_queue.append(task)
        self.initiate_consensus()

    def initiate_consensus(self):
        if self.consensus_state == 'idle':
            self.consensus_state = 'proposed'
            self.consensus_round += 1
            self.consensus_vote = random.choice(['accept', 'reject'])
            self.broadcast_vote()

    def broadcast_vote(self):
        for neighbor in self.neighbors:
            neighbor.receive_vote(self.node_id, self.consensus_round, self.consensus_vote)

    def receive_vote(self, sender_id, round_num, vote):
        if round_num == self.consensus_round:
            self.consensus_vote = vote
            self.tally_votes()

    def tally_votes(self):
        accept_count = 0
        reject_count = 0
        for neighbor in self.neighbors:
            if neighbor.consensus_vote == 'accept':
                accept_count += 1
            elif neighbor.consensus_vote == 'reject':
                reject_count += 1

        if accept_count > reject_count:
            self.consensus_state = 'accepted'
            self.execute_task()
        else:
            self.consensus_state = 'rejected'
            self.task_queue.pop(0)

    def execute_task(self):
        task = self.task_queue.pop(0)
        print(f'Executing task: {task}')
        time.sleep(2)
        print(f'Task {task} completed.')
