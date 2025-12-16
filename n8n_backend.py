#!/usr/bin/env python3
"""
n8n Backend Service - Processes interview data through n8n workflows
"""
import requests
import json
import os
from datetime import datetime
from config import N8N_MCP_URL, N8N_MCP_JWT

class N8NBackend:
    """n8n Backend for interview processing"""
    
    def __init__(self, mcp_url=None, jwt=None):
        self.mcp_url = mcp_url or N8N_MCP_URL
        self.jwt = jwt or N8N_MCP_JWT
        self.local_webhook = os.getenv('N8N_WEBHOOK_URL', 'http://localhost:5678/webhook/interview-webhook')
    
    def send_to_mcp(self, data, endpoint="process-interview"):
        """Send data to n8n MCP server"""
        if not self.mcp_url:
            return None
        
        # n8n cloud MCP uses HTTP endpoint directly
        # The MCP URL is the base, we send data to it
        url = self.mcp_url
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.jwt}"
        }
        
        # Wrap data for n8n processing
        payload = {
            "method": endpoint,
            "params": data
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                result = response.json()
                return result.get('result') if isinstance(result, dict) else result
            else:
                # Try direct POST to the URL
                response = requests.post(url, json=data, headers=headers, timeout=10)
                if response.status_code == 200:
                    return response.json()
                print(f"n8n MCP error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error sending to n8n MCP: {e}")
            return None
    
    def send_to_local_webhook(self, data):
        """Send data to local n8n webhook"""
        try:
            response = requests.post(self.local_webhook, json=data, timeout=5)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def process_interview(self, interview_data):
        """Process interview through n8n backend"""
        # Try MCP first, then local webhook
        result = None
        
        if self.mcp_url and self.jwt:
            print("🔄 Processing via n8n MCP...")
            result = self.send_to_mcp({
                "interview_id": interview_data.get("id"),
                "transcript": interview_data.get("transcript", ""),
                "timestamp": interview_data.get("timestamp"),
                "meeting_url": interview_data.get("meeting_url"),
                "analysis": interview_data.get("analysis", {}),
                "raw_data": interview_data.get("raw_data", {})
            }, "process-interview")
        
        if not result:
            print("🔄 Trying local n8n webhook...")
            result = self.send_to_local_webhook(interview_data)
        
        return result
    
    def enhance_analysis(self, interview_id, transcript):
        """Get enhanced analysis from n8n"""
        if self.mcp_url and self.jwt:
            return self.send_to_mcp({
                "interview_id": interview_id,
                "transcript": transcript
            }, "get-analysis")
        return None
    
    def generate_report(self, interview_id):
        """Generate comprehensive report via n8n"""
        if self.mcp_url and self.jwt:
            return self.send_to_mcp({
                "interview_id": interview_id
            }, "generate-report")
        return None

if __name__ == '__main__':
    backend = N8NBackend()
    print("Testing n8n backend...")
    test_data = {
        "id": "test_123",
        "transcript": "Test interview transcript for n8n processing",
        "timestamp": datetime.now().isoformat()
    }
    result = backend.process_interview(test_data)
    if result:
        print("✅ n8n backend working!")
    else:
        print("⚠️  n8n backend not available (this is okay if n8n isn't running)")

