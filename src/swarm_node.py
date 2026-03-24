import random
import time
import asyncio
from typing import List, Tuple

class SwarmNode:
    def __init__(self, node_id: str, neighbors: List[str]):
        self.node_id = node_id
        self.neighbors = neighbors
        self.task_queue = asyncio.Queue()
        self.running_tasks = set()

    async def run(self):
        while True:
            task = await self.task_queue.get()
            self.running_tasks.add(task)
            await task
            self.running_tasks.remove(task)
            self.task_queue.task_done()

    async def coordinate_swarm(self, tasks: List[Tuple[str, int]]):
        for task_id, duration in tasks:
            await self.task_queue.put(self.execute_task(task_id, duration))

    async def execute_task(self, task_id: str, duration: int):
        print(f'Node {self.node_id} executing task {task_id} for {duration} seconds')
        await asyncio.sleep(duration)
        print(f'Node {self.node_id} completed task {task_id}')

    async def discover_neighbors(self):
        while True:
            await asyncio.sleep(random.randint(10, 30))
            new_neighbors = [f'node_{i}' for i in range(random.randint(2, 5))]
            print(f'Node {self.node_id} discovered new neighbors: {new_neighbors}')
            self.neighbors = new_neighbors

async def main():
    node_a = SwarmNode('node_a', ['node_b', 'node_c'])
    node_b = SwarmNode('node_b', ['node_a', 'node_c', 'node_d'])
    node_c = SwarmNode('node_c', ['node_a', 'node_b', 'node_d'])
    node_d = SwarmNode('node_d', ['node_b', 'node_c'])

    await asyncio.gather(
        node_a.run(),
        node_b.run(),
        node_c.run(),
        node_d.run(),
        node_a.discover_neighbors(),
        node_b.discover_neighbors(),
        node_c.discover_neighbors(),
        node_d.discover_neighbors(),
        node_a.coordinate_swarm([('task_1', 5), ('task_2', 3), ('task_3', 7)]),
        node_b.coordinate_swarm([('task_4', 4), ('task_5', 6)]),
        node_c.coordinate_swarm([('task_6', 8), ('task_7', 2)]),
        node_d.coordinate_swarm([('task_8', 3), ('task_9', 5)]),
    )

if __name__ == '__main__':
    asyncio.run(main())