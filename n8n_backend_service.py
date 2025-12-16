#!/usr/bin/env python3
"""
n8n Backend Service - Standalone service for processing interviews
Can work with n8n cloud MCP or local n8n instance
"""
import requests
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from config import N8N_MCP_URL, N8N_MCP_JWT
except:
    N8N_MCP_URL = None
    N8N_MCP_JWT = None

class N8NBackendService:
    """n8n Backend Service for interview processing"""
    
    def __init__(self):
        self.mcp_url = N8N_MCP_URL
        self.jwt = N8N_MCP_JWT
        self.local_webhook = os.getenv('N8N_WEBHOOK_URL', 'http://localhost:5678/webhook/interview-webhook')
        self.api_url = os.getenv('API_URL', 'http://localhost:5000')
    
    def process_interview_data(self, interview_data):
        """Process interview data through n8n backend"""
        print(f"\n{'='*60}")
        print("🔄 n8n Backend Processing")
        print(f"{'='*60}")
        
        # Try n8n cloud MCP first
        if self.mcp_url and self.jwt:
            print("📡 Attempting n8n Cloud MCP...")
            result = self._send_to_cloud_mcp(interview_data)
            if result:
                print("✅ Processed via n8n Cloud MCP")
                return result
        
        # Try local n8n webhook
        print("📡 Attempting local n8n webhook...")
        result = self._send_to_local_webhook(interview_data)
        if result:
            print("✅ Processed via local n8n")
            return result
        
        # Fallback: Enhanced processing without n8n
        print("📡 Using enhanced local processing...")
        return self._enhanced_local_processing(interview_data)
    
    def _send_to_cloud_mcp(self, data):
        """Send to n8n cloud MCP server"""
        try:
            # n8n cloud MCP expects data in specific format
            payload = {
                "interview_id": data.get("id"),
                "transcript": data.get("transcript", ""),
                "timestamp": data.get("timestamp"),
                "meeting_url": data.get("meeting_url"),
                "analysis": data.get("analysis", {}),
                "metrics": data.get("analysis", {}).get("metrics", {}),
                "raw_data": data.get("raw_data", {})
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.jwt}"
            }
            
            response = requests.post(self.mcp_url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"   Error: {e}")
            return None
    
    def _send_to_local_webhook(self, data):
        """Send to local n8n webhook"""
        try:
            response = requests.post(self.local_webhook, json=data, timeout=5)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def _enhanced_local_processing(self, data):
        """Enhanced processing without n8n (fallback)"""
        transcript = data.get("transcript", "")
        analysis = data.get("analysis", {})
        
        # Additional processing
        enhanced = {
            "sentiment_analysis": self._analyze_sentiment(transcript),
            "topic_extraction": self._extract_topics(transcript),
            "engagement_score": self._calculate_engagement(transcript),
            "processed_at": datetime.now().isoformat(),
            "processing_method": "local-enhanced"
        }
        
        return {
            **data,
            "n8n_enhanced": enhanced
        }
    
    def _analyze_sentiment(self, text):
        """Simple sentiment analysis"""
        text_lower = text.lower()
        positive = ['excellent', 'great', 'success', 'achieved', 'improved', 'solved', 'optimized', 'love', 'enjoy']
        negative = ['difficult', 'challenge', 'problem', 'issue', 'failed', 'struggled', 'hard', 'complex']
        
        pos_count = sum(1 for w in positive if w in text_lower)
        neg_count = sum(1 for w in negative if w in text_lower)
        
        score = pos_count - neg_count
        return {
            "score": score,
            "positive_words": pos_count,
            "negative_words": neg_count,
            "sentiment": "positive" if score > 0 else "negative" if score < 0 else "neutral"
        }
    
    def _extract_topics(self, text):
        """Extract key topics from transcript"""
        text_lower = text.lower()
        topics = []
        
        topic_keywords = {
            "Programming Languages": ["python", "javascript", "java", "c++", "typescript", "go", "rust"],
            "Frameworks": ["react", "django", "flask", "spring", "angular", "vue", "express"],
            "Databases": ["database", "sql", "postgresql", "mongodb", "redis", "mysql"],
            "APIs": ["api", "rest", "graphql", "endpoint", "microservice"],
            "Cloud": ["aws", "azure", "gcp", "cloud", "docker", "kubernetes", "devops"],
            "Testing": ["test", "testing", "unit test", "integration", "qa"],
            "Architecture": ["architecture", "design pattern", "system design", "scalability"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(kw in text_lower for kw in keywords):
                topics.append(topic)
        
        return topics
    
    def _calculate_engagement(self, text):
        """Calculate engagement level"""
        word_count = len(text.split())
        question_count = text.count('?')
        
        if word_count > 500 and question_count > 5:
            return "high"
        elif word_count > 200 and question_count > 2:
            return "medium"
        else:
            return "low"

def main():
    """Test the n8n backend service"""
    service = N8NBackendService()
    
    test_data = {
        "id": "test_backend_123",
        "transcript": "I have been working as a software developer for 5 years. I'm proficient in Python, JavaScript, and React. I've worked with AWS and Docker.",
        "timestamp": datetime.now().isoformat(),
        "analysis": {"score": 75}
    }
    
    print("Testing n8n Backend Service...\n")
    result = service.process_interview_data(test_data)
    
    if result:
        print("\n✅ Backend processing successful!")
        print(f"Enhanced data keys: {list(result.get('n8n_enhanced', {}).keys())}")
    else:
        print("\n⚠️  Backend processing completed with fallback")

if __name__ == '__main__':
    main()


