import time
import random
import threading
from typing import Dict, Set, Optional
from dataclasses import dataclass

@dataclass
class PeerInfo:
    last_seen: float
    reputation: float
    address: str

class SwarmNode:
    def __init__(self, node_id: str, host: str, port: int):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.peers: Dict[str, PeerInfo] = {}
        self.active = True
        self.heartbeat_interval = 30  # seconds
        self._lock = threading.Lock()

    def start(self):
        """Start the swarm node and begin peer discovery/heartbeat"""
        self.active = True
        threading.Thread(target=self._heartbeat_loop, daemon=True).start()
        threading.Thread(target=self._cleanup_loop, daemon=True).start()

    def stop(self):
        """Stop all node activities"""
        self.active = False

    def register_peer(self, peer_id: str, address: str) -> None:
        """Register a new peer in the swarm"""
        with self._lock:
            if peer_id not in self.peers:
                self.peers[peer_id] = PeerInfo(
                    last_seen=time.time(),
                    reputation=1.0,
                    address=address
                )

    def get_active_peers(self) -> Set[str]:
        """Return set of currently active peer IDs"""
        current_time = time.time()
        with self._lock:
            return {pid for pid, info in self.peers.items() 
                    if current_time - info.last_seen <= self.heartbeat_interval * 2}

    def update_peer_reputation(self, peer_id: str, delta: float) -> None:
        """Update peer reputation score"""
        with self._lock:
            if peer_id in self.peers:
                self.peers[peer_id].reputation = max(0.0, 
                    min(1.0, self.peers[peer_id].reputation + delta))

    def _heartbeat_loop(self) -> None:
        """Continuously send heartbeats to peers"""
        while self.active:
            active_peers = self.get_active_peers()
            for peer_id in active_peers:
                try:
                    # TODO: Implement actual network heartbeat
                    # For now just update last_seen
                    with self._lock:
                        if peer_id in self.peers:
                            self.peers[peer_id].last_seen = time.time()
                except Exception as e:
                    self.update_peer_reputation(peer_id, -0.1)
            time.sleep(self.heartbeat_interval)

    def _cleanup_loop(self) -> None:
        """Remove inactive peers periodically"""
        while self.active:
            current_time = time.time()
            with self._lock:
                inactive = [pid for pid, info in self.peers.items()
                           if current_time - info.last_seen > self.heartbeat_interval * 3]
                for pid in inactive:
                    del self.peers[pid]
            time.sleep(self.heartbeat_interval)

    def get_peer_info(self, peer_id: str) -> Optional[PeerInfo]:
        """Get information about a specific peer"""
        with self._lock:
            return self.peers.get(peer_id)

    def broadcast_to_peers(self, message: dict) -> None:
        """Broadcast a message to all active peers"""
        active_peers = self.get_active_peers()
        for peer_id in active_peers:
            try:
                # TODO: Implement actual network broadcast
                pass
            except Exception as e:
                self.update_peer_reputation(peer_id, -0.05)
