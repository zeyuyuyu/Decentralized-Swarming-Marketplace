import asyncio
import json
import time
from typing import Dict, Set

class SwarmNode:
    def __init__(self, node_id: str, host: str = 'localhost', port: int = 8000):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.peers: Dict[str, dict] = {}
        self.active = False
        self.last_heartbeat: Dict[str, float] = {}
        self.heartbeat_interval = 5.0
        self.peer_timeout = 15.0

    async def start(self):
        """Start the swarm node and begin peer discovery"""
        self.active = True
        await asyncio.gather(
            self.heartbeat_loop(),
            self.cleanup_loop()
        )

    async def heartbeat_loop(self):
        """Periodically send heartbeat to all known peers"""
        while self.active:
            heartbeat = {
                'type': 'heartbeat',
                'node_id': self.node_id,
                'timestamp': time.time(),
                'peers': list(self.peers.keys())
            }
            for peer_id, peer_info in self.peers.items():
                try:
                    # Simulate network call for now
                    # In real implementation, would use actual network transport
                    await self.send_to_peer(peer_id, heartbeat)
                except Exception as e:
                    print(f'Failed to send heartbeat to {peer_id}: {e}')
            
            await asyncio.sleep(self.heartbeat_interval)

    async def cleanup_loop(self):
        """Remove peers that haven't sent a heartbeat recently"""
        while self.active:
            current_time = time.time()
            dead_peers = [
                peer_id for peer_id, last_beat in self.last_heartbeat.items()
                if current_time - last_beat > self.peer_timeout
            ]
            
            for peer_id in dead_peers:
                self.remove_peer(peer_id)
            
            await asyncio.sleep(self.heartbeat_interval)

    async def send_to_peer(self, peer_id: str, message: dict):
        """Send a message to a specific peer"""
        if peer_id not in self.peers:
            raise ValueError(f'Unknown peer {peer_id}')
        
        # Simulate network send - replace with actual transport
        peer = self.peers[peer_id]
        print(f'Sending to {peer_id}: {message}')

    def add_peer(self, peer_id: str, peer_info: dict):
        """Add a new peer to the swarm"""
        if peer_id not in self.peers:
            self.peers[peer_id] = peer_info
            self.last_heartbeat[peer_id] = time.time()
            print(f'Added peer {peer_id}')

    def remove_peer(self, peer_id: str):
        """Remove a peer from the swarm"""
        if peer_id in self.peers:
            del self.peers[peer_id]
            del self.last_heartbeat[peer_id]
            print(f'Removed peer {peer_id}')

    def handle_heartbeat(self, peer_id: str, heartbeat: dict):
        """Process a heartbeat received from a peer"""
        self.last_heartbeat[peer_id] = heartbeat['timestamp']
        
        # Add any new peers we learn about
        for new_peer_id in heartbeat['peers']:
            if new_peer_id not in self.peers and new_peer_id != self.node_id:
                # In real implementation, would need to get peer info
                self.add_peer(new_peer_id, {'host': 'unknown', 'port': 0})

    async def stop(self):
        """Stop the swarm node"""
        self.active = False
