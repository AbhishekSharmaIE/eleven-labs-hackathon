# n8n Backend Integration Guide

## Overview

n8n backend is integrated into the interview system to provide enhanced workflow automation for processing interview data. The system supports both n8n Cloud MCP and local n8n instances.

## Architecture

```
Recall.ai Bot → Webhook → API Server → n8n Backend → Enhanced Processing → Dashboard
                                    ↓
                            (n8n Cloud MCP or Local n8n)
```

## n8n Backend Features

- **Enhanced Analysis**: Sentiment analysis, topic extraction, engagement scoring
- **Multiple Backends**: Works with n8n Cloud MCP or local n8n
- **Fallback Processing**: Enhanced local processing if n8n unavailable
- **Real-time Processing**: Processes interviews as they happen

## Setup n8n

### Option 1: Install via npm (Recommended)

```bash
# Install Node.js if not installed
sudo apt-get install nodejs npm

# Install n8n globally
sudo npm install -g n8n

# Start n8n
n8n start
```

### Option 2: Use Docker

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  n8nio/n8n
```

### Option 3: Use Python Setup Script

```bash
python3 n8n_setup.py
```

## Access n8n

Once n8n is running:
- **Web UI**: http://localhost:5678
- **API**: http://localhost:5678/api/v1

## Backend Service

The n8n backend service (`n8n_backend_service.py`) automatically:
- Tries n8n Cloud MCP first (if configured)
- Falls back to local n8n webhook
- Uses enhanced local processing as final fallback

### Enhanced Processing Includes:
- **Sentiment Analysis**: Positive/negative word detection
- **Topic Extraction**: Identifies discussed topics (languages, frameworks, etc.)
- **Engagement Scoring**: Calculates engagement level (high/medium/low)
- **Metadata Enrichment**: Adds processing timestamps and methods

## Import Workflow (Local n8n)

1. Open n8n at http://localhost:5678
2. Click "Workflows" → "Import from File"
3. Select `n8n_enhanced_workflow.json` (recommended) or `n8n_workflow.json`
4. Activate the workflow

## Workflow Components

### 1. Webhook Node
- **Path**: `/webhook/interview-webhook`
- **Method**: POST
- Receives interview data from API server

### 2. Process Interview Data Node
- Extracts transcript from various formats
- Processes metadata
- Formats data for analysis

### 3. Send to API Server Node
- Sends processed data to `/api/webhook/n8n`
- Triggers analysis

### 4. Respond to Webhook Node
- Returns success response

## Configuration

Set environment variable for n8n webhook URL:

```bash
export N8N_WEBHOOK_URL="http://localhost:5678/webhook/interview-webhook"
```

Or update in `api_server.py`:

```python
n8n_url = os.getenv('N8N_WEBHOOK_URL', 'http://localhost:5678/webhook/interview-webhook')
```

## Custom Workflows

You can extend the workflow to:
- Send notifications (email, Slack, etc.)
- Store data in databases
- Trigger additional analysis
- Generate reports
- Integrate with other services

## Testing

1. Start n8n: `n8n start`
2. Import workflow from `n8n_workflow.json`
3. Activate workflow
4. Test webhook:
```bash
curl -X POST http://localhost:5678/webhook/interview-webhook \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Test interview transcript", "bot_id": "test123"}'
```

## Troubleshooting

- **n8n not starting**: Check if port 5678 is available
- **Workflow not triggering**: Verify webhook URL in API server
- **Data not processing**: Check n8n execution logs

