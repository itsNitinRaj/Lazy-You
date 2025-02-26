from utils import extract_meeting_start, schedule_alert, send_call_alert, scheduler
import imaplib
import email
from email.header import decode_header
import os
import datetime
from apscheduler.schedulers.background import BackgroundScheduler


from dotenv import load_dotenv
load_dotenv()


# --- Configuration ---
# Email credentials and server details
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
IMAP_SERVER = "imap.gmail.com"  # Adjust if you're not using Gmail

YOUR_NAME = os.environ.get("YOUR_NAME")

# Get today's date in the format "01-Jan-2022"
today = datetime.datetime.today().strftime("%d-%b-%Y")

# Email search criteria (for example, unseen emails with "meeting" in the subject)
SEARCH_CRITERIA =  f'(UNSEEN SINCE {today})'

# Polling interval in seconds
POLL_INTERVAL = os.environ.get("POLL_INTERVAL")


processed_email_ids = set()

# --- Main Email Check Function ---
def check_email():
    """Connects to the IMAP server, searches for unseen emails,
       and triggers or schedules an alert if a relevant email is found."""
    try:
        # Connect to the IMAP server and login
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        # Search for unseen emails
        status, messages = mail.search(None, SEARCH_CRITERIA)
        if status != "OK":
            print("Error searching for emails.")
            return

        email_ids = messages[0].split()
        for eid in email_ids:
            if eid in processed_email_ids:
                continue  # Skip already processed emails

            res, msg_data = mail.fetch(eid, "(BODY.PEEK[])")  # use 'RFC822' if you want to mark email as read
            if res != "OK":
                print("Error fetching email ID:", eid)
                continue

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Decode the email subject
            subject, encoding = decode_header(msg.get("Subject"))[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")

            # Determine if the subject contains a meeting invitation by trying to extract the meeting start time.
            if "invitation" in subject.lower() or YOUR_NAME in subject.lower():   # Adjust your keyword as you want. These keyword are in your subject.
                print(f"Processing email with subject: {subject}")
                try:
                    meeting_start = extract_meeting_start(subject)
                    schedule_alert(subject, meeting_start)
                except Exception as e:
                    print("Could not extract meeting time, triggering immediate alert. Error:", e)
                    send_call_alert(subject)
            else:
                print(f"Ignored email with subject: {subject}")

            # Add the email ID to the set of processed emails
            processed_email_ids.add(eid)


        mail.logout()
    except Exception as e:
        print("Exception in check_email:", e)


# --- Main Loop ---
if __name__ == "__main__":
    print("Starting email monitor...")
    try:
        while True:
            check_email()
            # time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("Shutting down scheduler and exiting...")
        scheduler.shutdown()



