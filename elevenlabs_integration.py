#!/usr/bin/env python3
"""
ElevenLabs API integration for voice synthesis
"""
import requests
import json
from config import ELEVENLABS_API_KEY, ELEVENLABS_API_URL

def synthesize_speech(text, voice_id="21m00Tcm4TlvDq8ikWAM", model_id="eleven_monolingual_v1"):
    """Synthesize speech using ElevenLabs API"""
    url = f"{ELEVENLABS_API_URL}/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.content  # Audio bytes
        else:
            print(f"ElevenLabs API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error synthesizing speech: {e}")
        return None

def get_voices():
    """Get available voices from ElevenLabs"""
    url = f"{ELEVENLABS_API_URL}/voices"
    headers = {"xi-api-key": ELEVENLABS_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error getting voices: {e}")
        return None

if __name__ == '__main__':
    # Test ElevenLabs connection
    print("Testing ElevenLabs API...")
    voices = get_voices()
    if voices:
        print(f"✓ Connected! Available voices: {len(voices.get('voices', []))}")
    else:
        print("✗ Failed to connect to ElevenLabs API")

