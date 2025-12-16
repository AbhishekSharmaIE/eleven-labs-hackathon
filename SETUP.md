# Setup Instructions

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Keys**
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys
   ```

3. **Start Services**
   ```bash
   ./start.sh
   ```

4. **Start Interview**
   ```bash
   python3 join_meeting_now.py "MEETING_URL"
   ```

## Required API Keys

- **ElevenLabs**: Get from https://elevenlabs.io
- **Ngrok**: Get from https://dashboard.ngrok.com
- **Recall.ai**: Get from https://recall.ai
- **Anam.ai**: Get from https://anam.ai
- **n8n**: Optional, for enhanced processing

## Environment Variables

All API keys should be set in `.env` file (see `.env.example`)

