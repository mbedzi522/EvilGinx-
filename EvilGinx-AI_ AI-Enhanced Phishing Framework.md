# EvilGinx-AI: AI-Enhanced Phishing Framework

![EvilGinx-AI Logo](https://img.shields.io/badge/EvilGinx--AI-v1.0.0-purple?style=for-the-badge&logo=shield)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-Educational%20Use%20Only-red?style=for-the-badge)

**EvilGinx-AI** is an advanced, AI-enhanced phishing framework inspired by Evilginx2, designed specifically for authorized penetration testing and security research. This tool integrates Google's Gemini AI to provide intelligent phishing detection, evasion capabilities, and automated content generation.

## ⚠️ IMPORTANT DISCLAIMER

**This tool is designed exclusively for authorized penetration testing, security research, and educational purposes. The authors and contributors are not responsible for any misuse of this software. Users must ensure they have explicit written permission before testing any systems they do not own.**

## 🚀 Features

### Core Functionality
- **Reverse Proxy Architecture**: Advanced man-in-the-middle proxy server
- **Session Cookie Capture**: Bypass 2FA by capturing valid session tokens
- **DNS Server**: Built-in DNS resolution for phishing domains
- **Phishlet System**: Configurable templates for different target services
- **Real-time Logging**: Comprehensive logging and monitoring

### AI-Enhanced Capabilities
- **Intelligent Request Analysis**: AI-powered detection of security scanners and bots
- **Dynamic Content Generation**: AI-driven content modification for better evasion
- **Automated Phishlet Generation**: AI assistance in creating phishlet configurations
- **Behavioral Analysis**: AI-powered analysis of captured session data
- **Evasion Techniques**: AI-suggested methods to bypass security controls

### Web Dashboard
- **Modern Interface**: Responsive web dashboard for campaign management
- **Real-time Statistics**: Live monitoring of active sessions and captures
- **AI Tools Integration**: Direct access to AI-powered features
- **Campaign Management**: Easy setup and monitoring of phishing campaigns
- **Session Viewer**: Detailed view of captured credentials and cookies

## 📋 Requirements

### System Requirements
- **Operating System**: Kali Linux (recommended) or Ubuntu 20.04+
- **Python**: 3.8 or higher
- **Memory**: Minimum 2GB RAM
- **Storage**: 1GB free space
- **Network**: Internet connection for AI features

### API Requirements
- **Gemini API Key**: Required for AI functionality
- **Root Privileges**: Optional, for DNS server on port 53

## 🛠️ Installation

### Quick Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/evilginx-ai.git
cd evilginx-ai

# Run the installation script
chmod +x install.sh
./install.sh
```

### Manual Installation

```bash
# Install system dependencies
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs certificates database
```

## ⚙️ Configuration

### Basic Configuration

Edit the `config/config.yaml` file to configure the framework:

```yaml
# Server settings
proxy_port: 8000
dashboard_port: 8080
dns_port: 5353

# AI settings
gemini_api_key: 'YOUR_GEMINI_API_KEY_HERE'
ai_enabled: true
ai_detection_enabled: true

# Domain settings
base_domain: 'your-phishing-domain.com'
redirect_url: 'https://google.com'
```

### Gemini API Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add the API key to your configuration file
4. Ensure you have sufficient API quota

## 🚀 Usage

### Starting the Framework

```bash
# Start with default settings
./run.sh

# Start with verbose logging
./run.sh --verbose

# Start with custom config
./run.sh --config custom-config.yaml
```

### Accessing the Dashboard

Once started, access the web dashboard at:
- **URL**: http://localhost:8080
- **Features**: Campaign management, AI tools, session monitoring

### Creating Phishlets

Phishlets are configuration files that define how to proxy specific target services:

```yaml
name: 'example-service'
author: 'Your Name'
proxy_hosts:
  - phish_sub: 'login'
    orig_sub: 'login'
    domain: 'example.com'
    session: true
    is_landing: true
credentials:
  username:
    key: 'username'
    search: '(.*)'
    type: 'post'
  password:
    key: 'password'
    search: '(.*)'
    type: 'post'
```

### AI-Powered Features

#### Request Analysis
```python
# Analyze incoming requests for scanners/bots
result = await ai_client.classify_request({
    'ip': '192.168.1.100',
    'user_agent': 'Mozilla/5.0...',
    'headers': {...}
})
```

#### Content Generation
```python
# Generate evasive content modifications
modified_content = await ai_client.modify_content_for_evasion(
    html_content, phishlet_config
)
```

## 📁 Project Structure

```
evilginx-ai/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── install.sh             # Installation script
├── run.sh                 # Run script
├── config/
│   └── config.yaml        # Configuration file
├── core/                  # Core framework modules
│   ├── proxy_server.py    # Reverse proxy implementation
│   ├── dns_server.py      # DNS server implementation
│   └── config_manager.py  # Configuration management
├── ai/                    # AI integration modules
│   └── gemini_client.py   # Gemini API client
├── web/                   # Web dashboard
│   └── dashboard.py       # FastAPI dashboard
├── phishlets/             # Phishlet configurations
├── database/              # Session database
├── logs/                  # Application logs
└── certificates/          # SSL certificates
```

## 🔧 Advanced Configuration

### SSL/TLS Setup

For HTTPS support, configure SSL certificates:

```yaml
ssl_cert_path: '/path/to/certificate.crt'
ssl_key_path: '/path/to/private.key'
auto_ssl: false
```

### DNS Configuration

For full DNS functionality, run with root privileges:

```bash
sudo ./run.sh
```

Or configure your DNS server to forward queries to the framework.

### Systemd Service

Enable automatic startup with systemd:

```bash
sudo systemctl enable evilginx-ai
sudo systemctl start evilginx-ai
```

## 🛡️ Security Considerations

### Defensive Measures
- **Rate Limiting**: Implement request rate limiting
- **IP Filtering**: Block known security scanner IPs
- **User-Agent Analysis**: Filter suspicious user agents
- **Behavioral Analysis**: Monitor for automated behavior

### Operational Security
- **Isolated Environment**: Run in isolated networks
- **Log Management**: Secure and rotate logs regularly
- **Access Control**: Restrict dashboard access
- **Data Encryption**: Encrypt captured data at rest

## 🔍 Troubleshooting

### Common Issues

#### Permission Denied (DNS)
```bash
# Solution: Run with sudo or use unprivileged port
sudo ./run.sh
# OR modify config to use port 5353
```

#### Gemini API Errors
```bash
# Check API key validity
# Verify API quota
# Check network connectivity
```

#### Module Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

### Debug Mode

Enable verbose logging for troubleshooting:

```bash
./run.sh --verbose
```

## 📊 Monitoring and Analytics

### Dashboard Metrics
- **Active Sessions**: Real-time session count
- **Captured Credentials**: Successful credential captures
- **AI Detections**: Scanner/bot detections
- **Blocked Requests**: Filtered malicious requests

### Log Analysis
```bash
# View real-time logs
tail -f logs/evilginx-ai.log

# Search for specific events
grep "AI detected" logs/evilginx-ai.log
```

## 🤝 Contributing

We welcome contributions from the security research community:

1. **Fork** the repository
2. **Create** a feature branch
3. **Commit** your changes
4. **Push** to the branch
5. **Create** a Pull Request

### Development Setup

```bash
# Clone for development
git clone https://github.com/your-repo/evilginx-ai.git
cd evilginx-ai

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

## 📜 License

This project is released under a **Educational Use Only** license. Commercial use, malicious use, or use without proper authorization is strictly prohibited.

## 🙏 Acknowledgments

- **Evilginx2**: Original inspiration by Kuba Gretzky
- **Google Gemini**: AI capabilities powered by Google's Gemini API
- **Security Community**: Thanks to all researchers and ethical hackers

## 📞 Support

For support and questions:

- **Issues**: GitHub Issues page
- **Documentation**: Check the wiki
- **Security**: Report vulnerabilities responsibly

---

**Remember: With great power comes great responsibility. Use this tool ethically and legally.**

