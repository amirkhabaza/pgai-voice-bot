# PGAI Voice Bot — Patient Simulator

An automated voice bot that calls the Pretty Good AI test line, simulates realistic patient conversations using Claude as the patient brain, and records + transcribes every call for bug analysis.

## Setup

**Prerequisites:** Python 3.10+, [ngrok](https://ngrok.com) installed and authenticated, Twilio paid account.

```bash
git clone https://github.com/YOUR_USERNAME/pgai-voice-bot.git
cd pgai-voice-bot
pip install -r requirements.txt
cp .env.example .env   # then fill in your credentials
```

## Run

```bash
bash run.sh
```

That's it. The script starts the Flask webhook server, opens an ngrok tunnel, auto-detects the public URL, and places the call. Watch the terminal for the live conversation. Transcripts save automatically to `transcripts/` when each call ends.

**To run a different patient scenario:** edit `PATIENT_SYSTEM_PROMPT` at the top of `server.py`, then run `bash run.sh` again.

> **Windows users:** Run the three steps manually — `python server.py` in one terminal, 
> `ngrok http 5000` in another, then set `NGROK_URL` in your environment and run `python main.py`.

## Environment Variables

Copy `.env.example` to `.env` and fill in:

| Variable | Description |
|----------|-------------|
| `TWILIO_ACCOUNT_SID` | Twilio Account SID (starts with AC) |
| `TWILIO_AUTH_TOKEN` | Twilio Auth Token |
| `TWILIO_PHONE_NUMBER` | Your Twilio number in E.164 format |
| `TARGET_NUMBER` | Test line: +18054398008 |
| `DEEPGRAM_API_KEY` | Deepgram API key |
| `ANTHROPIC_API_KEY` | Anthropic API key (Claude) |

## Loom Videos

- [Walkthrough — Approach & What I Built](https://www.loom.com/share/6b5c8840b58045648f03da73882299f0)
- [AI Debugging Session](https://www.loom.com/share/23cd441c1242400fa59ce1cbeb8a2c16)

## Project Structure

```
pgai-voice-bot/
├── run.sh              # Single-command launcher
├── server.py           # Flask webhook — STT + Claude + TTS loop
├── main.py             # Places outbound call via Twilio
├── .env.example        # Credentials template
├── requirements.txt    # Python dependencies
├── README.md
├── ARCHITECTURE.md     # Design decisions
├── BUG_REPORT.md       # Issues found during testing
├── transcripts/        # Auto-saved call transcripts (JSON)
└── recordings/         # MP3 recordings of all calls
```

## Cost Estimate

Under $5 total for 10 calls across all APIs.
