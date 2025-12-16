#!/usr/bin/env python3
"""
n8n setup and integration script
"""
import subprocess
import requests
import time
import json
import os
from pathlib import Path

def check_n8n_installed():
    """Check if n8n is installed"""
    try:
        result = subprocess.run(['n8n', '--version'], capture_output=True, check=True, text=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_n8n():
    """Install n8n using npm"""
    print("Installing n8n...")
    try:
        # Check if npm is available
        subprocess.run(['npm', '--version'], check=True, capture_output=True)
        
        # Install n8n globally
        print("Installing n8n via npm (this may take a few minutes)...")
        subprocess.run(['sudo', 'npm', 'install', '-g', 'n8n'], check=False)
        
        if check_n8n_installed():
            return True
    except FileNotFoundError:
        print("npm not found. Please install Node.js and npm first:")
        print("  sudo apt-get install nodejs npm")
        print("  or visit https://nodejs.org/")
    except:
        pass
    
    return False

def start_n8n(port=5678):
    """Start n8n server"""
    if not check_n8n_installed():
        if not install_n8n():
            print("\nPlease install n8n manually:")
            print("  npm install -g n8n")
            return None
    
    print(f"Starting n8n on port {port}...")
    process = subprocess.Popen(
        ['n8n', 'start', '--port', str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=Path(__file__).parent
    )
    
    # Wait for n8n to start
    time.sleep(5)
    
    # Check if n8n is running
    try:
        response = requests.get(f'http://localhost:{port}/healthz', timeout=5)
        if response.status_code == 200:
            print(f"\n{'='*60}")
            print(f"✓ n8n is running!")
            print(f"  Web UI: http://localhost:{port}")
            print(f"  API: http://localhost:{port}/api/v1")
            print(f"{'='*60}\n")
            return process
    except:
        pass
    
    print("n8n starting... Check http://localhost:5678")
    return process

def import_workflow(workflow_file, n8n_url="http://localhost:5678"):
    """Import n8n workflow from JSON file"""
    try:
        with open(workflow_file, 'r') as f:
            workflow = json.load(f)
        
        # Import via n8n API (requires authentication in production)
        print(f"Workflow file ready: {workflow_file}")
        print("Import manually via n8n UI or use n8n CLI")
        return True
    except Exception as e:
        print(f"Error importing workflow: {e}")
        return False

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5678
    process = start_n8n(port)
    
    if process:
        workflow_file = Path(__file__).parent / "n8n_workflow.json"
        if workflow_file.exists():
            import_workflow(workflow_file)
        
        print("\nPress Ctrl+C to stop n8n")
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\nStopping n8n...")
            process.terminate()

