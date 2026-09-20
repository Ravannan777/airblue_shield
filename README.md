# AirBlue-Shield 🛡️

**AirBlue-Shield** is an advanced cross-platform cybersecurity and network auditing tool designed for Windows and Termux/Linux. It helps security enthusiasts scan Wi-Fi networks across all bands, detect potential Rogue APs / Evil Twins, and monitor active Bluetooth devices in real-time.

---

## 🚀 Features
* **Detailed Wi-Fi Scanning:** Scan surrounding networks with band and channel details.
* **Live Wi-Fi Monitoring:** Continuous monitoring focusing on essential parameters (SSID, Open/Closed Auth Type, MAC Address, Signal Strength, Frequency, Channel).
* **Bluetooth Discovery:** Scan active nearby BLE and Classic devices using `bleak`.
* **Cross-Platform:** Fully optimized for Windows (CMD/PowerShell) and Android Termux.

---

## 📦 Installation & Setup

### For Termux (Android):
pkg update && pkg upgrade -y

pkg install python git bluez wireless-tools networkmanager -y

git clone [https://github.com/yourusername/AirBlue-Shield.git](https://github.com/yourusername/AirBlue-Shield.git)


pip install -r requirements.txt

python3 airblue_shield.py

# Developed By
**Sreenand**

