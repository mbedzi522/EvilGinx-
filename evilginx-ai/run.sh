#!/bin/bash

# EvilGinx-AI Run Script
# Start the AI-Enhanced Phishing Framework

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# ASCII Art Banner
echo -e "${PURPLE}"
cat << "EOF"
 ______     _ _  _____ _            _____   _____ 
|  ____|   (_) |/ ____(_)          |  __ \ |_   _|
| |____   ___| | |  __ _ _ __ __  __| |__) |  | |  
|  __\ \ / / | | | |_ | | '_ \\ \/ /|  _  /   | |  
| |___\ V /| | | |__| | | | | |>  < | | \ \  _| |_ 
|______\_/ |_|_|\_____|_|_| |_/_/\_\|_|  \_\|_____|
                                                   
    AI-Enhanced Phishing Framework for Pentesting
EOF
echo -e "${NC}"

echo -e "${BLUE}=========================================="
echo -e "EvilGinx-AI - Starting Framework"
echo -e "==========================================${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}[!] Virtual environment not found. Please run install.sh first.${NC}"
    exit 1
fi

# Activate virtual environment
echo -e "${GREEN}[+] Activating virtual environment...${NC}"
source venv/bin/activate

# Check if config exists
if [ ! -f "config/config.yaml" ]; then
    echo -e "${YELLOW}[!] Configuration file not found. Creating default config...${NC}"
    mkdir -p config
    python3 -c "
from core.config_manager import ConfigManager
config_manager = ConfigManager('config/config.yaml')
config_manager.load_config()
print('Default configuration created.')
"
fi

# Check for root privileges for DNS
if [ "$EUID" -eq 0 ]; then
    echo -e "${YELLOW}[!] Running as root. DNS server will use port 53.${NC}"
else
    echo -e "${YELLOW}[!] Running as non-root. DNS server will use port 5353.${NC}"
    echo -e "${YELLOW}    For full DNS functionality, consider running with sudo.${NC}"
fi

# Display startup information
echo -e "${GREEN}[+] Starting EvilGinx-AI Framework...${NC}"
echo -e "${BLUE}[i] Dashboard will be available at: http://localhost:8080${NC}"
echo -e "${BLUE}[i] Proxy server will listen on port: 8000${NC}"
echo -e "${BLUE}[i] DNS server will listen on port: 5353 (or 53 if root)${NC}"
echo ""
echo -e "${YELLOW}[!] IMPORTANT: This tool is for authorized penetration testing only!${NC}"
echo -e "${YELLOW}    Use responsibly and only on systems you own or have permission to test.${NC}"
echo ""
echo -e "${GREEN}[+] Press Ctrl+C to stop the framework${NC}"
echo ""

# Start the framework
python3 main.py "$@"

