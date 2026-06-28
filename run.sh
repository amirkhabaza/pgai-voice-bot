#!/bin/bash
# run.sh — starts ngrok, the Flask server, waits for tunnel, then places the call

set -e

echo "Starting Flask server..."
python server.py &
SERVER_PID=$!

echo "Starting ngrok tunnel..."
ngrok http 5000 --log=stdout --log-format=json > /tmp/ngrok.log &
NGROK_PID=$!

echo "Waiting for ngrok tunnel to be ready..."
sleep 3

# Extract the public URL from ngrok's local API
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "
import sys, json
tunnels = json.load(sys.stdin)['tunnels']
for t in tunnels:
    if t['proto'] == 'https':
        print(t['public_url'])
        break
")

if [ -z "$NGROK_URL" ]; then
    echo "Error: Could not get ngrok URL. Is ngrok installed and authenticated?"
    kill $SERVER_PID $NGROK_PID 2>/dev/null
    exit 1
fi

echo "Tunnel ready: $NGROK_URL"

# Inject the URL into the call
NGROK_URL=$NGROK_URL python main.py

echo ""
echo "Call placed. Watch above for live conversation."
echo "Press Ctrl+C to stop the server when done."

wait $SERVER_PID
