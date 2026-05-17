import imaplib
import email
import time
import requests
import re
import os
from datetime import datetime
import pytz

# =========================
# CONFIG
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHAT_ID = os.getenv("CHAT_ID")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

last_update_id = 0
bot_running = True
mail_check = True

accounts = [
    {"email": "mrzeeshanmalik530@gmail.com", "password": "etni pesy ydoe ghzb"},
    {"email": "ahmadkhansolangi12@gmail.com", "password": "pmcp vwjj zcma dthm"},
    {"email": "ahmadkhansolangi16@gmail.com", "password": "lnqj mxdp igao krfe"},
    {"email": "innocent.ahmad808@gmail.com", "password": "xgxv bxoc ctls pgnd"},
    {"email": "suhailahmedchandio43@gmail.com", "password": "eesf ahyh gjpj jtpw"},
    {"email": "innocent.shafeeq1@gmail.com", "password": "mofe tryf zfdt syei"},
    {"email": "shafiqkhansolangi8@gmail.com", "password": "tiap vact gemz yefs"},
]

seen_otps = set()

# =========================
# FANCY ENGINE
# =========================
def fancy(text):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    fancy = "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙" \
            "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳"
    for n, f in zip(normal, fancy):
        text = text.replace(n, f)
    return text

def num(text):
    normal = "0123456789"
    fancy = "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"
    for n, f in zip(normal, fancy):
        text = text.replace(n, f)
    return text

def time_now():
    tz = pytz.timezone("Asia/Karachi")
    t = datetime.now(tz).strftime("%I:%M:%S %p")
    t = t.replace("AM","𝐀𝐌").replace("PM","𝐏𝐌")
    return num(t)

# =========================
# OTP FILTER (ONLY 6 DIGITS)
# =========================
def find_otp(text):
    match = re.search(r"\b\d{6}\b", text)
    return match.group() if match else None

# =========================
# FANCY SERVICE NAMES (ULTRA STYLE)
# =========================
def service(text):
    t = text.lower()

    if "binance" in t:
        return "🟡 𝐁𝐈𝐍𝐀𝐍𝐂𝐄 𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘", "🟡"
    elif "okx" in t:
        return "⚫ 𝐎𝐊𝐗 𝐕𝐄𝐑𝐈𝐅𝐈𝐂𝐀𝐓𝐈𝐎𝐍", "⚫"
    elif "bybit" in t:
        return "🟠 𝐁𝐘𝐁𝐈𝐓 𝐏𝐑𝐎𝐓𝐄𝐂𝐓𝐈𝐎𝐍", "🟠"
    elif "bitget" in t:
        return "🔵 𝐁𝐈𝐓𝐆𝐄𝐓 𝐒𝐄𝐑𝐕𝐈𝐂𝐄", "🔵"
    else:
        return "📩 𝐄𝐌𝐀𝐈𝐋 𝐒𝐄𝐑𝐕𝐈𝐂𝐄 𝐀𝐋𝐄𝐑𝐓", "📩"

# =========================
# KEYBOARD (FANCY ADMIN PANEL)
# =========================
def keyboard():
    return {
        "keyboard": [
            ["🟢 𝐒𝐓𝐀𝐑𝐓 𝐁𝐎𝐓", "🔴 𝐒𝐓𝐎𝐏 𝐁𝐎𝐓"],
            ["🧪 𝐓𝐄𝐒𝐓 𝐎𝐓𝐏", "📊 𝐒𝐓𝐀𝐓𝐔𝐒 𝐏𝐀𝐍𝐄𝐋"],
            ["📡 𝐌𝐀𝐈𝐋 𝐎𝐍", "📡 𝐌𝐀𝐈𝐋 𝐎𝐅𝐅"]
        ],
        "resize_keyboard": True
    }

# =========================
# SEND MESSAGE
# =========================
def send(text):
    requests.post(
        f"{BASE_URL}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": text,
            "reply_markup": keyboard()
        }
    )

# =========================
# OTP ALERT (ULTRA FANCY)
# =========================
def send_otp(service_name, logo, otp):
    msg = f"""
╔════════════════════════════╗
        🔐 𝐎𝐓𝐏 𝐀𝐋𝐄𝐑𝐓 🔐
╚════════════════════════════╝

{logo} {service_name}

━━━━━━━━━━━━━━━━━━━━━━━
🔐 𝐎𝐓𝐏 : {num(otp)}
⏰ 𝐓𝐈𝐌𝐄 : {time_now()}
━━━━━━━━━━━━━━━━━━━━━━━

⚡ 𝐒𝐓𝐀𝐓𝐔𝐒 : 𝐈𝐍𝐒𝐓𝐀𝐍𝐓 𝐑𝐄𝐂𝐄𝐈𝐕𝐄𝐃
"""
    send(msg)

# =========================
# TEST OTP
# =========================
def test_otp():
    send(f"""
╔════════════════════════════╗
        🧪 𝐓𝐄𝐒𝐓 𝐌𝐎𝐃𝐄
╚════════════════════════════╝

🔐 𝐎𝐓𝐏 : {num("648975")}
⏰ 𝐓𝐈𝐌𝐄 : {time_now()}

⚡ 𝐒𝐓𝐀𝐓𝐔𝐒 : 𝐑𝐔𝐍𝐍𝐈𝐍𝐆
""")

# =========================
# STATUS PANEL
# =========================
def status():
    state = "𝐑𝐔𝐍𝐍𝐈𝐍𝐆" if bot_running else "𝐒𝐓𝐎𝐏𝐏𝐄𝐃"
    mail = "𝐀𝐂𝐓𝐈𝐕𝐄" if mail_check else "𝐎𝐅𝐅"

    send(f"""
╔════════════════════════════╗
        🤖 𝐂𝐎𝐍𝐓𝐑𝐎𝐋 𝐏𝐀𝐍𝐄𝐋
╚════════════════════════════╝

⚙ 𝐁𝐎𝐓 𝐒𝐓𝐀𝐓𝐔𝐒 : {state}
📡 𝐌𝐀𝐈𝐋 𝐂𝐇𝐄𝐂𝐊 : {mail}
⏰ 𝐓𝐈𝐌𝐄 : {time_now()}

━━━━━━━━━━━━━━━━━━━━━━━
✔ 𝐒𝐘𝐒𝐓𝐄𝐌 𝐎𝐍𝐋𝐈𝐍𝐄
""")

# =========================
# MAIL CHECK
# =========================
def check_mail(acc):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(acc["email"], acc["password"])
        mail.select("inbox")

        status, data = mail.search(None, "UNSEEN")
        mail_ids = data[0].split()

        for i in mail_ids:
            status, msg_data = mail.fetch(i, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])

            subject = str(msg["subject"])
            body = ""

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            full = subject + body
            otp = find_otp(full)

            if otp and otp not in seen_otps:
                seen_otps.add(otp)

                srv, logo = service(full)
                send_otp(srv, logo, otp)

        mail.logout()

    except:
        pass

# =========================
# CONTROL HANDLER
# =========================
def handle(msg):
    global bot_running, mail_check

    if msg.get("from", {}).get("id") != ADMIN_ID:
        return

    text = msg.get("text", "")

    if text == "🟢 𝐒𝐓𝐀𝐑𝐓 𝐁𝐎𝐓":
        bot_running = True
        send("🟢 𝐁𝐎𝐓 𝐒𝐓𝐀𝐑𝐓𝐄𝐃 𝐒𝐔𝐂𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐘")

    elif text == "🔴 𝐒𝐓𝐎𝐏 𝐁𝐎𝐓":
        bot_running = False
        send("🔴 𝐁𝐎𝐓 𝐒𝐓𝐎𝐏𝐏𝐄𝐃 𝐒𝐔𝐂𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐘")

    elif text == "🧪 𝐓𝐄𝐒𝐓 𝐎𝐓𝐏":
        test_otp()

    elif text == "📊 𝐒𝐓𝐀𝐓𝐔𝐒 𝐏𝐀𝐍𝐄𝐋":
        status()

    elif text == "📡 𝐌𝐀𝐈𝐋 𝐎𝐍":
        mail_check = True
        send("📡 𝐌𝐀𝐈𝐋 𝐂𝐇𝐄𝐂𝐊 : 𝐀𝐂𝐓𝐈𝐕𝐄")

    elif text == "📡 𝐌𝐀𝐈𝐋 𝐎𝐅𝐅":
        mail_check = False
        send("📡 𝐌𝐀𝐈𝐋 𝐂𝐇𝐄𝐂𝐊 : 𝐎𝐅𝐅")

# =========================
# UPDATES LOOP
# =========================
def updates():
    global last_update_id

    res = requests.get(
        f"{BASE_URL}/getUpdates",
        params={"offset": last_update_id + 1}
    ).json()

    for u in res.get("result", []):
        last_update_id = u["update_id"]

        if "message" in u:
            handle(u["message"])

# =========================
# START MESSAGE
# =========================
send("""
╔════════════════════════════╗
        🤖 𝐅𝐔𝐋𝐋 𝐅𝐀𝐍𝐂𝐘 𝐎𝐓𝐏 𝐁𝐎𝐓
╚════════════════════════════╝

⚡ 𝐒𝐘𝐒𝐓𝐄𝐌 𝐋𝐎𝐀𝐃𝐄𝐃 𝐒𝐔𝐂𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐘
""")

# =========================
# MAIN LOOP
# =========================
while True:
    updates()

    if bot_running and mail_check:
        for acc in accounts:
            check_mail(acc)

    time.sleep(3)