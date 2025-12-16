#!/bin/bash
# Simple startup script for the interview system

cd "$(dirname "$0")"

echo "=========================================="
echo "Starting AI Interview System"
echo "=========================================="
echo ""

# Start API server
echo "Starting API server..."
python3 api_server.py > /tmp/api_server.log 2>&1 &
API_PID=$!
sleep 3
echo "✓ API server started (PID: $API_PID)"
echo "  Dashboard: http://localhost:5000/dashboard"
echo ""

# Start ngrok
echo "Starting ngrok tunnel..."
./ngrok http 5000 > /tmp/ngrok.log 2>&1 &
NGROK_PID=$!
sleep 5
echo "✓ Ngrok started (PID: $NGROK_PID)"
echo "  Check: http://localhost:4040"
echo ""

echo "=========================================="
echo "Services Running!"
echo "=========================================="
echo ""
echo "To start an interview:"
echo "  python3 join_meeting_now.py \"MEETING_URL\""
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for interrupt
trap "echo ''; echo 'Stopping services...'; kill $API_PID $NGROK_PID 2>/dev/null; exit" INT
wait


