# --- Helper Functions ---
import os
import re
import datetime
from twilio.rest import Client
import pytz
from apscheduler.schedulers.background import BackgroundScheduler

from dotenv import load_dotenv
load_dotenv()

# Define the timezone for meeting times. In this example, IST (Asia/Kolkata)
MEETING_TZ = pytz.timezone("Asia/Kolkata")

# Twilio configuration (store credentials in environment variables for safety)
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER")  # Your Twilio phone number
YOUR_PHONE_NUMBER  = os.environ.get("YOUR_PHONE_NUMBER")  # The number to alert


# Set up the scheduler (runs in the background)
scheduler = BackgroundScheduler()
scheduler.start()


def extract_meeting_start(subject):
    """
    Extracts the meeting start time from the email subject.
    Handles cases like "11:45am" and "1pm".
    """
    match = re.search(r"@ ([^-]+) -", subject)
    if not match:
        raise ValueError("Unable to extract meeting time from subject.")

    start_time_str = match.group(1).strip()

    # Normalize "1pm" to "1:00pm" only when missing minutes
    time_match = re.search(r"(\d{1,2})([ap]m)", start_time_str)
    if time_match and ":" not in start_time_str:
      start_time_str = re.sub(r"(\d{1,2})([ap]m)", r"\1:00\2", start_time_str)

    dt_format = "%a %b %d, %Y %I:%M%p"  # ✅ Correct format

    try:
        naive_dt = datetime.datetime.strptime(start_time_str, dt_format)
    except Exception as e:
        raise ValueError(f"Error parsing datetime: {e}")

    aware_dt = MEETING_TZ.localize(naive_dt)
    return aware_dt


def send_call_alert(email_subject):
    """Uses Twilio's API to initiate a phone call with a custom voice message."""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        # message = f"Alert: New email received with subject: {email_subject}"
        # # The TwiML instructs Twilio to speak the message.
        # twiml = f'<Response><Say voice="alice">{message}</Say></Response>'

        call = client.calls.create(
            url="https://handler.twilio.com/twiml/EH75bafc11b0ccc138af6af13b04f493a2",
            to=YOUR_PHONE_NUMBER,
            from_=TWILIO_FROM_NUMBER
        )
        print(f"Call initiated with SID: {call.sid}")
    except Exception as e:
        print("Exception in send_call_alert:", e)


def schedule_alert(email_subject, meeting_start):
    """
    Schedules a call alert 10 minutes before the meeting start time.
    If the scheduled alert time has already passed, it triggers the call immediately.
    """
    alert_time = meeting_start - datetime.timedelta(minutes=30)
    now = datetime.datetime.now(MEETING_TZ)

    if alert_time <= now:
        print("Alert time has already passed. Triggering alert immediately.")
        send_call_alert(email_subject)
    else:
        print(f"Scheduling call alert at {alert_time.strftime('%Y-%m-%d %H:%M:%S %Z')} for meeting: {email_subject}")
        scheduler.add_job(send_call_alert, 'date', run_date=alert_time, args=[email_subject])
