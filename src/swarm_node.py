import asyncio
import json
import time
from typing import Dict, Set

class SwarmNode:
    def __init__(self, node_id: str, host: str, port: int):
        self.node_id = node_id
        self.host = host 
        self.port = port
        self.peers: Dict[str, dict] = {}
        self.last_seen: Dict[str, float] = {}
        self.dead_threshold = 30.0 # seconds
        self.running = False

    async def start(self):
        """Start the node's main loop"""
        self.running = True
        await asyncio.gather(
            self.heartbeat_loop(),
            self.cleanup_loop()
        )

    async def heartbeat_loop(self):
        """Periodically broadcast heartbeat to all known peers"""
        while self.running:
            heartbeat = {
                'type': 'heartbeat',
                'node_id': self.node_id,
                'timestamp': time.time(),
                'peers': list(self.peers.keys())
            }
            for peer in self.peers.values():
                try:
                    await self.send_to_peer(peer, heartbeat)
                except Exception as e:
                    print(f"Failed to send heartbeat to {peer['node_id']}: {e}")
            await asyncio.sleep(10)

    async def cleanup_loop(self):
        """Remove dead peers that haven't sent heartbeat"""
        while self.running:
            current_time = time.time()
            dead_peers = [
                peer_id for peer_id, last_seen in self.last_seen.items()
                if current_time - last_seen > self.dead_threshold
            ]
            for peer_id in dead_peers:
                print(f"Removing dead peer {peer_id}")
                self.peers.pop(peer_id, None)
                self.last_seen.pop(peer_id, None)
            await asyncio.sleep(10)

    async def handle_heartbeat(self, heartbeat: dict):
        """Process incoming heartbeat from peer"""
        peer_id = heartbeat['node_id']
        self.last_seen[peer_id] = heartbeat['timestamp']

        # Add any new peers we learn about
        for new_peer_id in heartbeat['peers']:
            if new_peer_id not in self.peers and new_peer_id != self.node_id:
                await self.discover_peer(new_peer_id)

    async def discover_peer(self, peer_id: str):
        """Attempt to discover and connect to a new peer"""
        try:
            # In real implementation, would do DHT lookup here
            peer_info = await self.lookup_peer(peer_id)
            self.peers[peer_id] = peer_info
            print(f"Discovered new peer {peer_id}")
        except Exception as e:
            print(f"Failed to discover peer {peer_id}: {e}")

    async def lookup_peer(self, peer_id: str) -> dict:
        """Lookup peer information (stub for DHT implementation)"""
        raise NotImplementedError()

    async def send_to_peer(self, peer: dict, message: dict):
        """Send message to peer (stub for network implementation)"""
        raise NotImplementedError()

    def stop(self):
        """Stop the node's main loop"""
        self.running = False