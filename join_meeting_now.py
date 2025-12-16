#!/usr/bin/env python3
"""
Join meeting immediately - Sarah will be present in the meeting
"""
import requests
import json
import sys
import os
from config import RECALL_API_TOKEN

API_BASE_URL = "https://us-west-2.recall.ai"
API_ENDPOINT = f"{API_BASE_URL}/api/v1/bot/"

def create_immediate_join_bot(meeting_url, webhook_url, ngrok_url=None):
    """Create bot that joins immediately with Sarah's video and audio"""
    
    # Get camera URL - Sarah's interface
    if ngrok_url:
        camera_url = f"{ngrok_url}/index.html"
    else:
        camera_url = webhook_url.replace('/api/webhook/recall', '/index.html')
    
    # Test if camera URL is accessible
    camera_accessible = False
    try:
        test_resp = requests.get(camera_url, timeout=5)
        if test_resp.status_code == 200:
            camera_accessible = True
            print(f"✅ Camera URL accessible: {camera_url}")
        else:
            print(f"⚠️  Camera URL returned {test_resp.status_code}")
    except Exception as e:
        print(f"⚠️  Camera URL test failed: {e}")
    
    # Build payload with camera for Sarah's video
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
            "waiting_room_timeout": 7200,
            "noone_joined_timeout": 7200,
            "everyone_left_timeout": {
                "timeout": 600
            },
            "in_call_not_recording_timeout": 10800,
            "recording_permission_denied_timeout": 120
        }
    }
    
    headers = {
        "Authorization": f"Token {RECALL_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    if not camera_accessible:
        print(f"⚠️  Warning: Camera URL may not be accessible, but trying anyway...")
        print(f"   URL: {camera_url}")
        print(f"   Make sure ngrok is running and API server is accessible")
    
    return requests.post(API_ENDPOINT, json=payload, headers=headers)

def main():
    print(f"\n{'='*70}")
    print("🤖 Sarah AI Bot - Joining Meeting Now")
    print(f"{'='*70}\n")
    
    # Get meeting URL
    if len(sys.argv) > 1:
        meeting_url = sys.argv[1]
    else:
        print("📝 IMPORTANT: Create a NEW Google Meet meeting with these settings:")
        print("   1. Go to: https://meet.google.com/new")
        print("   2. Click 'Create meeting'")
        print("   3. Click 'Settings' (gear icon)")
        print("   4. Turn OFF 'Require participants to be admitted'")
        print("   5. Copy the meeting link\n")
        meeting_url = input("Enter the NEW Google Meet URL: ").strip()
        if not meeting_url:
            print("❌ Meeting URL required")
            return
    
    # Get webhook URL and ngrok URL
    ngrok_url = None
    try:
        ngrok_resp = requests.get('http://localhost:4040/api/tunnels', timeout=3)
        if ngrok_resp.status_code == 200:
            ngrok_data = ngrok_resp.json()
            tunnels = ngrok_data.get('tunnels', [])
            if tunnels:
                ngrok_url = tunnels[0]['public_url']
                webhook_url = f"{ngrok_url}/api/webhook/recall"
                print(f"✅ Using ngrok URL: {ngrok_url}\n")
            else:
                webhook_url = "http://localhost:5000/api/webhook/recall"
                print("⚠️  Using localhost (webhooks may not work from external services)\n")
        else:
            webhook_url = "http://localhost:5000/api/webhook/recall"
    except:
        webhook_url = "http://localhost:5000/api/webhook/recall"
        print("⚠️  Ngrok not running, using localhost\n")
    
    print(f"📹 Meeting: {meeting_url}")
    print(f"🔗 Webhook: {webhook_url}")
    if ngrok_url:
        print(f"📹 Sarah's Camera: {ngrok_url}/index.html")
    print(f"\n🚀 Creating bot... Sarah will join with video and audio!\n")
    
    try:
        response = create_immediate_join_bot(meeting_url, webhook_url, ngrok_url)
        
        if response.status_code == 201:
            bot_data = response.json()
            print("✅ SUCCESS! Sarah is joining the meeting now!")
            print(f"\n🤖 Bot Details:")
            print(f"   ID: {bot_data.get('id')}")
            print(f"   Status: {bot_data.get('status', 'active')}")
            print(f"   Name: AI Interviewer - Sarah")
            
            print(f"\n📹 YOUR MEETING LINK:")
            print(f"   👉 {meeting_url}")
            print(f"\n💡 Sarah will:")
            print(f"   ✅ Join the meeting automatically")
            print(f"   ✅ Be present when you join")
            print(f"   ✅ Start the interview when you're ready")
            print(f"   ✅ Record and analyze everything")
            
            print(f"\n📊 Watch Dashboard:")
            if 'ngrok_url' in locals():
                print(f"   {ngrok_url}/dashboard")
            print(f"   http://localhost:5000/dashboard")
            
            print(f"\n🎤 Next Steps:")
            print(f"   1. Open the meeting link: {meeting_url}")
            print(f"   2. Join the meeting (Sarah should already be there!)")
            print(f"   3. Start talking - Sarah will conduct the interview")
            print(f"   4. Watch the dashboard for real-time analysis")
            print(f"\n{'='*70}\n")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    import requests
    main()

