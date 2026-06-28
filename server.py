"""Flask webhook server Twilio talks to."""

import os

from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse

load_dotenv()

app = Flask(__name__)
RECORDINGS_DIR = os.path.join(os.path.dirname(__file__), "recordings")
os.makedirs(RECORDINGS_DIR, exist_ok=True)


@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    response.say("Hello. This is your Pretty Good AI voice bot.")
    return str(response), 200, {"Content-Type": "text/xml"}


@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
