# Lazy-You

Lazy-You is a Python-based project designed to monitor your email inbox for meeting invitations and send you alerts via phone calls using Twilio. This project is particularly useful for those who want to ensure they never miss an important meeting while working from home (or sleeping while working from home).

## Features

- Monitors your email inbox for meeting invitations.
- Extracts meeting start times from email subjects.
- Schedules phone call alerts 30 minutes before the meeting starts.
- Uses Twilio API to make phone calls with custom voice messages.

## Requirements

- Python 3.11.5
- Twilio account and phone number
- Gmail account (or modify for other IMAP servers)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/lazy-wfh.git
    cd lazy-wfh
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Copy the `.env.example` file to `.env` and fill in your credentials:

    ```sh
    cp .env.example .env
    ```

## Usage

1. Ensure your `.env` file is correctly configured with your email and Twilio credentials.

2. Run the main script:

    ```sh
    python main.py
    ```

The script will start monitoring your email inbox and schedule phone call alerts for any meeting invitations it finds.

## Configuration

- **Email Credentials**: Set your email user and password in the `.env` file. You need your *email address* and an *app password* (if required) to log in via IMAP.
    
    🔹 Gmail Users -
    
    1. Go to [Google App Passwords](https://myaccount.google.com/apppasswords).
    2. Select *"Mail"* as the app and *"Other"* as the device.
    3. Generate a password and store it safely.
    4. Use this app password as `EMAIL_PASS`.
    
    🔹 Outlook / Hotmail Users -
       
    1. Go to [Microsoft Security Settings](https://account.live.com/proofs/Manage).
    2. Generate an app password.
    3. Use it instead of your normal password.
    
    🔹 Other Email Providers - Check if they require *App Passwords* or *OAuth authentication*.

- **Twilio Credentials**: Set your Twilio account SID, auth token, and phone numbers in the `.env` file.
- **Polling Interval**: Adjust the polling interval in the `.env` file to control how frequently the script checks for new emails.


## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

