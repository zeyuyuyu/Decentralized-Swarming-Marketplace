import time
import random
import threading
from dataclasses import dataclass
from typing import Dict, List, Set

@dataclass
class PeerInfo:
    address: str
    last_seen: float
    services: List[str]

class SwarmNode:
    def __init__(self, node_id: str, port: int):
        self.node_id = node_id
        self.port = port
        self.peers: Dict[str, PeerInfo] = {}
        self.services: Set[str] = set()
        self.is_running = False
        self._lock = threading.Lock()

    def start(self):
        """Start the swarm node and begin peer discovery"""
        self.is_running = True
        self._discovery_thread = threading.Thread(target=self._run_discovery)
        self._heartbeat_thread = threading.Thread(target=self._run_heartbeat)
        self._discovery_thread.start()
        self._heartbeat_thread.start()

    def stop(self):
        """Stop the swarm node and cleanup"""
        self.is_running = False
        self._discovery_thread.join()
        self._heartbeat_thread.join()

    def register_service(self, service_name: str):
        """Register a service that this node can provide"""
        with self._lock:
            self.services.add(service_name)

    def unregister_service(self, service_name: str):
        """Remove a service from this node"""
        with self._lock:
            self.services.discard(service_name)

    def get_peers_for_service(self, service_name: str) -> List[str]:
        """Find all peers that provide a specific service"""
        with self._lock:
            return [
                peer_id for peer_id, info in self.peers.items()
                if service_name in info.services
            ]

    def _run_discovery(self):
        """Background thread for peer discovery"""
        while self.is_running:
            try:
                # Simulate peer discovery
                if random.random() < 0.1:  # 10% chance to discover new peer
                    peer_id = f"peer_{random.randint(1000, 9999)}"
                    peer_info = PeerInfo(
                        address=f"192.168.1.{random.randint(2, 254)}",
                        last_seen=time.time(),
                        services=[f"service_{random.randint(1, 5)}"]
                    )
                    with self._lock:
                        self.peers[peer_id] = peer_info
            except Exception as e:
                print(f"Discovery error: {e}")
            time.sleep(5)

    def _run_heartbeat(self):
        """Background thread for peer heartbeat and cleanup"""
        while self.is_running:
            try:
                current_time = time.time()
                with self._lock:
                    # Remove peers not seen in last 30 seconds
                    self.peers = {
                        peer_id: info for peer_id, info in self.peers.items()
                        if (current_time - info.last_seen) < 30
                    }
                    # Update last_seen for connected peers
                    for peer_id in list(self.peers.keys()):
                        if random.random() < 0.8:  # 80% chance of successful heartbeat
                            self.peers[peer_id].last_seen = current_time
            except Exception as e:
                print(f"Heartbeat error: {e}")
            time.sleep(1)

    def get_network_stats(self) -> Dict:
        """Get statistics about the node's network"""
        with self._lock:
            return {
                "total_peers": len(self.peers),
                "active_services": list(self.services),
                "peer_services": {
                    peer_id: info.services
                    for peer_id, info in self.peers.items()
                }
            }
