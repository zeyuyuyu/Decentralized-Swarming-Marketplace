import random
import time
from typing import List, Tuple

class SwarmNode:
    def __init__(self, node_id: str, location: Tuple[float, float]):
        self.node_id = node_id
        self.location = location
        self.neighbors = []
        self.tasks = []
        self.available = True

    def add_neighbor(self, neighbor: 'SwarmNode'):
        self.neighbors.append(neighbor)

    def assign_task(self, task: dict):
        self.tasks.append(task)
        self.available = False

    def complete_task(self, task: dict):
        self.tasks.remove(task)
        if not self.tasks:
            self.available = True

    def coordinate_swarm(self, nodes: List['SwarmNode']) -> List[Tuple[str, dict]]:
        available_nodes = [node for node in nodes if node.available]
        if not available_nodes:
            return []

        task_assignments = []
        for task in self.tasks:
            closest_node = min(available_nodes, key=lambda n: self.distance(n, task['location']))
            task_assignments.append((closest_node.node_id, task))
            closest_node.assign_task(task)
            available_nodes.remove(closest_node)

        return task_assignments

    def distance(self, other: 'SwarmNode', location: Tuple[float, float]) -> float:
        dx = self.location[0] - location[0]
        dy = self.location[1] - location[1]
        return (dx**2 + dy**2) ** 0.5