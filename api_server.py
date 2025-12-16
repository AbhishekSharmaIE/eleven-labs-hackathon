#!/usr/bin/env python3
"""
Backend API server for interview analysis and dashboard
Handles webhooks from Recall.ai and provides interview data
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import requests
from datetime import datetime
from pathlib import Path
import re

# Import integrations
try:
    from n8n_backend_service import N8NBackendService
    n8n_backend_service = N8NBackendService()
    N8N_AVAILABLE = True
except:
    try:
        from n8n_backend import N8NBackend
        n8n_backend_service = N8NBackend()
        N8N_AVAILABLE = True
    except:
        try:
            from n8n_mcp_integration import process_interview_with_n8n, get_enhanced_analysis
            n8n_backend_service = None
            N8N_AVAILABLE = True
        except:
            N8N_AVAILABLE = False
            n8n_backend_service = None

try:
    from config import N8N_MCP_URL, ELEVENLABS_API_KEY
except:
    N8N_MCP_URL = None
    ELEVENLABS_API_KEY = None

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Store interview data
interviews_db = []
DATA_FILE = Path(__file__).parent / "interviews_data.json"

def load_interviews():
    """Load interviews from file"""
    global interviews_db
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r') as f:
                interviews_db = json.load(f)
        except:
            interviews_db = []
    return interviews_db

def save_interviews():
    """Save interviews to file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(interviews_db, f, indent=2)

def analyze_interview(transcript_text, audio_duration=None):
    """Enhanced interview analysis with software developer focus"""
    if not transcript_text:
        return {
            "score": 0,
            "summary": "No transcript available",
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "detailed_metrics": {}
        }
    
    text_lower = transcript_text.lower()
    words = transcript_text.split()
    word_count = len(words)
    
    # Enhanced technical keywords for software developers
    programming_languages = ['python', 'javascript', 'java', 'c++', 'c#', 'go', 'rust', 'typescript', 
                            'ruby', 'php', 'swift', 'kotlin', 'scala', 'dart', 'r', 'matlab']
    
    frameworks = ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'node', 
                 'laravel', 'rails', 'next', 'nuxt', 'nest', 'fastapi']
    
    technical_concepts = ['api', 'rest', 'graphql', 'microservices', 'docker', 'kubernetes', 
                         'aws', 'azure', 'gcp', 'database', 'sql', 'nosql', 'mongodb', 
                         'postgresql', 'redis', 'elasticsearch', 'git', 'ci/cd', 'devops',
                         'agile', 'scrum', 'tdd', 'testing', 'unit test', 'integration test',
                         'algorithm', 'data structure', 'big o', 'optimization', 'scalability',
                         'security', 'authentication', 'authorization', 'oauth', 'jwt']
    
    soft_skills = ['team', 'collaboration', 'communication', 'leadership', 'mentor', 
                   'code review', 'pair programming', 'scrum master', 'product owner']
    
    problem_solving = ['problem', 'solution', 'approach', 'challenge', 'solve', 'debug',
                      'troubleshoot', 'optimize', 'refactor', 'architecture', 'design pattern']
    
    # Count keyword mentions
    lang_score = sum(1 for lang in programming_languages if lang in text_lower)
    framework_score = sum(1 for fw in frameworks if fw in text_lower)
    tech_score = sum(1 for tech in technical_concepts if tech in text_lower)
    soft_score = sum(1 for skill in soft_skills if skill in text_lower)
    problem_score = sum(1 for ps in problem_solving if ps in text_lower)
    
    # Calculate detailed metrics
    technical_depth = lang_score + framework_score + tech_score
    communication_quality = soft_score + (word_count / 50)  # More words = better communication
    problem_solving_ability = problem_score
    
    # Advanced scoring algorithm
    technical_weight = 0.4
    communication_weight = 0.3
    problem_solving_weight = 0.2
    engagement_weight = 0.1
    
    technical_ratio = min(1.0, technical_depth / 15)  # Normalize to 0-1
    communication_ratio = min(1.0, communication_quality / 20)
    problem_ratio = min(1.0, problem_solving_ability / 10)
    engagement_ratio = min(1.0, word_count / 500)
    
    score = int((
        technical_ratio * technical_weight +
        communication_ratio * communication_weight +
        problem_ratio * problem_solving_weight +
        engagement_ratio * engagement_weight
    ) * 100)
    
    # Generate detailed strengths
    strengths = []
    if lang_score >= 2:
        strengths.append(f"Demonstrates knowledge of {lang_score} programming languages")
    if framework_score >= 2:
        strengths.append(f"Familiar with {framework_score} frameworks/libraries")
    if tech_score >= 5:
        strengths.append("Strong understanding of technical concepts and best practices")
    if soft_score >= 3:
        strengths.append("Good soft skills and team collaboration experience")
    if problem_score >= 3:
        strengths.append("Shows strong problem-solving and analytical thinking")
    if word_count > 400:
        strengths.append("Provides detailed and comprehensive answers")
    if not strengths:
        strengths.append("Participated actively in the interview")
    
    # Generate detailed weaknesses
    weaknesses = []
    if lang_score < 1:
        weaknesses.append("Limited discussion of specific programming languages")
    if framework_score < 1:
        weaknesses.append("Could mention more frameworks and tools")
    if tech_score < 3:
        weaknesses.append("Needs deeper technical discussion")
    if soft_score < 2:
        weaknesses.append("Could emphasize more on teamwork and collaboration")
    if problem_score < 2:
        weaknesses.append("Limited demonstration of problem-solving process")
    if word_count < 150:
        weaknesses.append("Responses were too brief - provide more detail")
    
    # Generate actionable recommendations
    recommendations = []
    if technical_depth < 10:
        recommendations.append("Prepare specific examples of projects using different technologies")
        recommendations.append("Be ready to discuss system architecture and design decisions")
    if communication_quality < 10:
        recommendations.append("Practice explaining complex technical concepts in simple terms")
        recommendations.append("Prepare STAR method examples (Situation, Task, Action, Result)")
    if problem_score < 3:
        recommendations.append("Prepare examples of challenging problems you've solved")
        recommendations.append("Practice walking through your problem-solving process")
    if word_count < 200:
        recommendations.append("Provide more detailed answers with concrete examples")
    if not recommendations:
        recommendations.append("Continue building on current strengths")
        recommendations.append("Consider contributing to open source projects")
    
    # Generate comprehensive summary
    summary = f"Comprehensive interview analysis for Software Developer position. "
    summary += f"Analyzed {word_count} words over {audio_duration or 'unknown'} duration. "
    summary += f"Technical depth: {'Excellent' if technical_depth >= 15 else 'Good' if technical_depth >= 8 else 'Needs improvement'}. "
    summary += f"Communication: {'Excellent' if communication_quality >= 15 else 'Good' if communication_quality >= 8 else 'Needs improvement'}. "
    summary += f"Problem-solving: {'Strong' if problem_score >= 5 else 'Moderate' if problem_score >= 3 else 'Limited'}. "
    summary += f"Overall performance score: {score}/100."
    
    return {
        "score": score,
        "summary": summary,
        "metrics": {
            "word_count": word_count,
            "audio_duration": audio_duration,
            "technical_depth": technical_depth,
            "programming_languages_mentioned": lang_score,
            "frameworks_mentioned": framework_score,
            "technical_concepts": tech_score,
            "soft_skills_demonstrated": soft_score,
            "problem_solving_examples": problem_score
        },
        "detailed_metrics": {
            "technical_ratio": round(technical_ratio, 2),
            "communication_ratio": round(communication_ratio, 2),
            "problem_solving_ratio": round(problem_ratio, 2),
            "engagement_ratio": round(engagement_ratio, 2)
        },
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
        "transcript": transcript_text
    }

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory('.', 'dashboard.html')

@app.route('/api/webhook/recall', methods=['POST'])
def recall_webhook():
    """Webhook endpoint for Recall.ai to send interview data"""
    try:
        data = request.json or {}
        print(f"\n{'='*60}")
        print(f"📥 Received webhook from Recall.ai")
        print(f"{'='*60}")
        print(f"Data keys: {list(data.keys())}")
        
        # Extract transcript from various possible formats
        transcript_text = ""
        
        # Format 1: Direct transcript string
        if 'transcript' in data:
            if isinstance(data['transcript'], str):
                transcript_text = data['transcript']
            elif isinstance(data['transcript'], list):
                # Join transcript segments
                transcript_text = " ".join([seg.get('text', '') if isinstance(seg, dict) else str(seg) for seg in data['transcript']])
        
        # Format 2: Realtime transcription events
        if 'event' in data and data.get('event') == 'transcription':
            if 'text' in data:
                transcript_text = data['text']
            elif 'transcript' in data:
                transcript_text = data['transcript']
        
        # Format 3: Recording data with transcript
        if 'recording' in data:
            recording = data['recording']
            if 'transcript' in recording:
                if isinstance(recording['transcript'], str):
                    transcript_text = recording['transcript']
                elif isinstance(recording['transcript'], list):
                    transcript_text = " ".join([seg.get('text', '') if isinstance(seg, dict) else str(seg) for seg in recording['transcript']])
        
        # Format 4: Messages array (common in realtime)
        if 'messages' in data and isinstance(data['messages'], list):
            transcript_parts = []
            for msg in data['messages']:
                if isinstance(msg, dict):
                    text = msg.get('text') or msg.get('transcript') or msg.get('content', '')
                    if text:
                        transcript_parts.append(text)
                elif isinstance(msg, str):
                    transcript_parts.append(msg)
            transcript_text = " ".join(transcript_parts)
        
        # Format 5: Participant events
        if 'participant' in data and 'transcript' in data.get('participant', {}):
            transcript_text = data['participant']['transcript']
        
        # If still no transcript, try to extract from any text fields
        if not transcript_text:
            for key in ['text', 'content', 'message', 'utterance']:
                if key in data:
                    transcript_text = str(data[key])
                    break
        
        print(f"📝 Extracted transcript: {len(transcript_text)} characters")
        if transcript_text:
            print(f"Preview: {transcript_text[:100]}...")
        
        # Extract audio duration
        audio_duration = data.get('duration') or data.get('audio_duration') or data.get('recording_duration')
        
        # Extract meeting/bot info
        bot_id = data.get('bot_id') or data.get('id') or data.get('bot', {}).get('id')
        meeting_url = data.get('meeting_url') or data.get('meeting', {}).get('url')
        
        print(f"🎤 Audio duration: {audio_duration}")
        print(f"🤖 Bot ID: {bot_id}")
        print(f"📹 Meeting: {meeting_url}")
        
        # Only process if we have transcript data
        if not transcript_text and not audio_duration:
            print("⚠️  No transcript or audio data, skipping analysis")
            return jsonify({"status": "received", "message": "No transcript data yet"}), 200
        
        # Analyze the interview
        print("🔍 Analyzing interview...")
        analysis = analyze_interview(transcript_text, audio_duration)
        print(f"✅ Analysis complete - Score: {analysis['score']}/100")
        
        # Create or update interview record
        interview_id = bot_id or f"interview_{datetime.now().timestamp()}"
        
        # Check if interview already exists
        existing_interview = None
        for idx, inv in enumerate(interviews_db):
            if inv.get('id') == interview_id or inv.get('bot_id') == bot_id:
                existing_interview = idx
                break
        
        if existing_interview is not None:
            # Update existing interview
            interview = interviews_db[existing_interview]
            # Append new transcript to existing
            if transcript_text:
                existing_transcript = interview.get('transcript', '')
                interview['transcript'] = existing_transcript + " " + transcript_text if existing_transcript else transcript_text
            # Update analysis with combined data
            interview['analysis'] = analyze_interview(interview['transcript'], audio_duration or interview.get('audio_duration'))
            interview['last_updated'] = datetime.now().isoformat()
            interview['raw_data'].append(data)  # Append new data
            print(f"📝 Updated existing interview: {interview_id}")
        else:
            # Create new interview record
            interview = {
                "id": interview_id,
                "bot_id": bot_id,
                "timestamp": datetime.now().isoformat(),
                "meeting_url": meeting_url,
                "transcript": transcript_text,
                "analysis": analysis,
                "raw_data": [data],
                "audio_duration": audio_duration
            }
            interviews_db.append(interview)
            print(f"✨ Created new interview: {interview_id}")
        
        # Save to database
        save_interviews()
        print(f"💾 Saved interview data to {DATA_FILE}")
        
        # Forward to n8n backend for enhanced processing
        if N8N_AVAILABLE and n8n_backend_service:
            try:
                print("🔄 Processing via n8n backend...")
                enhanced_result = n8n_backend_service.process_interview_data(interview)
                if enhanced_result and enhanced_result.get('n8n_enhanced'):
                    interview['n8n_enhanced'] = enhanced_result.get('n8n_enhanced')
                    save_interviews()
                    print("✅ n8n backend processing complete")
            except Exception as e:
                print(f"⚠️  n8n backend processing error: {e}")
        
        # Also try local n8n webhook
        n8n_url = os.getenv('N8N_WEBHOOK_URL', 'http://localhost:5678/webhook/interview-webhook')
        try:
            requests.post(n8n_url, json=interview, timeout=2)
        except:
            pass  # n8n not available, continue anyway
        
        print(f"{'='*60}\n")
        
        return jsonify({
            "status": "success",
            "interview_id": interview["id"],
            "transcript_length": len(transcript_text),
            "score": analysis['score'],
            "message": "Interview data processed and analyzed"
        }), 200
        
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/webhook/n8n', methods=['POST'])
def n8n_webhook():
    """Webhook endpoint for n8n to send processed interview data"""
    try:
        data = request.json
        interview_data = data.get('interview_data', data)
        
        # Extract transcript
        transcript_text = interview_data.get('transcript', '')
        audio_duration = interview_data.get('duration')
        
        # Analyze the interview
        analysis = analyze_interview(transcript_text, audio_duration)
        
        # Create interview record
        interview = {
            "id": interview_data.get('bot_id') or interview_data.get('id') or f"interview_{datetime.now().timestamp()}",
            "timestamp": interview_data.get('timestamp', datetime.now().isoformat()),
            "meeting_url": interview_data.get('meeting_url'),
            "transcript": transcript_text,
            "analysis": analysis,
            "raw_data": interview_data,
            "processed_by": "n8n"
        }
        
        # Save to database
        interviews_db.append(interview)
        save_interviews()
        
        return jsonify({
            "status": "success",
            "interview_id": interview["id"],
            "analysis": analysis
        }), 200
        
    except Exception as e:
        print(f"n8n webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/interviews', methods=['GET'])
def get_interviews():
    """Get all interviews"""
    load_interviews()
    return jsonify(interviews_db)

@app.route('/api/interviews/<interview_id>', methods=['GET'])
def get_interview(interview_id):
    """Get specific interview by ID"""
    load_interviews()
    interview = next((i for i in interviews_db if i['id'] == interview_id), None)
    if interview:
        return jsonify(interview)
    return jsonify({"error": "Interview not found"}), 404

@app.route('/api/interviews/latest', methods=['GET'])
def get_latest_interview():
    """Get the most recent interview"""
    load_interviews()
    if interviews_db:
        return jsonify(interviews_db[-1])
    return jsonify({"error": "No interviews found"}), 404

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "interviews_count": len(interviews_db)})

if __name__ == '__main__':
    load_interviews()
    print(f"\n{'='*60}")
    print("API Server starting on http://localhost:5000")
    print("Endpoints:")
    print("  - GET  /api/interviews - List all interviews")
    print("  - GET  /api/interviews/latest - Get latest interview")
    print("  - POST /api/webhook/recall - Recall.ai webhook")
    print("  - GET  /dashboard - Interview dashboard")
    print(f"{'='*60}\n")
    app.run(host='0.0.0.0', port=5000, debug=True)

