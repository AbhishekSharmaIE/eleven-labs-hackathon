#!/usr/bin/env python3
"""
Enhanced Recall.ai bot script for interview capture
Configures bot to capture audio/transcript and send to webhook
"""
import requests
import json
import sys
import os

# Configuration
MEETING_URL = os.getenv("MEETING_URL", "https://meet.google.com/zif-cudw-mph")
API_TOKEN = os.getenv("RECALL_API_TOKEN", "")
API_BASE_URL = "https://us-west-2.recall.ai"
API_ENDPOINT = f"{API_BASE_URL}/api/v1/bot/"

# Get webhook URL from environment or ngrok
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://localhost:5000/api/webhook/recall")

def create_interview_bot(meeting_url, webhook_url, camera_url=None):
    """Create a Recall.ai bot configured for interview capture"""
    
    # Default camera URL - use the local server with Sarah interface
    if not camera_url:
        camera_url = webhook_url.replace('/api/webhook/recall', '/index.html')
    
    payload = {
        "meeting_url": meeting_url,
        "bot_name": "AI Interviewer - Sarah",
        "output_media": {
            "camera": {
                "kind": "webpage",
                "config": {
                    "url": camera_url,
                    "width": 1920,
                    "height": 1080
                }
            }
        },
        "variant": {
            "google_meet": "web_4_core"
        },
        "recording_config": {
            "transcript": {
                "provider": {
                    "recallai_streaming": {
                        "mode": "prioritize_low_latency",
                        "language_code": "en"
                    }
                }
            },
            "include_bot_in_recording": {
                "audio": True,
                "video": True
            },
            "video_mixed_layout": "speaker_view"
        },
        "realtime_media": {
            "transcription": {
                "provider": {
                    "recallai_streaming": {
                        "language_code": "en"
                    }
                },
                "destination": "webhook",
                "webhook": {
                    "url": webhook_url,
                    "method": "POST"
                }
            }
        },
        "automatic_leave": {
            "waiting_room_timeout": 3600,  # Wait up to 1 hour in waiting room
            "noone_joined_timeout": 3600,  # Stay even if no one joins for 1 hour
            "everyone_left_timeout": {
                "timeout": 300  # Leave only if everyone left for 5 minutes
            },
            "in_call_not_recording_timeout": 7200,  # Stay in call for 2 hours
            "recording_permission_denied_timeout": 60
        }
    }
    
    headers = {
        "Authorization": f"Token {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    return requests.post(API_ENDPOINT, json=payload, headers=headers)

def main():
    print(f"{'='*60}")
    print("AI Interview Bot Setup")
    print(f"{'='*60}\n")
    print(f"Meeting URL: {MEETING_URL}")
    print(f"Webhook URL: {WEBHOOK_URL}")
    print(f"\nCreating bot...\n")
    
    try:
        response = create_interview_bot(MEETING_URL, WEBHOOK_URL)
        
        if response.status_code == 201:
            bot_data = response.json()
            print("✓ Bot successfully created!")
            print(f"\nBot ID: {bot_data.get('id')}")
            print(f"Status: {bot_data.get('status', 'active')}")
            print(f"\nBot will:")
            print("  - Join the Google Meet meeting")
            print("  - Stream Sarah (AI interviewer) as video")
            print("  - Capture audio and transcript")
            print("  - Send transcript data to webhook for analysis")
            print(f"\nView dashboard at: {WEBHOOK_URL.replace('/api/webhook/recall', '/dashboard')}")
            print(f"\nResponse:")
            print(json.dumps(bot_data, indent=2))
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"Response: {response.text}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Request failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

