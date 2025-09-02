from flask import Flask, render_template, request
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import smtplib
from email.message import EmailMessage
import csv
import os
import time
import json

app = Flask(__name__)

# Google Sheets setup (ENV method)
scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

# Load credentials from ENV (instead of file)
from dotenv import load_dotenv
load_dotenv()
creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
if not creds_json:
    raise Exception("❌ GOOGLE_CREDENTIALS_JSON not found in environment variables")

creds_dict = json.loads(creds_json)
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

client = gspread.authorize(creds)
sheet_name = os.getenv("GOOGLE_SHEET_NAME", "Class 6 Attendance")
sheet = client.open(sheet_name).sheet1

# Email config (from env for security)
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")


def update_sheet(name, roll, section):
    try:
        date = get_current_date()
        sheet.append_row([name, roll, section, date])
        print(f"✅ Updated sheet for {name} on {date}")
        return True
    except Exception as e:
        print(f"❌ Sheet update failed: {e}")
        return False


def send_full_sheet():
    try:
        client = gspread.authorize(creds)
        sheet = client.open(sheet_name).sheet1

        data = sheet.get_all_values()
        filename = f"Class6_Attendance_{get_current_date()}.csv"

        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)

        msg = EmailMessage()
        msg['Subject'] = f'Class 6 Attendance - {get_current_date()}'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = TO_EMAIL
        msg.set_content("Attached is the complete attendance record.")

        with open(filename, "rb") as f:
            msg.add_attachment(f.read(), maintype="text", subtype="csv", filename=filename)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        if os.path.exists(filename):
            os.remove(filename)

        print(f"✅ Full sheet sent on {get_current_date()}")
        return True
    except Exception as e:
        print(f"❌ Failed to send sheet: {e}")
        return False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/checkin")
def checkin():
    try:
        name = request.args.get('name')
        roll = request.args.get('id')
        section = request.args.get('section')

        if update_sheet(name, roll, section):
            return render_template(
                'scanned.html',
                name=name,
                roll=roll,
                section=section,
                date=get_current_date()
            )
        return "<h2>❌ Check-in failed</h2>"
    except Exception as e:
        return f"<h2>❌ Error: {str(e)}</h2>"


@app.route("/scan")
def scan():
    code = request.args.get('code')
    if code == 'STOP_SCAN':
        time.sleep(2)
        if send_full_sheet():
            return f"<h2>✅ Attendance Completed</h2><p>Full attendance sheet sent on {get_current_date()}</p>"
        return "<h2>❌ Failed to send attendance</h2>"
    return "<h2>❌ Invalid QR code</h2>"


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
