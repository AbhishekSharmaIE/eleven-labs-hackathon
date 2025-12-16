#!/usr/bin/env python3
"""
Ngrok integration script to expose local server
"""
import subprocess
import requests
import time
import json
import sys
from pathlib import Path

def check_ngrok_installed():
    """Check if ngrok is installed"""
    script_dir = Path(__file__).parent
    local_ngrok = script_dir / 'ngrok'
    if local_ngrok.exists() and local_ngrok.is_file():
        try:
            subprocess.run([str(local_ngrok), 'version'], capture_output=True, check=True)
            return str(local_ngrok)
        except:
            pass
    try:
        subprocess.run(['ngrok', 'version'], capture_output=True, check=True)
        return 'ngrok'
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def install_ngrok():
    """Install ngrok if not available"""
    print("Ngrok not found. Installing...")
    try:
        # Try to install via package manager or download
        subprocess.run(['sudo', 'apt-get', 'update'], check=False)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'ngrok'], check=False)
        if check_ngrok_installed():
            return True
    except:
        pass
    
    print("Please install ngrok manually:")
    print("  Option 1: sudo apt-get install ngrok")
    print("  Option 2: Download from https://ngrok.com/download")
    return False

def start_ngrok_tunnel(port=5000):
    """Start ngrok tunnel for the specified port"""
    ngrok_path = check_ngrok_installed()
    if not ngrok_path:
        if not install_ngrok():
            return None
        ngrok_path = check_ngrok_installed()
        if not ngrok_path:
            return None
    
    print(f"Starting ngrok tunnel on port {port}...")
    
    # Start ngrok in background
    process = subprocess.Popen(
        [ngrok_path, 'http', str(port), '--log=stdout'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=Path(__file__).parent
    )
    
    # Wait a bit for ngrok to start
    time.sleep(3)
    
    # Get the public URL from ngrok API
    try:
        response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
        if response.status_code == 200:
            data = response.json()
            tunnels = data.get('tunnels', [])
            if tunnels:
                public_url = tunnels[0]['public_url']
                print(f"\n{'='*60}")
                print(f"✓ Ngrok tunnel active!")
                print(f"  Public URL: {public_url}")
                print(f"  Local URL: http://localhost:{port}")
                print(f"{'='*60}\n")
                return public_url
    except:
        pass
    
    print("Ngrok started but couldn't fetch URL. Check http://localhost:4040")
    return "http://localhost:4040"

def get_ngrok_url():
    """Get current ngrok URL"""
    try:
        response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
        if response.status_code == 200:
            data = response.json()
            tunnels = data.get('tunnels', [])
            if tunnels:
                return tunnels[0]['public_url']
    except:
        pass
    return None

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    url = start_ngrok_tunnel(port)
    if url:
        print(f"Webhook URL for Recall.ai: {url}/api/webhook/recall")
        print("\nPress Ctrl+C to stop ngrok")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping ngrok...")

