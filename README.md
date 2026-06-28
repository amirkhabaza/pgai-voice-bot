# PGAI Voice Bot — Patient Simulator

An automated voice bot that calls the Pretty Good AI test line (+1-805-439-8008), simulates realistic patient conversations using Claude as the patient brain, and records/transcribes every call for bug analysis.

## Architecture

See `ARCHITECTURE.md` for a full explanation of design decisions.

## Requirements

- Python 3.10+
- A Twilio account (paid, not trial) with a voice-capable phone number
- A Deepgram account (free tier sufficient)
- An Anthropic API key
- ngrok (for local webhook tunneling)

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/pgai-voice-bot.git
cd pgai-voice-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1XXXXXXXXXX
TARGET_NUMBER=+18054398008
DEEPGRAM_API_KEY=your_deepgram_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

### 4. Start ngrok

In a dedicated terminal:

```bash
ngrok http 5000
```

Copy the `https://xxxx.ngrok-free.app` URL — you'll need it in the next step.

### 5. Configure the webhook URL

Open `main.py` and set your ngrok URL:

```python
NGROK_URL = "https://your-ngrok-url.ngrok-free.app"
```

### 6. Run

Open two terminals:

**Terminal 1 — start the webhook server:**
```bash
python server.py
```

**Terminal 2 — place a call:**
```bash
python main.py
```

That's it. Watch Terminal 1 for the live conversation. Transcripts auto-save to `transcripts/` when each call ends.

## Changing Scenarios

To run a different patient scenario, edit the `PATIENT_SYSTEM_PROMPT` variable at the top of `server.py`, save the file (Flask auto-reloads), then run `python main.py` again.

## Output

- `transcripts/<CallSID>.json` — full conversation history per call (both sides)
- Recording URL printed to console after each call (Twilio-hosted MP3)

## Project Structure

```
pgai-voice-bot/
├── server.py           # Flask webhook server (STT + LLM + TTS logic)
├── main.py             # Places outbound calls via Twilio
├── .env                # Your credentials (never commit this)
├── .env.example        # Template showing required variables
├── requirements.txt    # Python dependencies
├── transcripts/        # Auto-generated call transcripts (JSON)
├── recordings/         # Downloaded MP3 recordings (if fetched)
├── BUG_REPORT.md       # Documented issues found during testing
└── ARCHITECTURE.md     # Design decisions and system overview
```

## Environment Variables Reference

| Variable | Description |
|----------|-------------|
| `TWILIO_ACCOUNT_SID` | Your Twilio Account SID (starts with AC) |
| `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token |
| `TWILIO_PHONE_NUMBER` | Your Twilio phone number in E.164 format |
| `TARGET_NUMBER` | The test line to call (+18054398008) |
| `DEEPGRAM_API_KEY` | Deepgram API key for transcription |
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude (patient brain) |

## Cost Estimate

Typical cost for 10 calls: under $5 total across all APIs.
