#!/usr/bin/env python3
"""
Configuration file for API keys and tokens
Loads from environment variables for security
"""
import os

# ElevenLabs API
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_API_URL = os.getenv("ELEVENLABS_API_URL", "https://api.elevenlabs.io/v1")

# Ngrok Token
NGROK_TOKEN = os.getenv("NGROK_TOKEN", "")

# n8n MCP Server
N8N_MCP_URL = os.getenv("N8N_MCP_URL", "")
N8N_MCP_JWT = os.getenv("N8N_MCP_JWT", "")

# Recall.ai
RECALL_API_TOKEN = os.getenv("RECALL_API_TOKEN", "")

# Anam.ai
ANAM_API_KEY = os.getenv("ANAM_API_KEY", "")
