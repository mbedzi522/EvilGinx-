#!/usr/bin/env python3
"""
EvilGinx-AI: AI-Enhanced Phishing Framework
A penetration testing tool inspired by Evilginx2 with AI capabilities using Gemini API
For educational and authorized security testing purposes only.
"""

import asyncio
import argparse
import sys
import os
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.proxy_server import ProxyServer
from core.dns_server import DNSServer
from core.config_manager import ConfigManager
from ai.gemini_client import GeminiClient
from web.dashboard import create_dashboard_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/evilginx-ai.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class EvilGinxAI:
    """Main application class for EvilGinx-AI framework"""
    
    def __init__(self, config_file='config/config.yaml'):
        self.config_manager = ConfigManager(config_file)
        self.config = self.config_manager.load_config()
        
        # Initialize AI client
        self.ai_client = GeminiClient(
            api_key=self.config.get('gemini_api_key', 'AIzaSyAJFQ_m8mrEB8n_QfiO7nosPfz9wJAtk_0')
        )
        
        # Initialize servers
        self.proxy_server = ProxyServer(self.config, self.ai_client)
        self.dns_server = DNSServer(self.config)
        
        # Initialize web dashboard
        self.dashboard_app = create_dashboard_app(self.config, self.ai_client)
        
    async def start_servers(self):
        """Start all servers (proxy, DNS, dashboard)"""
        logger.info("Starting EvilGinx-AI framework...")
        
        # Start DNS server
        dns_task = asyncio.create_task(self.dns_server.start())
        logger.info(f"DNS server starting on port {self.config.get('dns_port', 53)}")
        
        # Start proxy server
        proxy_task = asyncio.create_task(self.proxy_server.start())
        logger.info(f"Proxy server starting on port {self.config.get('proxy_port', 80)}")
        
        # Start dashboard
        dashboard_task = asyncio.create_task(self.start_dashboard())
        logger.info(f"Dashboard starting on port {self.config.get('dashboard_port', 8080)}")
        
        # Wait for all servers
        await asyncio.gather(dns_task, proxy_task, dashboard_task)
        
    async def start_dashboard(self):
        """Start the web dashboard"""
        import uvicorn
        config = uvicorn.Config(
            self.dashboard_app,
            host="0.0.0.0",
            port=self.config.get('dashboard_port', 8080),
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()
        
    def stop(self):
        """Stop all servers"""
        logger.info("Stopping EvilGinx-AI framework...")
        # Cleanup code here
        
def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='EvilGinx-AI: AI-Enhanced Phishing Framework')
    parser.add_argument('--config', '-c', default='config/config.yaml',
                       help='Configuration file path')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create application instance
    app = EvilGinxAI(args.config)
    
    try:
        # Run the application
        asyncio.run(app.start_servers())
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
        app.stop()
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

