import imaplib
import email
import time
import requests
import re
import os
from datetime import datetime
import pytz

# =========================
# BOT CONFIG
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

last_update_id = 0

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
# FANCY NUMBER
# =========================
def fancy_number(text):

    normal = "0123456789"
    fancy = "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"

    for n, f in zip(normal, fancy):
        text = text.replace(n, f)

    return text

# =========================
# FANCY TIME
# =========================
def get_fancy_time():

    tz = pytz.timezone("Asia/Karachi")

    now = datetime.now(tz)

    time_str = now.strftime("%I:%M %p")

    time_str = time_str.replace("AM", "𝐀𝐌")
    time_str = time_str.replace("PM", "𝐏𝐌")

    return fancy_number(time_str)

# =========================
# DETECT SERVICE
# =========================
def detect_service(text):

    text = text.lower()

    if "binance" in text:
        return "Binance", "🟡"

    elif "okx" in text:
        return "OKX", "⚫"

    elif "bitget" in text:
        return "Bitget", "🔵"

    elif "bybit" in text:
        return "Bybit", "🟠"

    return "Email Service", "📩"

# =========================
# FIND OTP
# =========================
def find_otp(text):

    match = re.search(r"\b\d{6}\b", text)

    return match.group() if match else None

# =========================
# BUTTONS
# =========================
def get_buttons():

    return {
        "inline_keyboard": [

            [
                {
                    "text": f"🧪 {fancy_text('TEST OTP')}",
                    "callback_data": "testotp"
                }
            ],

            [
                {
                    "text": f"🔄 {fancy_text('REFRESH')}",
                    "callback_data": "refresh"
                }
            ],

            [
                {
                    "text": f"📊 {fancy_text('STATUS')}",
                    "callback_data": "status"
                }
            ]
        ]
    }

# =========================
# SEND TELEGRAM
# =========================
def send_telegram(service, logo, otp):

    message = f"""
╔══════════════════╗
🔥 {logo} {fancy_text(service.upper())} {fancy_text("OTP")} 🔥
╚══════════════════╝

📩 {fancy_text("OTP")}: {fancy_number(otp[:3])}-{fancy_number(otp[3:])}

⏰ {fancy_text("TIME")}: {get_fancy_time()}

──────────────────

🔐 {fancy_text("DO NOT SHARE")}
"""

    requests.post(
        f"{BASE_URL}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": message,
            "reply_markup": get_buttons()
        }
    )

# =========================
# TEST OTP
# =========================
def send_test_otp():

    send_telegram(
        "Test Service",
        "🧪",
        "648975"
    )

# =========================
# STATUS MESSAGE
# =========================
def send_status():

    message = f"""
╔══════════════════╗
🤖 {fancy_text("BOT STATUS")}
╚══════════════════╝

✅ {fancy_text("BOT ONLINE")}

📧 {fancy_text("MAIL CHECKER ACTIVE")}

⏰ {fancy_text("TIME")}: {get_fancy_time()}
"""

    requests.post(
        f"{BASE_URL}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": message,
            "reply_markup": get_buttons()
        }
    )

# =========================
# CHECK MAIL
# =========================
def check_mail(account):

    try:

        mail = imaplib.IMAP4_SSL("imap.gmail.com")

        mail.login(
            account["email"],
            account["password"]
        )

        mail.select("inbox")

        status, data = mail.search(
            None,
            "UNSEEN"
        )

        mail_ids = data[0].split()

        for i in mail_ids:

            status, msg_data = mail.fetch(
                i,
                "(RFC822)"
            )

            msg = email.message_from_bytes(
                msg_data[0][1]
            )

            subject = str(msg["subject"])

            body = ""

            if msg.is_multipart():

                for part in msg.walk():

                    if part.get_content_type() == "text/plain":

                        body = part.get_payload(
                            decode=True
                        ).decode(errors="ignore")

            else:

                body = msg.get_payload(
                    decode=True
                ).decode(errors="ignore")

            full_text = subject + " " + body

            otp = find_otp(full_text)

            if otp:

                service, logo = detect_service(full_text)

                send_telegram(
                    service,
                    logo,
                    otp
                )

        mail.logout()

    except Exception as e:

        print("Error:", e)

# =========================
# HANDLE BUTTONS
# =========================
def handle_updates():

    global last_update_id

    try:

        response = requests.get(
            f"{BASE_URL}/getUpdates",
            params={
                "offset": last_update_id + 1
            }
        ).json()

        for update in response.get("result", []):

            last_update_id = update["update_id"]

            if "callback_query" in update:

                data = update["callback_query"]["data"]

                if data == "testotp":

                    send_test_otp()

                elif data == "refresh":

                    send_status()

                elif data == "status":

                    send_status()

    except Exception as e:

        print("Update Error:", e)

# =========================
# START MESSAGE
# =========================
send_status()

# =========================
# MAIN LOOP
# =========================
while True:

    handle_updates()

    for account in accounts:

        check_mail(account)

    time.sleep(10)
