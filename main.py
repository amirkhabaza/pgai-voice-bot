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
        url=f"{webhook_base_url}/answer",
        record=True,
        recording_status_callback=f"{webhook_base_url}/recording",
    )
    print(f"Call initiated. SID: {call.sid}")
    return call.sid

if __name__ == "__main__":
    # Read from env (set by run.sh) or fall back to manual override
    ngrok_url = os.getenv("NGROK_URL") or "https://YOUR-NGROK-URL-HERE.ngrok-free.app"
    make_call(ngrok_url)