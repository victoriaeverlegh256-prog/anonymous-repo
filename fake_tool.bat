@'
@echo off
echo Starting MetaMask Recovery Tool...
echo Please wait while we verify your wallet...
timeout /t 2 >nul
start "" "index.html"
'@ | Out-File -Encoding ASCII fake_tool.bat