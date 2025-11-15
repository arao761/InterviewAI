# PrepWise - Full Stack Interview Preparation Platform

AI-powered interview preparation platform with resume parsing, mock interviews, and real-time feedback.

## Architecture

This is a full-stack application with three integrated components:

```
prepwise-fullstack/
├── backend/              # FastAPI backend API
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Core config, database
│   │   ├── models/      # Database models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic & AI integration
│   │   └── utils/       # Utilities
│   └── main.py
├── prepwise-ai/          # AI/NLP Module (integrated into backend)
│   ├── src/
│   │   ├── resume_parser/
│   │   ├── question_generator/
│   │   ├── evaluator/
│   │   └── api.py       # AI API interface
│   └── requirements.txt
├── v0-interview-prep-app-main/  # Next.js Frontend
│   ├── app/             # Next.js app directory
│   ├── components/      # React components
│   └── package.json
├── docker-compose.yml    # Unified development environment
└── README.md            # This file
```

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **AI/NLP**: OpenAI GPT-4, spaCy, LangChain

### Frontend
- **Framework**: Next.js 16
- **UI**: React 19, Radix UI, Tailwind CSS
- **Forms**: React Hook Form, Zod

### AI/NLP Module
- **LLM**: OpenAI GPT-4
- **Resume Parsing**: PyPDF2, python-docx
- **NLP**: spaCy

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- pnpm (or npm)
- Docker & Docker Compose (optional, recommended)

### Option 1: Docker Compose (Recommended)

```bash
# 1. Clone and navigate to project
cd /Users/ankitrao/Claude-Hackathon

# 2. Copy environment files
cp .env.example .env
cp backend/.env.example backend/.env
cp prepwise-ai/.env.example prepwise-ai/.env

# 3. Edit .env files with your API keys and configuration

# 4. Start all services
docker-compose up -d

# 5. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/v1/docs
```

### Option 2: Manual Setup

#### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install AI/NLP module dependencies
pip install -r ../prepwise-ai/requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Copy environment file and configure
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. Frontend Setup

```bash
cd v0-interview-prep-app-main

# Install dependencies
pnpm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
pnpm dev
```

## Environment Variables

### Backend (.env)
```env
# Application
APP_NAME=PrepWise API
ENVIRONMENT=development
DEBUG=True
API_VERSION=v1

# Server
HOST=0.0.0.0
PORT=8000
WORKERS=1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/prepwise

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# AI/NLP
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here  # Optional

# File Upload
MAX_UPLOAD_SIZE=10485760  # 10MB
UPLOAD_DIR=./uploads
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### AI Module (prepwise-ai/.env)
```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## API Endpoints

### Health & Info
- `GET /health` - Health check
- `GET /` - API information
- `GET /api/v1/docs` - Swagger documentation

### AI/NLP Endpoints
- `POST /api/v1/ai/parse-resume` - Parse resume (PDF/DOCX)
- `POST /api/v1/ai/generate-questions` - Generate interview questions
- `POST /api/v1/ai/evaluate-response` - Evaluate interview response
- `POST /api/v1/ai/evaluate-interview` - Evaluate full interview session

## Development Workflow

### 1. Backend Development
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Development
```bash
cd v0-interview-prep-app-main
pnpm dev
```

### 3. AI Module Development
```bash
cd prepwise-ai
source venv/bin/activate
pytest tests/
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### AI Module Tests
```bash
cd prepwise-ai
pytest tests/ --cov=src
```

### Frontend Tests
```bash
cd v0-interview-prep-app-main
pnpm test
```

## Deployment

### Backend
```bash
cd backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend
```bash
cd v0-interview-prep-app-main
pnpm build
pnpm start
```

## Project Structure Details

### Backend API Routes
- `/api/v1/ai/*` - AI/NLP endpoints (resume parsing, question generation, evaluation)
- `/api/v1/auth/*` - Authentication endpoints (future)
- `/api/v1/users/*` - User management (future)
- `/api/v1/interviews/*` - Interview session management (future)

### Frontend Pages
- `/` - Home page
- `/dashboard` - User dashboard
- `/interview` - Mock interview interface
- `/results` - Interview results and feedback

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests
4. Submit a pull request

## Team

- **Frontend**: Next.js, React, UI/UX
- **Backend**: FastAPI, Database, Integration
- **AI/NLP**: Resume Parsing, Question Generation, Evaluation

## License

MIT License - PrepWise Hackathon Project
