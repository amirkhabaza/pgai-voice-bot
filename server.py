import os
import json
import httpx
import anthropic
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from deepgram import DeepgramClient
from dotenv import load_dotenv
import re


load_dotenv()

app = Flask(__name__)
deepgram = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))
claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Store conversation history per call
conversations = {}

PATIENT_SYSTEM_PROMPT = """You are a patient calling a medical office AI assistant.

Your persona: Jennifer Mills, 50 years old.
Your goal: You think you're calling your regular GP office but this is actually an orthopedics office.

Rules:
- Keep responses SHORT — 1-2 sentences max
- Start by asking about a dermatology referral
- When they clarify this is orthopedics, act surprised
- Then pivot and ask if they can refer you somewhere for dermatology
- Then ask if you can still schedule something for a wrist issue you have
- DOB: April 27, 1975
- Phone: 650-555-0789
- When resolved, say goodbye naturally
"""


def clean_response(text: str) -> str:
    """Remove stage directions Claude sometimes adds e.g. *listens to greeting*"""
    text = re.sub(r'\*[^*]+\*', '', text)
    return text.strip()

def transcribe_audio(recording_url: str) -> str:
    """Download Twilio recording and transcribe with Deepgram."""
    try:
        # Download the recording from Twilio
        auth = (os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        audio_response = httpx.get(f"{recording_url}.mp3", auth=auth)
        
        # Send to Deepgram
        response = deepgram.listen.v1.media.transcribe_file(
            request=audio_response.content,
            model="nova-2",
            smart_format=True,
        )
        
        transcript = response.results.channels[0].alternatives[0].transcript
        return transcript.strip()
    except Exception as e:
        print(f"Transcription error: {e}")
        return ""

def get_claude_response(call_sid: str, agent_said: str) -> str:
    """Get Claude's response as the patient."""
    if call_sid not in conversations:
        conversations[call_sid] = []
    
    # Add agent's message to history
    if agent_said:
        conversations[call_sid].append({
            "role": "user", 
            "content": f"The agent said: {agent_said}"
        })
    else:
        # First turn — agent just picked up
        conversations[call_sid].append({
            "role": "user",
            "content": "The phone just connected. The agent is greeting you."
        })
    
    response = claude.messages.create(
        model="claude-haiku-4-5",
        max_tokens=150,
        system=PATIENT_SYSTEM_PROMPT,
        messages=conversations[call_sid]
    )
    
    patient_response = response.content[0].text
    
    # Add Claude's response to history
    conversations[call_sid].append({
        "role": "assistant",
        "content": patient_response
    })
    
    print(f"\n[{call_sid[-6:]}] Agent: {agent_said}")
    print(f"[{call_sid[-6:]}] Patient: {patient_response}\n")
    
    return patient_response


@app.route("/answer", methods=["POST"])
def answer():
    """Called when the call connects — start the conversation."""
    call_sid = request.form.get("CallSid")
    response = VoiceResponse()
    
    # Get Claude's opening line as the patient
    opening = get_claude_response(call_sid, "")
    
    # Use Gather to listen for the agent's response
    gather = Gather(
        input="speech",
        action="/agent_spoke",
        method="POST",
        speech_timeout="auto",
        timeout=10,
    )
    gather.say(opening, voice="Polly.Joanna")
    response.append(gather)
    
    # If gather times out (agent didn't speak), hang up
    response.say("I didn't hear anything. Goodbye.", voice="Polly.Joanna")
    response.hangup()
    
    return Response(str(response), mimetype="text/xml")


@app.route("/agent_spoke", methods=["POST"])
def agent_spoke():
    """Called after the agent speaks — transcribe, think, respond."""
    call_sid = request.form.get("CallSid")
    
    # Twilio's built-in speech recognition (backup if Deepgram fails)
    agent_text = request.form.get("SpeechResult", "")
    confidence = request.form.get("Confidence", "0")
    
    print(f"[Twilio STT] Agent said: '{agent_text}' (confidence: {confidence})")
    
    response = VoiceResponse()
    
    # If we got a transcript, generate patient response
    if agent_text:
        patient_reply = clean_response(get_claude_response(call_sid, agent_text))
        
        # Check if conversation should end
        end_words = ["goodbye", "bye", "thank you for calling", "have a great day"]
        should_end = any(word in patient_reply.lower() for word in end_words)
        
        if should_end:
            response.say(patient_reply, voice="Polly.Joanna")
            response.pause(length=1)
            response.hangup()
        else:
            # Keep listening for agent's next response
            gather = Gather(
                input="speech",
                action="/agent_spoke",
                method="POST",
                speech_timeout="auto",
                timeout=10,
            )
            gather.say(patient_reply, voice="Polly.Joanna")
            response.append(gather)
            response.say("I see. Thank you, goodbye.", voice="Polly.Joanna")
            response.hangup()
    else:
        # Nothing heard — wrap up
        response.say("Sorry, I couldn't hear you. I'll try again later. Goodbye.", voice="Polly.Joanna")
        response.hangup()
    
    return Response(str(response), mimetype="text/xml")


@app.route("/recording", methods=["POST"])
def recording():
    """Called when recording is ready."""
    recording_url = request.form.get("RecordingUrl")
    call_sid = request.form.get("CallSid")
    duration = request.form.get("RecordingDuration")
    print(f"\n Recording ready!")
    print(f"Call SID: {call_sid}")
    print(f"Duration: {duration}s")
    print(f"URL: {recording_url}.mp3")
    
    # Save transcript to file
    if call_sid in conversations:
        os.makedirs("transcripts", exist_ok=True)
        with open(f"transcripts/{call_sid}.json", "w") as f:
            json.dump(conversations[call_sid], f, indent=2)
        print(f"Transcript saved: transcripts/{call_sid}.json")
    
    return Response("OK", status=200)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
