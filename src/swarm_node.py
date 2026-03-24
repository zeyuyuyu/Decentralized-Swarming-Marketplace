import asyncio
from dataclasses import dataclass
from typing import Dict, List, Optional
import time

@dataclass
class PeerStats:
    uptime: float
    success_rate: float
    last_seen: float
    total_transactions: int
    response_time: float

class SwarmNode:
    def __init__(self, node_id: str, host: str, port: int):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.peers: Dict[str, PeerStats] = {}
        self.active = False
        self.load_threshold = 0.8

    async def start(self):
        self.active = True
        await asyncio.gather(
            self.peer_discovery_loop(),
            self.reputation_update_loop()
        )

    async def peer_discovery_loop(self):
        while self.active:
            await self.discover_peers()
            await asyncio.sleep(30)

    async def discover_peers(self):
        # Implement DHT-based peer discovery here
        pass

    async def reputation_update_loop(self):
        while self.active:
            self._update_peer_scores()
            await asyncio.sleep(60)

    def _update_peer_scores(self):
        current_time = time.time()
        for peer_id, stats in self.peers.items():
            # Decay old reputation scores
            time_factor = max(0, 1 - (current_time - stats.last_seen) / 3600)
            stats.success_rate *= time_factor

    def get_best_peers(self, n: int = 3) -> List[str]:
        """Return top N peers based on reputation score"""
        scored_peers = [
            (peer_id, self._calculate_reputation(stats))
            for peer_id, stats in self.peers.items()
        ]
        return [p[0] for p in sorted(scored_peers, key=lambda x: x[1], reverse=True)[:n]]

    def _calculate_reputation(self, stats: PeerStats) -> float:
        uptime_weight = 0.3
        success_weight = 0.4
        response_weight = 0.3

        response_score = 1.0 / (1.0 + stats.response_time)  # Normalize response time
        
        return (
            (stats.uptime * uptime_weight) +
            (stats.success_rate * success_weight) +
            (response_score * response_weight)
        )

    async def handle_transaction(self, transaction_data: dict) -> bool:
        if self._is_overloaded():
            best_peers = self.get_best_peers()
            if best_peers:
                return await self._delegate_transaction(transaction_data, best_peers[0])
        return await self._process_transaction(transaction_data)

    def _is_overloaded(self) -> bool:
        # Implementation of load checking logic
        return False

    async def _delegate_transaction(self, transaction_data: dict, peer_id: str) -> bool:
        # Implementation of transaction delegation
        return True

    async def _process_transaction(self, transaction_data: dict) -> bool:
        # Implementation of local transaction processing
        return True

    async def stop(self):
        self.active = False
