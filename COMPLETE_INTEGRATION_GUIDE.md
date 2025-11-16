# 🎯 Complete PrepWise AI Integration Guide

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                          │
│           Next.js Frontend (Port 3000)                      │
└───────────┬──────────────────────────┬──────────────────────┘
            │                          │
            │ HTTP/REST                │ HTTP/REST
            ↓                          ↓
┌───────────────────────┐    ┌────────────────────────┐
│   Backend API         │    │   Voice API            │
│   (Port 8000)         │←───│   (Port 8001)          │
│   - FastAPI           │    │   - VAPI Integration   │
│   - Resume Parsing    │    │   - Transcription      │
│   - Question Gen      │    │   - Voice Recording    │
│   - Evaluation        │    └────────────────────────┘
└──────────┬────────────┘
           │ Python Import
           ↓
┌───────────────────────┐
│   PrepWise AI Engine  │
│   - NLP Processing    │
│   - OpenAI GPT-4      │
│   - Question Gen      │
│   - Evaluation        │
└───────────────────────┘
```

---

## 🚀 Quick Start

### One Command to Start Everything:

```bash
cd /Users/ankitrao/Claude-Hackathon
./START_ALL_SERVICES.sh
```

This starts:
1. ✅ Backend API (Port 8000)
2. ✅ Voice API (Port 8001)
3. ✅ Frontend (Port 3000)

### Stop Everything:

```bash
./STOP_ALL_SERVICES.sh
```

---

## 📊 Complete User Flow

### Flow 1: Text-Based Interview (Current)

```
1. User opens http://localhost:3000/interview-setup
2. (Optional) Upload Resume → Backend parses → Extracts info
3. Configure Interview:
   - Interview Type (Behavioral/Technical/Both)
   - Job Details
   - Difficulty
   - Number of Questions
4. Backend generates personalized questions using PrepWise AI
5. User types answers in interview session
6. Each answer evaluated by AI in real-time
7. View comprehensive results with:
   - Overall score
   - Strengths & weaknesses
   - Detailed feedback per question
   - Recommendations
```

### Flow 2: Voice-Based Interview (With Voice API)

```
1. User opens http://localhost:3000/interview-setup
2. Upload Resume → Backend parses
3. Configure Interview + Enable "Voice Mode"
4. Backend generates questions
5. For each question:
   a. Display question
   b. User records audio answer
   c. Audio sent to Voice API → Transcribed
   d. Transcription sent to Backend → Evaluated by AI
   e. Real-time feedback
6. View results with transcripts + evaluations
```

---

## 🔌 API Endpoints

### Backend API (Port 8000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/v1/ai/health` | GET | AI service health |
| `/api/v1/ai/parse-resume` | POST | Parse resume (PDF/DOCX) |
| `/api/v1/ai/generate-questions` | POST | Generate questions |
| `/api/v1/ai/evaluate-response` | POST | Evaluate single answer |
| `/api/v1/ai/evaluate-interview` | POST | Evaluate full interview |
| `/api/v1/voice/health` | GET | Voice API health check |
| `/api/v1/voice/transcribe` | POST | Transcribe audio |
| `/api/v1/voice/start-voice-interview` | POST | Init voice session |

### Voice API (Port 8001)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/transcribe` | POST | Transcribe audio file |
| `/config` | GET | Get configuration |

---

## 🧪 Testing

### Test Backend API:

```bash
# Health check
curl http://localhost:8000/health

# AI service check
curl http://localhost:8000/api/v1/ai/health

# Voice integration check
curl http://localhost:8000/api/v1/voice/health

# Generate questions
curl -X POST http://localhost:8000/api/v1/ai/generate-questions \
  -H "Content-Type: application/json" \
  -d '{
    "resume_data": {
      "name": "Test User",
      "skills": ["Python"],
      "experience": [],
      "education": []
    },
    "interview_type": "technical",
    "num_questions": 3
  }'
```

### Test Voice API:

```bash
# Health check
curl http://localhost:8001/health

# Check configuration
curl http://localhost:8001/config
```

---

## 🔧 Configuration

### Backend: `backend/.env`
```env
OPENAI_API_KEY=sk-proj-...  # ✅ Your key
API_VERSION=v1
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### Voice API: `voice-api/voice/.env`
```env
# VAPI Configuration (if using VAPI)
VAPI_API_KEY=your_vapi_key_here
TRANSCRIPTION_PROVIDER=vapi

# Or use OpenAI Whisper
OPENAI_API_KEY=sk-proj-...
TRANSCRIPTION_PROVIDER=whisper
```

### Frontend: `v0-interview-prep-app-main/.env.local`
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_VOICE_API_URL=http://localhost:8001
```

---

## 🎯 For Your Hackathon Demo

### Demo Script:

**1. Introduction (30 sec)**
- "PrepWise AI: Complete interview prep platform"
- "Powered by GPT-4, real-time evaluation, voice support"

**2. Resume Upload (1 min)**
- Upload resume → Show instant parsing
- "AI extracts: skills, experience, education"

**3. Interview Setup (30 sec)**
- Configure: Technical interview, 3 questions
- "Questions tailored to resume"

**4. Interview Session (2 min)**
- Show AI-generated questions
- Type/speak answers
- "Real-time evaluation as you go"

**5. Results & Feedback (1 min)**
- Overall score visualization
- Strengths/weaknesses breakdown
- "Actionable recommendations"

**Total Demo Time: ~5 minutes**

---

## 🛠️ Troubleshooting

### Backend won't start:
```bash
cd backend
source ../venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Voice API won't start:
```bash
cd voice-api/voice
python main.py
# Check logs in voice.log
```

### Frontend shows "Failed to generate questions":
1. Check backend is running: `curl http://localhost:8000/health`
2. Check browser console (F12) for errors
3. Restart backend: `./STOP_ALL_SERVICES.sh && ./START_ALL_SERVICES.sh`

### Question generation works in curl but not frontend:
- This has been fixed!
- Make sure you restarted the backend
- Clear browser cache and refresh

---

## 📦 What's Integrated

✅ **Backend Features:**
- Resume parsing (PDF/DOCX)
- AI question generation
- Response evaluation
- Full interview evaluation
- Voice API integration

✅ **Voice API Features:**
- Audio transcription (VAPI/Whisper)
- Voice interview support
- Real-time processing

✅ **Frontend Features:**
- Resume upload with drag-drop
- Interview configuration
- Live interview session
- Voice recording (ready for integration)
- Comprehensive results

---

## 🎉 You're All Set!

**Just run:**
```bash
./START_ALL_SERVICES.sh
```

**Then open:** http://localhost:3000/interview-setup

**Test the flow:**
1. Upload resume
2. Configure interview
3. Answer questions
4. View AI-powered results

**Good luck with your hackathon!** 🏆
