#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool Name: AirBlue-Shield (Advanced Wi-Fi & Bluetooth Threat Detector)
Description: Cross-platform security audit tool featuring customized Live Wi-Fi
             monitoring with essential parameters only, and clean developer branding.
"""

import platform
import subprocess
import time
import os
import sys
import asyncio
from datetime import datetime

# Check and import Bleak for Bluetooth
try:
    from bleak import BleakScanner
    BLEAK_AVAILABLE = True
except ImportError:
    BLEAK_AVAILABLE = False

class AirBlueShield:
    def __init__(self):
        self.os_type = platform.system()
        self.is_termux = os.path.exists("/data/data/com.termux/files/home")
        self.tool_name = "AirBlue-Shield"
        self.version = "3.5.0"
        self.developer_name = "SREENAND " 
        self.banner = f"""
        =========================================================
           {self.tool_name} : CYBERSECURITY THREAT DETECTOR v{self.version}
        =========================================================
           [+] Developed By  : {self.developer_name}
           [+] Platform      : {self.os_type} {'(Termux/Android)' if self.is_termux else '(Windows/PC)'}
           [+] Status        : Ready for Live Monitoring & Auditing
        =========================================================
        """

    def clear_screen(self):
        os.system("clear" if self.os_type != "Windows" else "cls")

    def parse_netsh_live(self):
        """Extracts strictly the required 6 fields for Live Wi-Fi Monitoring."""
        try:
            output = subprocess.check_output(["netsh", "wlan", "show", "networks", "mode=bssid"], universal_newlines=True, encoding="latin-1")
            lines = output.split('\n')
            
            networks = []
            current_net = {}
            
            for line in lines:
                line = line.strip()
                if line.startswith("SSID"):
                    if current_net and "ssid" in current_net:
                        networks.append(current_net)
                        current_net = {}
                    parts = line.split(":", 1)
                    if len(parts) > 1:
                        current_net["ssid"] = parts[1].strip()
                elif "Authentication" in line:
                    parts = line.split(":", 1)
                    if len(parts) > 1:
                        auth_val = parts[1].strip()
                        if "Open" in auth_val:
                            current_net["auth"] = "Open (Unsecured)"
                        else:
                            current_net["auth"] = f"Closed / Secured ({auth_val})"
                elif "BSSID" in line:
                    parts = line.split(":", 1)
                    if len(parts) > 1:
                        current_net["bssid"] = parts[1].strip()
                elif "Signal" in line:
                    parts = line.split(":", 1)
                    if len(parts) > 1:
                        current_net["signal"] = parts[1].strip()
                elif "Channel" in line:
                    parts = line.split(":", 1)
                    if len(parts) > 1:
                        current_net["channel"] = parts[1].strip()
                elif "Band" in line or "Frequency" in line:
                    parts = line.split(":", 1)
                    if len(parts) > 1:
                        current_net["freq"] = parts[1].strip()
                        
            if current_net and "ssid" in current_net:
                networks.append(current_net)
                
            return networks
        except Exception:
            return []

    def scan_wifi_networks(self):
        """Detailed One-Time Wi-Fi Scan."""
        self.clear_screen()
        print("\n[*] Initiating Detailed One-Time Wi-Fi Scan...")
        try:
            if self.os_type == "Windows":
                output = subprocess.check_output(["netsh", "wlan", "show", "networks", "mode=bssid"], universal_newlines=True, encoding="latin-1")
                print("\n" + "=" * 75)
                print(output)
                print("=" * 75)
            else:
                output = subprocess.check_output(["nmcli", "-t", "-f", "BSSID,SSID,SIGNAL,FREQ,CHAN", "dev", "wifi"], universal_newlines=True)
                print("\n" + "=" * 75)
                print(output)
                print("=" * 75)
        except Exception as e:
            print(f"[-] Scan error: {e}")

    def live_wifi_monitoring(self):
        """Live Continuous Wi-Fi Monitoring with ONLY requested essential fields."""
        self.clear_screen()
        print("=" * 65)
        print("       LIVE WI-FI MONITORING (PRESS CTRL+C TO STOP)")
        print("=" * 65)
        print("[*] Showing: SSID, Open/Closed Type, MAC ID, Signal, Frequency & Channel.\n")
        
        try:
            while True:
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"\n[--- Scan Cycle Triggered at {timestamp} ---]")
                
                if self.os_type == "Windows":
                    nets = self.parse_netsh_live()
                    if nets:
                        for net in nets:
                            ssid = net.get("ssid", "Unknown")
                            auth = net.get("auth", "Unknown")
                            bssid = net.get("bssid", "N/A")
                            signal = net.get("signal", "N/A")
                            freq = net.get("freq", "N/A")
                            channel = net.get("channel", "N/A")
                            
                            print(f" ➔ SSID          : {ssid}")
                            print(f"   Network Type  : {auth}")
                            print(f"   MAC Address   : {bssid}")
                            print(f"   Signal Strength: {signal}")
                            print(f"   Frequency     : {freq}")
                            print(f"   Channel       : {channel}")
                            print("-" * 50)
                    else:
                        print("[-] No Wi-Fi networks captured in this cycle.")
                else:
                    # Termux / Linux fallback live display
                    output = subprocess.check_output(["nmcli", "-f", "SSID,SECURITY,BSSID,SIGNAL,FREQ,CHAN", "dev", "wifi"], universal_newlines=True)
                    print(output)
                
                print("[--- Waiting 5 seconds for next scan cycle... (Press Ctrl+C to Exit) ---]")
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n[+] Exiting Live Wi-Fi Monitoring and returning to menu...")
            time.sleep(1.5)

    async def execute_bleak_scan(self):
        """One-time Bluetooth Scan."""
        self.clear_screen()
        print("\n[*] Scanning for active Bluetooth devices...")

        if not BLEAK_AVAILABLE:
            print("[-] Error: 'bleak' library is missing! Install via: pip install bleak")
            return

        try:
            devices_found = await BleakScanner.discover(timeout=6.0, return_adv=True)
            
            print("\n" + "=" * 60)
            print("           BLUETOOTH ACTIVE DEVICES REPORT")
            print("=" * 60)
            
            if not devices_found:
                print("[-] No active Bluetooth devices detected nearby.")
            else:
                for address, data in devices_found.items():
                    device_obj = data[0]
                    adv_data = data[1]
                    
                    name = device_obj.name if device_obj.name else (adv_data.local_name if adv_data.local_name else "Unknown Device")
                    mac = device_obj.address
                    rssi = adv_data.rssi
                    
                    print(f" Device Name  : {name}")
                    print(f" MAC Address  : {mac}")
                    print(f" Signal       : {rssi} dBm")
                    print("-" * 60)
            print("=" * 60)
        except Exception as e:
            print(f"[-] Bluetooth scan error: {e}")

    async def live_bluetooth_monitoring_loop(self):
        """Live Continuous Bluetooth Monitoring with History."""
        print("=" * 65)
        print("      LIVE BLUETOOTH MONITORING (PRESS CTRL+C TO STOP)")
        print("=" * 65)
        print("[*] Listening for active broadcast signals...\n")
        
        try:
            while True:
                if BLEAK_AVAILABLE:
                    devices_found = await BleakScanner.discover(timeout=4.0, return_adv=True)
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    
                    if devices_found:
                        for address, data in devices_found.items():
                            dev = data[0]
                            adv = data[1]
                            name = dev.name if dev.name else (adv.local_name if adv.local_name else "Unknown Device")
                            mac = dev.address
                            rssi = adv.rssi
                            
                            print(f" [{timestamp}] ➔ Device : {name}")
                            print(f"               MAC    : {mac}")
                            print(f"               Signal : {rssi} dBm")
                            print("-" * 55)
                    else:
                        print(f" [{timestamp}] [-] No active devices broadcasting in this cycle...")
                
                print("\n[--- Next bluetooth scan cycle in 4 seconds... ---]\n")
                await asyncio.sleep(4)
        except asyncio.CancelledError:
            pass

    def live_bluetooth_monitoring(self):
        try:
            asyncio.run(self.live_bluetooth_monitoring_loop())
        except KeyboardInterrupt:
            print("\n[+] Exiting Live Bluetooth Monitoring...")
            time.sleep(1.5)

    def scan_bluetooth_dispatcher(self):
        try:
            asyncio.run(self.execute_bleak_scan())
        except RuntimeError:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.execute_bleak_scan())

    def run_interactive_lobby(self):
        while True:
            self.clear_screen()
            print(self.banner)
            print(" [1] Detailed One-Time Wi-Fi Scan")
            print(" [2] Detailed One-Time Bluetooth Scan")
            print(" [3] Live Wi-Fi Monitoring Mode (Custom Fields & History)")
            print(" [4] Live Bluetooth Monitoring Mode (Continuous with History)")
            print(" [5] Exit Application")
            print("-" * 57)
            
            user_choice = input("\n Enter your selection [1-5]: ").strip()
            
            if user_choice == "1":
                self.scan_wifi_networks()
                input("\n[*] Press Enter key to return to the main lobby...")
            elif user_choice == "2":
                self.scan_bluetooth_dispatcher()
                input("\n[*] Press Enter key to return to the main lobby...")
            elif user_choice == "3":
                self.live_wifi_monitoring()
                input("\n[*] Press Enter key to return to the main lobby...")
            elif user_choice == "4":
                self.live_bluetooth_monitoring()
                input("\n[*] Press Enter key to return to the main lobby...")
            elif user_choice == "5":
                self.clear_screen()
                print(f"[+] Thank you for using {self.tool_name}. Goodbye!")
                sys.exit(0)
            else:
                print("[-] Invalid choice! Please select an option between 1 and 5.")
                time.sleep(1.5)

if __name__ == "__main__":
    try:
        shield_app = AirBlueShield()
        shield_app.run_interactive_lobby()
    except KeyboardInterrupt:
        print("\n\n[+] Program terminated. Goodbye!")
        sys.exit(0)
