#!/bin/bash

# EvilGinx-AI Installation Script for Kali Linux
# AI-Enhanced Phishing Framework for Penetration Testing

set -e

echo "=========================================="
echo "EvilGinx-AI Installation Script"
echo "AI-Enhanced Phishing Framework"
echo "=========================================="

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "This script should not be run as root for security reasons."
   echo "Please run as a regular user with sudo privileges."
   exit 1
fi

# Update system
echo "[+] Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required system packages
echo "[+] Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv git curl wget dnsutils net-tools

# Create virtual environment
echo "[+] Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "[+] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "[+] Creating directory structure..."
mkdir -p logs certificates database

# Set up configuration
echo "[+] Setting up configuration..."
if [ ! -f "config/config.yaml" ]; then
    echo "Configuration file already exists."
else
    echo "Please edit config/config.yaml to set your Gemini API key and other settings."
fi

# Create systemd service (optional)
echo "[+] Creating systemd service..."
sudo tee /etc/systemd/system/evilginx-ai.service > /dev/null <<EOF
[Unit]
Description=EvilGinx-AI Phishing Framework
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv/bin
ExecStart=$(pwd)/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Set permissions
echo "[+] Setting permissions..."
chmod +x main.py
chmod +x install.sh
chmod +x run.sh

echo ""
echo "=========================================="
echo "Installation completed successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit config/config.yaml to set your Gemini API key"
echo "2. Run './run.sh' to start the framework"
echo "3. Access the dashboard at http://localhost:8080"
echo ""
echo "For DNS functionality, you may need to run with sudo:"
echo "sudo ./run.sh"
echo ""
echo "To enable systemd service:"
echo "sudo systemctl enable evilginx-ai"
echo "sudo systemctl start evilginx-ai"
echo ""
echo "IMPORTANT: This tool is for authorized penetration testing only!"
echo "Use responsibly and only on systems you own or have permission to test."
echo ""

