import imaplib
import email
import time
import requests
import re
import os
from datetime import datetime
import pytz

# =========================
# TELEGRAM BOT DETAILS
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# GMAIL ACCOUNTS
# =========================
accounts = [
    {"email": "ahmadkhansolangi12gmail@gmail.com", "password": "pmcp vwjj zcma dthm"},
    {"email": "ahmadkhansolangi16@gmail.com", "password": "lnqj mxdp igao krfe"},
    {"email": "mrzeeshanmalik523gmail@gmail.com", "password": "etni pesy ydoe ghzb"},
    {"email": "innocent.shafeeq1@gmail.com", "password": "xgxv bxoc ctls pgnd"},
        {"email": "suhailahmedchandio43@gmail.com", "password": "eesf ahyh gjpj jtpw"},
            {"email": "innocent.ahmad808@gmail.com", "password": "xgxv bxoc ctls pgnd"},
                {"email": "shafeeqkhansolangi8@gmail.com", "password": "tiap vact gemz yefs"},
]

# =========================
# FANCY TEXT
# =========================
def fancy_text(text):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    fancy = "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙" \
            "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳"

    for n, f in zip(normal, fancy):
        text = text.replace(n, f)

    return text

# =========================
# FANCY NUMBERS
# =========================
def fancy_number(text):
    normal = "0123456789"
    fancy = "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"

    for n, f in zip(normal, fancy):
        text = text.replace(n, f)

    return text

# =========================
# GET FANCY TIME
# =========================
def get_fancy_time():
    tz = pytz.timezone("Asia/Karachi")
    now = datetime.now(tz)

    current_time = now.strftime("%I:%M %p")

    return fancy_number(current_time)

# =========================
# DETECT SERVICE
# =========================
def detect_service(text):
    text = text.lower()

    if "bitget" in text:
        return "Bitget", "🟡🏦"

    elif "binance" in text:
        return "Binance", "🟡🟨"

    elif "okx" in text:
        return "OKX", "⚫🟦"

    elif "bybit" in text:
        return "Bybit", "🟠⚡"

    return "Unknown", "📩"

# =========================
# FIND OTP
# =========================
def find_otp(text):
    otp = re.search(r"\b\d{6}\b", text)

    if otp:
        return otp.group()

    return None

# =========================
# SEND TELEGRAM MESSAGE
# =========================
def send_telegram(service, logo, otp):
    service_fancy = fancy_text(service.upper())
    otp_fancy = fancy_number(otp)

    message = f"""
╔══════════════════╗
🔥 {logo} {service_fancy} 𝐎𝐓𝐏 🔥
╚══════════════════╝

📩 𝐎𝐓𝐏: {otp_fancy}
🏦 𝐒𝐄𝐑𝐕𝐈𝐂𝐄: {service_fancy}
⏰ 𝐓𝐈𝐌𝐄: {get_fancy_time()}

──────────────────
⚡ 𝐒𝐓𝐀𝐓𝐔𝐒: 𝐕𝐄𝐑𝐈𝐅𝐈𝐂𝐀𝐓𝐈𝐎𝐍
🔐 𝐃𝐎 𝐍𝐎𝐓 𝐒𝐇𝐀𝐑𝐄
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)

# =========================
# CHECK MAIL
# =========================
def check_mail(account):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")

        mail.login(account["email"], account["password"])

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
                    content_type = part.get_content_type()

                    if content_type == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")

            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            full_text = subject + " " + body

            otp = find_otp(full_text)

            if otp:
                service, logo = detect_service(full_text)

                send_telegram(service, logo, otp)

        mail.logout()

    except Exception as e:
        print("Error:", e)

# =========================
# MAIN LOOP
# =========================
while True:
    for account in accounts:
        check_mail(account)

    time.sleep(30)