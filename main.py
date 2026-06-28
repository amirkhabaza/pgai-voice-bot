"""Makes the outbound call via Twilio."""

import os

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
from_number = os.environ["TWILIO_PHONE_NUMBER"]
to_number = os.environ["TARGET_NUMBER"]
webhook_base_url = os.environ.get("WEBHOOK_BASE_URL", "http://localhost:5000")

client = Client(account_sid, auth_token)

if __name__ == "__main__":
    call = client.calls.create(
        to=to_number,
        from_=from_number,
        url=f"{webhook_base_url}/voice",
    )
    print(f"Call initiated: {call.sid}")
