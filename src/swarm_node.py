import time
import json
from dataclasses import dataclass
from typing import Dict, List, Optional
import hashlib
import asyncio

@dataclass
class PeerInfo:
    node_id: str
    reputation: float
    last_seen: float
    services: List[str]
    
class SwarmNode:
    def __init__(self, node_id: str = None):
        self.node_id = node_id or hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
        self.peers: Dict[str, PeerInfo] = {}
        self.services: List[str] = []
        self.reputation_threshold = 0.5
        
    async def start(self, port: int = 8000):
        self.port = port
        await self.start_discovery_service()
        
    async def start_discovery_service(self):
        while True:
            await self.broadcast_presence()
            await self.update_peer_status()
            await asyncio.sleep(60)
            
    async def broadcast_presence(self):
        # Simulate broadcasting node presence to network
        presence_msg = {
            'node_id': self.node_id,
            'services': self.services,
            'timestamp': time.time()
        }
        # TODO: Implement actual P2P broadcast
        
    async def update_peer_status(self):
        current_time = time.time()
        stale_peers = []
        
        for peer_id, info in self.peers.items():
            # Remove peers not seen in last 5 minutes
            if current_time - info.last_seen > 300:
                stale_peers.append(peer_id)
                
        for peer_id in stale_peers:
            del self.peers[peer_id]
            
    def register_service(self, service_name: str):
        if service_name not in self.services:
            self.services.append(service_name)
            
    def update_peer_reputation(self, peer_id: str, success: bool):
        if peer_id in self.peers:
            # Reputation adjustments
            delta = 0.1 if success else -0.2
            self.peers[peer_id].reputation = max(0.0, min(1.0, 
                self.peers[peer_id].reputation + delta))
            
    def get_reliable_peers(self) -> List[str]:
        return [
            peer_id for peer_id, info in self.peers.items()
            if info.reputation >= self.reputation_threshold
        ]
    
    def handle_peer_message(self, peer_id: str, message: dict):
        if peer_id not in self.peers:
            self.peers[peer_id] = PeerInfo(
                node_id=peer_id,
                reputation=0.5,
                last_seen=time.time(),
                services=[]
            )
        else:
            self.peers[peer_id].last_seen = time.time()
            
        if 'services' in message:
            self.peers[peer_id].services = message['services']
            
    async def find_service_provider(self, service_name: str) -> Optional[str]:
        reliable_peers = self.get_reliable_peers()
        for peer_id in reliable_peers:
            if service_name in self.peers[peer_id].services:
                return peer_id
        return None

if __name__ == '__main__':
    node = SwarmNode()
    asyncio.run(node.start())