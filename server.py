from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route("/answer", methods=["POST"])
def answer():
    """Twilio calls this when the call connects."""
    response = VoiceResponse()

    # Greet and pause to let the agent respond
    response.say(
        "Hello, I'd like to schedule an appointment please.",
        voice="Polly.Joanna"  # sounds more natural than default
    )

    # Listen for up to 10 seconds of agent speech
    response.pause(length=10)

    # Then say something else to keep the call alive
    response.say(
        "I'm sorry, can you repeat that?",
        voice="Polly.Joanna"
    )

    response.pause(length=8)

    # Hang up
    response.say("Thank you, goodbye.", voice="Polly.Joanna")

    return Response(str(response), mimetype="text/xml")


@app.route("/recording", methods=["POST"])
def recording():
    """Twilio posts recording info here when call ends."""
    recording_url = request.form.get("RecordingUrl")
    call_sid = request.form.get("CallSid")
    print(f"Recording ready: {recording_url}")
    print(f"Call SID: {call_sid}")
    return Response("OK", status=200)


if __name__ == "__main__":
    app.run(port=5000, debug=True)