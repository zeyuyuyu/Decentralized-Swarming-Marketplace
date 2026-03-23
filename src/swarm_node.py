import time
import threading
import json
from typing import Dict, List, Set
import socket
import logging

class SwarmNode:
    def __init__(self, host: str = 'localhost', port: int = 8000):
        self.host = host
        self.port = port
        self.peers: Dict[str, float] = {}  # peer_addr -> last_seen_timestamp
        self.known_services: Dict[str, List[str]] = {}  # service -> [peer_addrs]
        self.active = False
        self.heartbeat_interval = 30  # seconds
        self.peer_timeout = 90  # seconds
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('SwarmNode')

    def start(self):
        """Start the swarm node and begin peer discovery"""
        self.active = True
        self.discovery_thread = threading.Thread(target=self._discovery_loop)
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop)
        self.discovery_thread.start()
        self.heartbeat_thread.start()
        self.logger.info(f'SwarmNode started on {self.host}:{self.port}')

    def stop(self):
        """Stop the swarm node"""
        self.active = False
        self.discovery_thread.join()
        self.heartbeat_thread.join()
        self.sock.close()
        self.logger.info('SwarmNode stopped')

    def register_service(self, service_name: str):
        """Register a service that this node can provide"""
        if service_name not in self.known_services:
            self.known_services[service_name] = []
        addr = f'{self.host}:{self.port}'
        if addr not in self.known_services[service_name]:
            self.known_services[service_name].append(addr)
            self.logger.info(f'Registered service: {service_name}')

    def _discovery_loop(self):
        """Main discovery loop that listens for peer announcements"""
        self.sock.settimeout(1.0)
        while self.active:
            try:
                data, addr = self.sock.recvfrom(1024)
                msg = json.loads(data.decode())
                
                if msg['type'] == 'heartbeat':
                    peer_addr = f'{addr[0]}:{addr[1]}'
                    self.peers[peer_addr] = time.time()
                    
                    # Update services
                    for service in msg.get('services', []):
                        if service not in self.known_services:
                            self.known_services[service] = []
                        if peer_addr not in self.known_services[service]:
                            self.known_services[service].append(peer_addr)
                    
                    self.logger.debug(f'Heartbeat from {peer_addr}')
                    
            except socket.timeout:
                continue
            except Exception as e:
                self.logger.error(f'Error in discovery loop: {str(e)}')

    def _heartbeat_loop(self):
        """Periodically send heartbeats and clean up stale peers"""
        while self.active:
            try:
                # Send heartbeat to broadcast
                msg = {
                    'type': 'heartbeat',
                    'services': list(self.known_services.keys())
                }
                self.sock.sendto(json.dumps(msg).encode(), ('<broadcast>', self.port))
                
                # Clean up stale peers
                now = time.time()
                stale_peers = [
                    peer for peer, last_seen in self.peers.items()
                    if now - last_seen > self.peer_timeout
                ]
                
                for peer in stale_peers:
                    del self.peers[peer]
                    # Remove from services
                    for services in self.known_services.values():
                        if peer in services:
                            services.remove(peer)
                    self.logger.info(f'Removed stale peer: {peer}')
                
                time.sleep(self.heartbeat_interval)
                
            except Exception as e:
                self.logger.error(f'Error in heartbeat loop: {str(e)}')
                time.sleep(1)

    def get_peers(self) -> List[str]:
        """Get list of active peers"""
        return list(self.peers.keys())

    def get_service_providers(self, service_name: str) -> List[str]:
        """Get list of peers providing a specific service"""
        return self.known_services.get(service_name, [])