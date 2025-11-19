# PrepWise AI

An AI-powered interview preparation platform that helps candidates practice and improve their interview skills with personalized feedback.

## What is PrepWise?

InterviewAI is a comprehensive interview preparation tool that uses artificial intelligence to provide a realistic interview experience. The platform offers:

### Key Features

**Resume Parsing & Analysis**
- Upload your resume (PDF/DOCX) and get instant parsing
- Automatic extraction of skills, experience, and education
- Personalized question generation based on your background

**AI-Powered Mock Interviews**
- Behavioral and technical interview questions
- Questions tailored to your experience level and target role
- Multiple difficulty levels and customizable interview length

**Real-Time Evaluation & Feedback**
- AI evaluation of each response
- Detailed scoring with strengths and weaknesses
- Personalized improvement recommendations

**Comprehensive Results**
- Overall performance metrics
- Question-by-question breakdown
- Actionable suggestions for improvement

## Tech Stack

**Frontend:** Next.js 16, React 19, TypeScript, Tailwind CSS

**Backend:** FastAPI (Python), SQLAlchemy

**AI/NLP:** OpenAI GPT-4, Custom evaluation engine

**File Processing:** PDF/DOCX parsing with intelligent text extraction

## Quick Start

```bash
# 1. Start all services
./START_HACKATHON.sh

# 2. Open the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/v1/docs
```

To stop all services:
```bash
./STOP_HACKATHON.sh
```

## Project Structure

```
├── backend/                    # FastAPI REST API
├── prepwise-ai/               # AI/NLP processing engine
├── v0-interview-prep-app-main/ # Next.js frontend
└── SETUP_PROJECT.sh           # Initial setup script
```

## License

MIT License
