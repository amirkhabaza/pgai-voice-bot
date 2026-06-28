import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

def make_call(webhook_base_url: str):
    call = client.calls.create(
        to=os.getenv("TARGET_NUMBER"),
        from_=os.getenv("TWILIO_PHONE_NUMBER"),
        url=f"{webhook_base_url}/answer",        # Twilio fetches TwiML from here
        record=True,
        recording_status_callback=f"{webhook_base_url}/recording",
    )
    print(f"Call initiated. SID: {call.sid}")
    return call.sid

if __name__ == "__main__":
    # Replace with your ngrok URL each time you start ngrok
    NGROK_URL = "https://YOUR-NGROK-URL-HERE.ngrok-free.app"
    make_call(NGROK_URL)