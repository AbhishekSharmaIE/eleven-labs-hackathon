#!/usr/bin/env python3
"""
n8n MCP Server integration
"""
import requests
import json
from config import N8N_MCP_URL, N8N_MCP_JWT

def send_to_n8n_mcp(data, endpoint="process-interview"):
    """Send data to n8n MCP server"""
    url = f"{N8N_MCP_URL}/{endpoint}"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {N8N_MCP_JWT}"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"n8n MCP error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error sending to n8n MCP: {e}")
        return None

def process_interview_with_n8n(interview_data):
    """Process interview data through n8n MCP"""
    payload = {
        "interview_id": interview_data.get("id"),
        "transcript": interview_data.get("transcript", ""),
        "timestamp": interview_data.get("timestamp"),
        "meeting_url": interview_data.get("meeting_url"),
        "raw_data": interview_data.get("raw_data", {})
    }
    
    return send_to_n8n_mcp(payload, "process-interview")

def get_enhanced_analysis(interview_id):
    """Get enhanced analysis from n8n"""
    return send_to_n8n_mcp({"interview_id": interview_id}, "get-analysis")

if __name__ == '__main__':
    # Test n8n MCP connection
    print("Testing n8n MCP connection...")
    test_data = {
        "id": "test_123",
        "transcript": "Test interview transcript",
        "timestamp": "2024-01-01T00:00:00"
    }
    result = process_interview_with_n8n(test_data)
    if result:
        print("✓ n8n MCP connected successfully!")
    else:
        print("✗ Failed to connect to n8n MCP")

