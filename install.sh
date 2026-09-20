#!/bin/bash

echo "[+] Starting AirBlue-Shield Automated Installation..."

# 1. Check if running in Termux or Linux/Windows
if [ -d "/data/data/com.termux/files/home" ]; then
    echo "[*] Termux environment detected. Installing system packages..."
    pkg update && pkg upgrade -y
    pkg install python git bluez wireless-tools networkmanager -y
else
    echo "[*] Standard Linux/PC environment detected."
end

# 2. Upgrade pip and install requirements automatically
echo "[*] Upgrading pip and installing required Python libraries..."
python3 -m pip install --upgrade pip
python3 -m pip install bleak pywifi comtypes

echo "[+] Installation completed successfully! You can now run the tool using:"
echo "    python3 airblue_shield.py"