# AI Interview System with Analysis Dashboard

A complete AI-powered interview system that conducts interviews via Google Meet, captures audio/transcript, and provides real-time analysis with a comprehensive dashboard.

## Features

- 🤖 **AI Interviewer (Sarah)** - AI persona that conducts technical interviews
- 📹 **Google Meet Integration** - Bot joins meetings and streams AI interviewer
- 🎤 **Audio & Transcript Capture** - Records all interview conversations
- 📊 **Real-time Analysis** - Analyzes interview performance with AI insights
- 📈 **Dashboard Reports** - Beautiful dashboard with scores, strengths, weaknesses
- 🌐 **Ngrok Integration** - Expose local server for webhook callbacks
- 🔄 **n8n Integration** - Workflow automation for enhanced processing

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Edit `config.py` with your API keys:
- ElevenLabs API Key
- Ngrok Token
- n8n MCP credentials
- Recall.ai API Token
- Anam.ai API Key (in `index.html`)

### 3. Start Services

**Terminal 1 - API Server:**
```bash
python3 api_server.py
```

**Terminal 2 - Ngrok:**
```bash
./ngrok http 5000
```

### 4. Start Interview

```bash
python3 join_meeting_now.py "https://meet.google.com/your-meeting-id"
```

Or create a new meeting:
```bash
python3 join_meeting_now.py
```

### 5. View Dashboard

- Local: http://localhost:5000/dashboard
- Public: Check ngrok URL (http://localhost:4040)

## Project Structure

```
prototype-main/
├── api_server.py           # Main Flask API server
├── interview_bot.py        # Recall.ai bot creation
├── join_meeting_now.py     # Main script to start interviews
├── config.py               # API keys and configuration
├── index.html              # Sarah AI interviewer interface
├── dashboard.html          # Analysis dashboard
├── ngrok_setup.py          # Ngrok tunnel management
├── n8n_setup.py            # n8n installation/setup
├── n8n_mcp_integration.py  # n8n MCP server integration
├── elevenlabs_integration.py # ElevenLabs voice synthesis
├── n8n_workflow.json       # n8n workflow definition
├── requirements.txt        # Python dependencies
├── interviews_data.json    # Stored interview data
├── ngrok                   # Ngrok binary
└── README.md               # This file
```

## Configuration

### Environment Variables

```bash
export RECALL_API_TOKEN="your-recall-api-token"
export MEETING_URL="https://meet.google.com/your-meeting"
export WEBHOOK_URL="https://your-ngrok-url.ngrok.io/api/webhook/recall"
```

### API Keys

Update in `config.py`:
- `ELEVENLABS_API_KEY`
- `NGROK_TOKEN`
- `N8N_MCP_URL`
- `N8N_MCP_JWT`

Update in `index.html` (line 139):
- `ANAM_API_KEY`

## API Endpoints

- `GET /` - Sarah interview interface
- `GET /dashboard` - Analysis dashboard
- `POST /api/webhook/recall` - Recall.ai webhook
- `POST /api/webhook/n8n` - n8n webhook
- `GET /api/interviews` - List all interviews
- `GET /api/interviews/latest` - Get latest interview
- `GET /api/health` - Health check

## Interview Analysis

The system analyzes interviews based on:
- **Technical Keywords** - Programming languages, frameworks, concepts
- **Communication Skills** - Clarity, explanation quality, examples
- **Problem Solving** - Approach, strategy, optimization discussions
- **Response Length** - Detail and comprehensiveness

### Scoring (0-100)
- **70-100**: Excellent performance
- **50-69**: Good performance with room for improvement
- **0-49**: Needs significant improvement

## Troubleshooting

### Ngrok Not Working
- Get auth token: https://dashboard.ngrok.com/get-started/your-authtoken
- Configure: `./ngrok config add-authtoken YOUR_TOKEN`

### Bot Not Joining
- Verify meeting URL is correct
- Check Recall.ai API token is valid
- Ensure meeting allows guests/bots
- Create new meeting with waiting room OFF

### Sarah Not Speaking
- Check Anam.ai API key in `index.html`
- Verify camera URL is accessible via ngrok
- Bot may be in audio-only mode (still captures transcript)

### Dashboard Not Loading
- Ensure API server is running on port 5000
- Check browser console for errors
- Verify `/api/interviews` endpoint is accessible

## Documentation

- **README.md** - This file (main documentation)
- **N8N_INTEGRATION.md** - n8n setup and usage
- **HACKATHON_FEATURES.md** - Feature list and technical details

## License

This is a prototype project for hackathon purposes.
