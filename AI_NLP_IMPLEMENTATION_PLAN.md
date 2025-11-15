# PrepWise AI/NLP Implementation Plan
**AI Interview Preparation Platform - Intelligence Layer**

**Role:** Person 4 - AI/NLP Engineer
**Last Updated:** 2025-11-15
**Project:** PrepWise Hackathon

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Architecture Overview](#architecture-overview)
3. [Phased Implementation Plan](#phased-implementation-plan)
4. [Potential Problems & Mitigations](#potential-problems--mitigations)
5. [MVP vs Enhancement Features](#mvp-vs-enhancement-features)
6. [Dependencies & Integration Points](#dependencies--integration-points)
7. [Recommended Timeline](#recommended-timeline)
8. [Success Metrics](#success-metrics)
9. [Technology Decisions](#technology-decisions)
10. [Critical Success Factors](#critical-success-factors)
11. [Next Steps](#next-steps)

---

## Executive Summary

Building the intelligence layer for PrepWise - an AI interview prep platform that combines resume parsing, mock behavioral and technical interviews, and real-time voice feedback through multimodal AI (VAPI).

**Core Responsibilities:**
- Resume parsing and structured data extraction
- Behavioral question generation (STAR framework)
- Technical question generation (4 domains)
- Response evaluation (behavioral + technical)
- Feedback generation and scoring

**Technology Stack:**
- **Primary Language:** Python
- **LLM APIs:** OpenAI GPT-4 / Anthropic Claude
- **Resume Parsing:** PyPDF2, python-docx
- **NLP:** spaCy, LangChain (optional)
- **Data Processing:** Pandas, NumPy, Pydantic
- **Evaluation:** LLM-based + custom algorithms

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    AI/NLP MODULE                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────────┐                   │
│  │   Resume     │───▶│  Question        │                   │
│  │   Parser     │    │  Generator       │                   │
│  └──────────────┘    └──────────────────┘                   │
│         │                     │                              │
│         ▼                     ▼                              │
│  ┌──────────────┐    ┌──────────────────┐                   │
│  │  Structured  │    │  Behavioral +    │                   │
│  │  Resume JSON │    │  Technical Qs    │                   │
│  └──────────────┘    └──────────────────┘                   │
│                              │                               │
│                              ▼                               │
│                      ┌──────────────────┐                    │
│                      │   Response       │                    │
│                      │   Evaluator      │                    │
│                      └──────────────────┘                    │
│                              │                               │
│                              ▼                               │
│                      ┌──────────────────┐                    │
│                      │  Feedback +      │                    │
│                      │  Scoring Engine  │                    │
│                      └──────────────────┘                    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
                   ┌─────────────────┐
                   │  Person 2's     │
                   │  Backend API    │
                   └─────────────────┘
```

**Data Flow:**
1. User uploads resume (PDF/DOCX) → Parse to structured JSON
2. Generate personalized questions (behavioral + technical)
3. User answers via VAPI → Get transcript
4. Evaluate response → Generate scores and feedback
5. Compile overall performance report

---

## Phased Implementation Plan

### **PHASE 1: Foundation & Setup** ⏱️ 2-3 hours
**Priority:** CRITICAL (MVP)

#### 1.1 Project Structure
```
prepwise-ai/
├── src/
│   ├── __init__.py
│   ├── resume_parser/
│   │   ├── __init__.py
│   │   ├── extractors.py      # PDF/DOCX extraction
│   │   ├── parser.py           # LLM-based entity extraction
│   │   └── schemas.py          # Pydantic models
│   ├── question_generator/
│   │   ├── __init__.py
│   │   ├── behavioral.py       # STAR questions
│   │   ├── technical.py        # Domain-specific questions
│   │   └── question_banks.py   # Fallback questions
│   ├── evaluator/
│   │   ├── __init__.py
│   │   ├── behavioral.py       # STAR evaluation
│   │   └── technical.py        # Technical evaluation
│   ├── scoring/
│   │   ├── __init__.py
│   │   ├── scorer.py           # Overall scoring
│   │   └── feedback.py         # Feedback generation
│   └── utils/
│       ├── __init__.py
│       ├── llm_client.py       # LLM wrapper
│       └── validators.py       # Data validation
├── prompts/
│   ├── resume_parsing.txt
│   ├── behavioral_questions.txt
│   ├── technical_questions.txt
│   ├── behavioral_eval.txt
│   └── technical_eval.txt
├── tests/
│   ├── test_resume_parser.py
│   ├── test_question_generator.py
│   ├── test_evaluator.py
│   └── test_scorer.py
├── examples/
│   ├── sample_resumes/
│   └── usage_examples.py
├── .env.example
├── .gitignore
├── requirements.txt
├── setup.py
└── README.md
```

#### 1.2 Dependencies Installation
```python
# requirements.txt
# Core LLM
openai>=1.0.0
anthropic>=0.18.0  # Optional alternative

# Resume Parsing
pypdf2>=3.0.0
python-docx>=0.8.11
pdfplumber>=0.10.0  # Alternative to PyPDF2

# NLP & Context Management
spacy>=3.7.0
langchain>=0.1.0
langchain-openai>=0.0.5

# Data Processing & Validation
pandas>=2.0.0
numpy>=1.24.0
pydantic>=2.0.0
pydantic-settings>=2.0.0

# Utilities
python-dotenv>=1.0.0
requests>=2.31.0
tenacity>=8.2.0  # Retry logic for API calls

# Optional (Enhanced Features)
pytesseract>=0.3.10  # OCR for scanned PDFs
chromadb>=0.4.0  # Vector database
tiktoken>=0.5.0  # Token counting

# Development
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.0.0
flake8>=6.1.0
mypy>=1.5.0
```

#### 1.3 Environment Configuration
```python
# .env.example
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here  # Optional

# Model Configuration
DEFAULT_MODEL=gpt-4
FAST_MODEL=gpt-4-mini
TEMPERATURE=0.0  # Deterministic for consistency

# API Configuration
MAX_RETRIES=3
TIMEOUT=30

# Feature Flags
ENABLE_OCR=false
ENABLE_VECTOR_DB=false
```

#### 1.4 Initial Setup Tasks
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Test LLM connectivity
python -c "from openai import OpenAI; client = OpenAI(); print('Connected!')"
```

#### 1.5 LLM Client Wrapper
```python
# src/utils/llm_client.py
from openai import OpenAI
from anthropic import Anthropic
from tenacity import retry, stop_after_attempt, wait_exponential
import json
from typing import Optional, Dict, Any
import os

class LLMClient:
    """Unified LLM client supporting OpenAI and Anthropic"""

    def __init__(
        self,
        provider: str = "openai",
        model: Optional[str] = None,
        temperature: float = 0.0
    ):
        self.provider = provider
        self.temperature = temperature

        if provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = model or os.getenv("DEFAULT_MODEL", "gpt-4")
        elif provider == "anthropic":
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = model or "claude-3-5-sonnet-20241022"
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        json_mode: bool = False
    ) -> str:
        """Generate response from LLM"""

        if self.provider == "openai":
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature
            }

            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}

            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content

        elif self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=self.temperature,
                system=system_prompt or "",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text

    def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> Dict[Any, Any]:
        """Generate and parse JSON response"""
        response = self.generate(prompt, system_prompt, json_mode=True)
        return json.loads(response)
```

**Success Criteria:**
- ✅ Project structure created
- ✅ All dependencies installed
- ✅ LLM API connection working
- ✅ spaCy model downloaded
- ✅ Can make successful test API call

---

### **PHASE 2: Resume Parser** ⏱️ 4-6 hours
**Priority:** CRITICAL (MVP)

#### 2.1 Data Schemas (Pydantic Models)
```python
# src/resume_parser/schemas.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import date

class Contact(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    location: Optional[str] = None

class Education(BaseModel):
    institution: str
    degree: str
    field: Optional[str] = None
    graduation_date: Optional[str] = None
    gpa: Optional[str] = None
    honors: Optional[List[str]] = []

class Experience(BaseModel):
    company: str
    title: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = None
    responsibilities: List[str] = []
    achievements: List[str] = []
    technologies: List[str] = []

class Project(BaseModel):
    name: str
    description: str
    technologies: List[str] = []
    url: Optional[str] = None
    highlights: List[str] = []

class Skills(BaseModel):
    technical: List[str] = []
    soft: List[str] = []
    tools: List[str] = []
    languages: List[str] = []  # Programming languages
    frameworks: List[str] = []

class ParsedResume(BaseModel):
    contact: Contact
    education: List[Education] = []
    experience: List[Experience] = []
    skills: Skills = Skills()
    projects: List[Project] = []
    certifications: List[str] = []
    leadership: List[str] = []
    awards: List[str] = []

    # Metadata
    experience_level: Optional[str] = None  # "junior", "mid", "senior"
    total_years_experience: Optional[float] = None

    @validator('experience_level', always=True)
    def determine_experience_level(cls, v, values):
        """Auto-determine experience level from years of experience"""
        if 'total_years_experience' in values and values['total_years_experience']:
            years = values['total_years_experience']
            if years < 2:
                return "junior"
            elif years < 5:
                return "mid"
            else:
                return "senior"
        return v or "unknown"
```

#### 2.2 Text Extraction
```python
# src/resume_parser/extractors.py
import PyPDF2
from docx import Document
from pathlib import Path
from typing import Optional
import re

class TextExtractor:
    """Extract text from various document formats"""

    @staticmethod
    def extract_from_pdf(file_path: str) -> str:
        """Extract text from PDF using PyPDF2"""
        text = []

        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)

                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
        except Exception as e:
            raise ValueError(f"Error extracting PDF: {str(e)}")

        return "\n".join(text)

    @staticmethod
    def extract_from_docx(file_path: str) -> str:
        """Extract text from DOCX using python-docx"""
        try:
            doc = Document(file_path)
            text = [paragraph.text for paragraph in doc.paragraphs]
            return "\n".join(text)
        except Exception as e:
            raise ValueError(f"Error extracting DOCX: {str(e)}")

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.,;:\-\(\)@/]', '', text)
        # Remove multiple newlines
        text = re.sub(r'\n+', '\n', text)
        return text.strip()

    @staticmethod
    def extract_text(file_path: str) -> str:
        """Universal text extractor - auto-detects format"""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        suffix = path.suffix.lower()

        if suffix == '.pdf':
            raw_text = TextExtractor.extract_from_pdf(file_path)
        elif suffix in ['.docx', '.doc']:
            raw_text = TextExtractor.extract_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")

        return TextExtractor.clean_text(raw_text)
```

#### 2.3 LLM-Based Resume Parsing
```python
# src/resume_parser/parser.py
from src.utils.llm_client import LLMClient
from src.resume_parser.extractors import TextExtractor
from src.resume_parser.schemas import ParsedResume
from typing import Dict, Any
import json

class ResumeParser:
    """Parse resumes using LLM-based extraction"""

    PARSING_PROMPT = """You are an expert resume parser. Extract structured information from this resume text.

Resume Text:
{resume_text}

Return a JSON object with this EXACT schema:
{{
  "contact": {{
    "name": "",
    "email": "",
    "phone": "",
    "linkedin": "",
    "github": "",
    "location": ""
  }},
  "education": [
    {{
      "institution": "",
      "degree": "",
      "field": "",
      "graduation_date": "",
      "gpa": "",
      "honors": []
    }}
  ],
  "experience": [
    {{
      "company": "",
      "title": "",
      "start_date": "",
      "end_date": "",
      "location": "",
      "responsibilities": [],
      "achievements": [],
      "technologies": []
    }}
  ],
  "skills": {{
    "technical": [],
    "soft": [],
    "tools": [],
    "languages": [],
    "frameworks": []
  }},
  "projects": [
    {{
      "name": "",
      "description": "",
      "technologies": [],
      "url": "",
      "highlights": []
    }}
  ],
  "certifications": [],
  "leadership": [],
  "awards": [],
  "total_years_experience": 0.0
}}

Instructions:
1. Extract ALL available information accurately
2. For missing fields, use null or empty arrays
3. For responsibilities/achievements, create separate bullet points
4. Extract action verbs and quantifiable results
5. Identify all technical skills, tools, and technologies mentioned
6. Calculate total_years_experience by summing work experience duration
7. Be precise with dates, names, and technical terms
8. Separate responsibilities (what they did) from achievements (impact/results)

Return ONLY valid JSON, no additional text.
"""

    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient(provider="openai", model="gpt-4")
        self.extractor = TextExtractor()

    def parse_resume(self, file_path: str) -> ParsedResume:
        """Parse resume from file path"""
        # Extract text
        resume_text = self.extractor.extract_text(file_path)

        # Generate prompt
        prompt = self.PARSING_PROMPT.format(resume_text=resume_text)

        # Call LLM
        response = self.llm_client.generate_json(prompt)

        # Validate and return
        try:
            parsed_resume = ParsedResume(**response)
            return parsed_resume
        except Exception as e:
            raise ValueError(f"Failed to validate parsed resume: {str(e)}\nResponse: {response}")

    def parse_resume_from_text(self, resume_text: str) -> ParsedResume:
        """Parse resume from already-extracted text"""
        cleaned_text = self.extractor.clean_text(resume_text)
        prompt = self.PARSING_PROMPT.format(resume_text=cleaned_text)
        response = self.llm_client.generate_json(prompt)
        return ParsedResume(**response)
```

#### 2.4 Testing Resume Parser
```python
# tests/test_resume_parser.py
import pytest
from src.resume_parser.parser import ResumeParser
from src.resume_parser.schemas import ParsedResume

def test_parse_pdf_resume():
    """Test parsing PDF resume"""
    parser = ResumeParser()
    result = parser.parse_resume("examples/sample_resumes/sample1.pdf")

    assert isinstance(result, ParsedResume)
    assert result.contact.name is not None
    assert len(result.experience) > 0

def test_parse_docx_resume():
    """Test parsing DOCX resume"""
    parser = ResumeParser()
    result = parser.parse_resume("examples/sample_resumes/sample2.docx")

    assert isinstance(result, ParsedResume)
    assert result.contact.email is not None

def test_minimal_resume():
    """Test with minimal resume (new grad)"""
    parser = ResumeParser()
    result = parser.parse_resume("examples/sample_resumes/new_grad.pdf")

    assert result.experience_level == "junior"
    assert len(result.education) > 0

def test_extensive_resume():
    """Test with extensive resume (10+ years)"""
    parser = ResumeParser()
    result = parser.parse_resume("examples/sample_resumes/senior.pdf")

    assert result.experience_level == "senior"
    assert result.total_years_experience >= 10
```

**Challenges & Mitigations:**
- ⚠️ **Scanned PDFs:** Skip OCR for MVP, require digital PDFs
- ⚠️ **Multi-column layouts:** LLM handles better than regex
- ⚠️ **Tables:** Text extraction may lose structure - rely on LLM to reconstruct
- ⚠️ **Inconsistent formats:** LLM is more robust than rule-based systems

**Success Criteria:**
- ✅ Parse PDF and DOCX successfully
- ✅ Extract all major sections (contact, education, experience, skills)
- ✅ Handle edge cases (minimal resume, extensive resume)
- ✅ Validate output with Pydantic schemas

---

### **PHASE 3: Behavioral Question Generation** ⏱️ 3-4 hours
**Priority:** CRITICAL (MVP)

#### 3.1 Question Generation Logic
```python
# src/question_generator/behavioral.py
from src.utils.llm_client import LLMClient
from src.resume_parser.schemas import ParsedResume
from typing import List, Dict, Any
from pydantic import BaseModel

class BehavioralQuestion(BaseModel):
    question: str
    competency: str  # Leadership, Teamwork, Problem-Solving, etc.
    difficulty: str  # Easy, Medium, Hard
    resume_reference: str  # What from resume triggered this
    star_focus: List[str]  # Which STAR components to emphasize

class BehavioralQuestionGenerator:
    """Generate STAR-based behavioral questions"""

    GENERATION_PROMPT = """You are an expert behavioral interviewer using the STAR framework.

Candidate Resume Summary:
{resume_summary}

Generate exactly {num_questions} behavioral interview questions that:
1. Are SPECIFIC to this candidate's actual experiences
2. Use STAR framework (expect Situation, Task, Action, Result)
3. Cover different competencies:
   - Leadership
   - Teamwork and Collaboration
   - Problem-Solving
   - Communication
   - Adaptability and Learning
   - Conflict Resolution
   - Time Management and Prioritization
4. Reference actual projects/roles/companies from their resume
5. Vary in difficulty (mix of standard and challenging)
6. Are open-ended and encourage detailed stories

Format as JSON array:
[
  {{
    "question": "Tell me about a time when you had to [specific scenario from their experience]...",
    "competency": "Leadership",
    "difficulty": "Medium",
    "resume_reference": "Lead Developer role at XYZ Corp, 2022-2024",
    "star_focus": ["Action", "Result"]
  }}
]

IMPORTANT:
- DO NOT ask generic questions like "Tell me about yourself"
- ALWAYS reference specific experiences, projects, or technologies from their resume
- Questions should make the candidate think about specific past situations
- Ensure each question can be answered using the STAR framework

Return ONLY valid JSON array, no additional text.
"""

    COMPETENCIES = [
        "Leadership",
        "Teamwork and Collaboration",
        "Problem-Solving",
        "Communication",
        "Adaptability and Learning",
        "Conflict Resolution",
        "Time Management and Prioritization",
        "Initiative and Ownership",
        "Handling Failure and Feedback"
    ]

    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient(provider="openai", model="gpt-4")

    def _create_resume_summary(self, parsed_resume: ParsedResume) -> str:
        """Create concise resume summary for context"""
        summary_parts = []

        # Experience
        if parsed_resume.experience:
            exp_summary = "Work Experience:\n"
            for exp in parsed_resume.experience[:3]:  # Top 3
                exp_summary += f"- {exp.title} at {exp.company}"
                if exp.start_date:
                    exp_summary += f" ({exp.start_date} - {exp.end_date or 'Present'})"
                exp_summary += "\n"
                if exp.achievements:
                    exp_summary += f"  Key achievements: {', '.join(exp.achievements[:2])}\n"
            summary_parts.append(exp_summary)

        # Projects
        if parsed_resume.projects:
            proj_summary = "Key Projects:\n"
            for proj in parsed_resume.projects[:3]:
                proj_summary += f"- {proj.name}: {proj.description}\n"
                if proj.technologies:
                    proj_summary += f"  Technologies: {', '.join(proj.technologies)}\n"
            summary_parts.append(proj_summary)

        # Skills
        if parsed_resume.skills.technical:
            skills_summary = f"Technical Skills: {', '.join(parsed_resume.skills.technical[:10])}\n"
            summary_parts.append(skills_summary)

        # Leadership
        if parsed_resume.leadership:
            lead_summary = f"Leadership: {', '.join(parsed_resume.leadership)}\n"
            summary_parts.append(lead_summary)

        # Experience level
        summary_parts.append(f"Experience Level: {parsed_resume.experience_level}")

        return "\n".join(summary_parts)

    def generate_questions(
        self,
        parsed_resume: ParsedResume,
        num_questions: int = 5
    ) -> List[BehavioralQuestion]:
        """Generate behavioral questions based on resume"""

        resume_summary = self._create_resume_summary(parsed_resume)

        prompt = self.GENERATION_PROMPT.format(
            resume_summary=resume_summary,
            num_questions=num_questions
        )

        response = self.llm_client.generate_json(prompt)

        # Parse and validate
        questions = []
        for q_data in response:
            try:
                question = BehavioralQuestion(**q_data)
                questions.append(question)
            except Exception as e:
                print(f"Warning: Failed to validate question: {e}")
                continue

        # Quality check: ensure not generic
        questions = self._filter_generic_questions(questions)

        return questions

    def _filter_generic_questions(
        self,
        questions: List[BehavioralQuestion]
    ) -> List[BehavioralQuestion]:
        """Remove generic questions that don't reference resume"""

        generic_patterns = [
            "tell me about yourself",
            "what are your strengths",
            "what are your weaknesses",
            "where do you see yourself"
        ]

        filtered = []
        for q in questions:
            question_lower = q.question.lower()
            is_generic = any(pattern in question_lower for pattern in generic_patterns)
            has_reference = q.resume_reference and q.resume_reference != ""

            if not is_generic and has_reference:
                filtered.append(q)

        return filtered
```

#### 3.2 Fallback Question Bank
```python
# src/question_generator/question_banks.py

FALLBACK_BEHAVIORAL_QUESTIONS = {
    "Leadership": [
        {
            "question": "Tell me about a time when you had to lead a project with tight deadlines. How did you prioritize and delegate tasks?",
            "difficulty": "Medium",
            "competency": "Leadership"
        },
        {
            "question": "Describe a situation where you had to motivate a team member who was struggling. What was your approach?",
            "difficulty": "Medium",
            "competency": "Leadership"
        }
    ],
    "Problem-Solving": [
        {
            "question": "Tell me about a complex technical problem you solved. Walk me through your debugging process.",
            "difficulty": "Medium",
            "competency": "Problem-Solving"
        },
        {
            "question": "Describe a time when you had to make a decision with incomplete information. How did you approach it?",
            "difficulty": "Hard",
            "competency": "Problem-Solving"
        }
    ],
    "Teamwork": [
        {
            "question": "Tell me about a time when you had to work with a difficult team member. How did you handle it?",
            "difficulty": "Medium",
            "competency": "Teamwork and Collaboration"
        },
        {
            "question": "Describe a project where you had to collaborate across multiple teams. What challenges did you face?",
            "difficulty": "Medium",
            "competency": "Teamwork and Collaboration"
        }
    ],
    "Adaptability": [
        {
            "question": "Tell me about a time when project requirements changed significantly mid-way. How did you adapt?",
            "difficulty": "Medium",
            "competency": "Adaptability and Learning"
        }
    ],
    "Communication": [
        {
            "question": "Describe a time when you had to explain a complex technical concept to a non-technical stakeholder.",
            "difficulty": "Medium",
            "competency": "Communication"
        }
    ]
}
```

**Success Criteria:**
- ✅ Generate 5 relevant questions
- ✅ All questions reference specific resume content
- ✅ Cover diverse competencies
- ✅ No generic questions
- ✅ Vary in difficulty

---

### **PHASE 4: Technical Question Generation** ⏱️ 4-5 hours
**Priority:** CRITICAL (MVP)

#### 4.1 Domain-Specific Question Generator
```python
# src/question_generator/technical.py
from src.utils.llm_client import LLMClient
from src.resume_parser.schemas import ParsedResume
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class TechnicalQuestion(BaseModel):
    question: str
    type: str  # "conceptual", "coding", "system_design"
    domain: str  # "algorithms", "web_development", etc.
    difficulty: str  # "easy", "medium", "hard"
    skills_tested: List[str]
    expected_answer_outline: str
    follow_ups: List[str] = []

class TechnicalQuestionGenerator:
    """Generate domain-specific technical questions"""

    GENERATION_PROMPT = """Generate {num_questions} technical interview questions for: {domain}

Candidate Profile:
- Technical Skills: {technical_skills}
- Experience Level: {experience_level}
- Relevant Projects: {relevant_projects}
- Tools/Frameworks: {tools_frameworks}

Question Requirements:
1. Match candidate's stated skills (ask about technologies they claim to know)
2. Appropriate difficulty for {experience_level} level:
   - Junior: Fundamentals, basic concepts, simple implementations
   - Mid: Deeper understanding, trade-offs, moderate complexity
   - Senior: System design, architecture, optimization, trade-offs
3. Mix of question types:
   - Conceptual understanding ({conceptual_count} questions)
   - Coding/implementation ({coding_count} questions)
   - System design ({design_count} questions, if senior)

Domain-Specific Guidelines:

ALGORITHMS:
- Data structures (arrays, linked lists, trees, graphs, hash tables)
- Sorting and searching algorithms
- Recursion and dynamic programming
- Big O complexity analysis
- Problem-solving patterns (two pointers, sliding window, etc.)

WEB DEVELOPMENT:
- Frontend: HTML/CSS/JavaScript, React/Vue, state management, DOM manipulation
- Backend: RESTful APIs, databases (SQL/NoSQL), authentication, server architecture
- Full-stack: Architecture, API design, data flow
- Performance: Optimization, caching, lazy loading
- Security: XSS, CSRF, SQL injection, authentication best practices

MACHINE LEARNING:
- Supervised vs unsupervised learning
- Model selection and evaluation metrics
- Feature engineering and selection
- Overfitting/underfitting and regularization
- Specific algorithms: regression, classification, clustering, neural networks
- ML pipeline: data preprocessing, training, validation, deployment

SYSTEM DESIGN:
- Scalability and load balancing
- Database design and sharding
- Caching strategies (Redis, Memcached)
- Microservices vs monolithic architecture
- Message queues and asynchronous processing
- CAP theorem and consistency models

For EACH question, return JSON:
{{
  "question": "Clear, specific question...",
  "type": "conceptual|coding|system_design",
  "domain": "{domain}",
  "difficulty": "easy|medium|hard",
  "skills_tested": ["skill1", "skill2"],
  "expected_answer_outline": "Key points a good answer should cover...",
  "follow_ups": ["Follow-up question 1", "Follow-up question 2"]
}}

IMPORTANT:
- Reference technologies from candidate's resume when possible
- For coding questions, clearly state the problem and constraints
- For system design, specify scale and requirements
- Ensure questions test understanding, not just memorization

Return JSON array of {num_questions} questions. Only valid JSON, no additional text.
"""

    DOMAINS = [
        "algorithms",
        "web_development",
        "machine_learning",
        "system_design"
    ]

    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient(provider="openai", model="gpt-4")

    def generate_questions(
        self,
        domain: str,
        parsed_resume: ParsedResume,
        num_questions: int = 5
    ) -> List[TechnicalQuestion]:
        """Generate technical questions for specific domain"""

        if domain not in self.DOMAINS:
            raise ValueError(f"Unsupported domain: {domain}. Choose from {self.DOMAINS}")

        # Determine question mix based on experience level
        question_mix = self._get_question_mix(parsed_resume.experience_level, num_questions)

        # Extract relevant skills
        technical_skills = ", ".join(parsed_resume.skills.technical[:15])
        tools_frameworks = ", ".join(
            parsed_resume.skills.tools + parsed_resume.skills.frameworks
        )[:200]

        relevant_projects = self._get_relevant_projects(parsed_resume, domain)

        prompt = self.GENERATION_PROMPT.format(
            num_questions=num_questions,
            domain=domain,
            technical_skills=technical_skills or "General programming",
            experience_level=parsed_resume.experience_level,
            relevant_projects=relevant_projects,
            tools_frameworks=tools_frameworks or "N/A",
            conceptual_count=question_mix["conceptual"],
            coding_count=question_mix["coding"],
            design_count=question_mix["design"]
        )

        response = self.llm_client.generate_json(prompt)

        # Parse and validate
        questions = []
        for q_data in response:
            try:
                question = TechnicalQuestion(**q_data)
                questions.append(question)
            except Exception as e:
                print(f"Warning: Failed to validate question: {e}")
                continue

        return questions

    def _get_question_mix(self, experience_level: str, total: int) -> Dict[str, int]:
        """Determine mix of question types based on experience level"""

        if experience_level == "junior":
            return {
                "conceptual": int(total * 0.6),  # 60% conceptual
                "coding": int(total * 0.4),      # 40% coding
                "design": 0                       # No system design
            }
        elif experience_level == "mid":
            return {
                "conceptual": int(total * 0.4),
                "coding": int(total * 0.4),
                "design": int(total * 0.2)
            }
        else:  # senior
            return {
                "conceptual": int(total * 0.3),
                "coding": int(total * 0.3),
                "design": int(total * 0.4)
            }

    def _get_relevant_projects(self, parsed_resume: ParsedResume, domain: str) -> str:
        """Extract projects relevant to domain"""

        domain_keywords = {
            "algorithms": ["algorithm", "data structure", "leetcode", "coding"],
            "web_development": ["web", "frontend", "backend", "api", "react", "node"],
            "machine_learning": ["ml", "machine learning", "ai", "model", "neural"],
            "system_design": ["architecture", "scalable", "distributed", "microservice"]
        }

        keywords = domain_keywords.get(domain, [])
        relevant = []

        for project in parsed_resume.projects:
            description_lower = project.description.lower()
            if any(keyword in description_lower for keyword in keywords):
                relevant.append(f"- {project.name}: {project.description}")

        return "\n".join(relevant[:3]) if relevant else "No specific projects mentioned"
```

#### 4.2 Fallback Technical Question Banks
```python
# src/question_generator/question_banks.py (continued)

TECHNICAL_QUESTION_BANKS = {
    "algorithms": {
        "easy": [
            {
                "question": "Explain the difference between an array and a linked list. When would you use each?",
                "type": "conceptual",
                "difficulty": "easy",
                "skills_tested": ["Data Structures"],
                "expected_answer_outline": "Arrays: contiguous memory, O(1) access, fixed size. Linked Lists: dynamic size, O(n) access, easy insertion/deletion."
            },
            {
                "question": "What is Big O notation? Explain with examples of O(1), O(n), and O(log n).",
                "type": "conceptual",
                "difficulty": "easy",
                "skills_tested": ["Complexity Analysis"],
                "expected_answer_outline": "Big O describes worst-case time complexity. Examples: array access (O(1)), linear search (O(n)), binary search (O(log n))."
            },
            {
                "question": "Write a function to reverse a string in Python.",
                "type": "coding",
                "difficulty": "easy",
                "skills_tested": ["String Manipulation", "Python"],
                "expected_answer_outline": "def reverse_string(s): return s[::-1] or use two pointers"
            }
        ],
        "medium": [
            {
                "question": "Implement a function to detect if a linked list has a cycle. What is the time and space complexity?",
                "type": "coding",
                "difficulty": "medium",
                "skills_tested": ["Linked Lists", "Floyd's Algorithm"],
                "expected_answer_outline": "Use Floyd's cycle detection (fast/slow pointers). Time: O(n), Space: O(1)"
            },
            {
                "question": "Explain the difference between BFS and DFS. When would you use each for graph traversal?",
                "type": "conceptual",
                "difficulty": "medium",
                "skills_tested": ["Graphs", "Traversal Algorithms"],
                "expected_answer_outline": "BFS: level-order, shortest path. DFS: explores deep, topological sort. BFS uses queue, DFS uses stack/recursion."
            }
        ],
        "hard": [
            {
                "question": "Design and implement an LRU (Least Recently Used) cache with O(1) get and put operations.",
                "type": "coding",
                "difficulty": "hard",
                "skills_tested": ["Hash Maps", "Doubly Linked List", "Data Structure Design"],
                "expected_answer_outline": "Use HashMap + Doubly Linked List. HashMap for O(1) lookup, DLL for O(1) insertion/deletion."
            }
        ]
    },

    "web_development": {
        "easy": [
            {
                "question": "Explain the difference between GET and POST HTTP methods. When would you use each?",
                "type": "conceptual",
                "difficulty": "easy",
                "skills_tested": ["HTTP", "REST APIs"],
                "expected_answer_outline": "GET: retrieve data, idempotent, cacheable. POST: submit data, not idempotent, creates resources."
            },
            {
                "question": "What is the difference between var, let, and const in JavaScript?",
                "type": "conceptual",
                "difficulty": "easy",
                "skills_tested": ["JavaScript", "Variable Scope"],
                "expected_answer_outline": "var: function-scoped, hoisted. let: block-scoped, not hoisted. const: block-scoped, immutable reference."
            }
        ],
        "medium": [
            {
                "question": "Explain how React's virtual DOM works and why it improves performance.",
                "type": "conceptual",
                "difficulty": "medium",
                "skills_tested": ["React", "Virtual DOM", "Performance"],
                "expected_answer_outline": "Virtual DOM is in-memory representation. React diffs old/new VDOM, calculates minimal DOM updates, batches changes."
            },
            {
                "question": "Design a RESTful API for a blog system with posts and comments. Define the endpoints and HTTP methods.",
                "type": "system_design",
                "difficulty": "medium",
                "skills_tested": ["API Design", "REST", "Resource Modeling"],
                "expected_answer_outline": "GET /posts, POST /posts, GET /posts/:id, PUT /posts/:id, DELETE /posts/:id, GET /posts/:id/comments, POST /posts/:id/comments"
            }
        ],
        "hard": [
            {
                "question": "Design a system to handle 1 million concurrent WebSocket connections. How would you scale it?",
                "type": "system_design",
                "difficulty": "hard",
                "skills_tested": ["WebSockets", "Scalability", "Load Balancing"],
                "expected_answer_outline": "Use load balancer, connection servers, message broker (Redis/RabbitMQ), horizontal scaling, sticky sessions."
            }
        ]
    },

    "machine_learning": {
        "easy": [
            {
                "question": "Explain the difference between supervised and unsupervised learning with examples.",
                "type": "conceptual",
                "difficulty": "easy",
                "skills_tested": ["ML Fundamentals"],
                "expected_answer_outline": "Supervised: labeled data, prediction (classification/regression). Unsupervised: unlabeled, pattern discovery (clustering/dimensionality reduction)."
            },
            {
                "question": "What is overfitting and how can you prevent it?",
                "type": "conceptual",
                "difficulty": "easy",
                "skills_tested": ["Model Training", "Regularization"],
                "expected_answer_outline": "Overfitting: model memorizes training data, poor generalization. Prevention: regularization, cross-validation, more data, simpler model."
            }
        ],
        "medium": [
            {
                "question": "Explain the bias-variance tradeoff in machine learning.",
                "type": "conceptual",
                "difficulty": "medium",
                "skills_tested": ["ML Theory", "Model Selection"],
                "expected_answer_outline": "Bias: underfitting, model too simple. Variance: overfitting, model too complex. Goal: balance both for optimal generalization."
            },
            {
                "question": "You're building a spam classifier. Walk me through your approach from data collection to deployment.",
                "type": "system_design",
                "difficulty": "medium",
                "skills_tested": ["ML Pipeline", "Classification"],
                "expected_answer_outline": "Data collection, preprocessing, feature extraction (TF-IDF), model selection (Naive Bayes/SVM), training, validation, deployment, monitoring."
            }
        ],
        "hard": [
            {
                "question": "Explain backpropagation in neural networks. How does gradient descent update weights?",
                "type": "conceptual",
                "difficulty": "hard",
                "skills_tested": ["Neural Networks", "Optimization"],
                "expected_answer_outline": "Backpropagation: compute gradients using chain rule, propagate errors backward. Gradient descent: update weights in direction of negative gradient to minimize loss."
            }
        ]
    },

    "system_design": {
        "medium": [
            {
                "question": "Design a URL shortening service like bit.ly. Consider scalability and collision handling.",
                "type": "system_design",
                "difficulty": "medium",
                "skills_tested": ["Distributed Systems", "Hashing", "Databases"],
                "expected_answer_outline": "Hash function (MD5/Base62), collision handling, database (NoSQL for scalability), caching (Redis), load balancer, analytics."
            }
        ],
        "hard": [
            {
                "question": "Design a distributed cache system like Redis. How do you handle consistency, replication, and failover?",
                "type": "system_design",
                "difficulty": "hard",
                "skills_tested": ["Distributed Systems", "CAP Theorem", "Replication"],
                "expected_answer_outline": "Master-slave replication, eventual consistency, sharding, consistent hashing, failover with sentinel, persistence strategies."
            },
            {
                "question": "Design Netflix's video streaming architecture. How do you handle CDN, encoding, and recommendation systems?",
                "type": "system_design",
                "difficulty": "hard",
                "skills_tested": ["Scalability", "CDN", "Microservices"],
                "expected_answer_outline": "CDN for content delivery, adaptive bitrate streaming, encoding pipeline, microservices architecture, recommendation engine, analytics."
            }
        ]
    }
}
```

**Success Criteria:**
- ✅ Generate relevant questions for all 4 domains
- ✅ Questions match candidate's skill level
- ✅ Appropriate mix of conceptual/coding/design questions
- ✅ Questions reference technologies from resume

---

### **PHASE 5: Behavioral Response Evaluation** ⏱️ 5-6 hours
**Priority:** CRITICAL (MVP)

#### 5.1 STAR Framework Evaluator
```python
# src/evaluator/behavioral.py
from src.utils.llm_client import LLMClient
from src.question_generator.behavioral import BehavioralQuestion
from typing import Dict, Any, Optional, List
from pydantic import BaseModel

class STARComponent(BaseModel):
    present: bool
    score: int  # 0-10
    quote: Optional[str] = None
    feedback: Optional[str] = None

class BehavioralEvaluation(BaseModel):
    # STAR Analysis
    star_scores: Dict[str, STARComponent]

    # Quality Metrics
    specificity: int  # 0-10
    clarity: int  # 0-10
    impact: int  # 0-10
    ownership: int  # 0-10 (use of "I" vs "we")

    # Overall
    overall_score: int  # 0-100
    performance_level: str  # "Excellent", "Good", "Satisfactory", "Needs Improvement"

    # Feedback
    strengths: List[str]
    weaknesses: List[str]
    missing_components: List[str]
    priority_improvement: str
    example_better_answer: Optional[str] = None

class BehavioralEvaluator:
    """Evaluate behavioral interview responses using STAR framework"""

    EVALUATION_PROMPT = """You are an expert interview evaluator using the STAR framework.

QUESTION: {question}

CANDIDATE'S ANSWER: {transcript}

Evaluate this response systematically:

## 1. STAR COMPONENT ANALYSIS (Score each 0-10):

**Situation (0-10):**
- Did they provide clear context and background?
- Quote the relevant part if present
- What's missing or could be improved?

**Task (0-10):**
- Did they explain the objective/challenge/goal?
- Quote the relevant part if present
- Was the task/challenge clear?

**Action (0-10):**
- Did they describe THEIR specific actions (not "we", but "I")?
- Quote the relevant part if present
- Were actions concrete and detailed?

**Result (0-10):**
- Did they share measurable outcomes?
- Quote the relevant part if present
- Were there metrics/numbers/impact stated?

## 2. QUALITY METRICS (Score each 0-10):

**Specificity:** Concrete details vs vague statements
**Clarity:** Easy to follow and understand
**Impact:** Evidence of meaningful contribution
**Ownership:** Used "I" not "we" consistently

## 3. RESPONSE CHARACTERISTICS:

- Length: Too short (<1 min) / Appropriate / Too long (>4 min)
- Filler words: Excessive "um", "like", "you know"
- Structure: Clear narrative vs rambling

## 4. PROVIDE:

- Overall score (0-100): Weighted average (STAR 60%, Quality 40%)
- Performance level: "Excellent" (90-100), "Good" (75-89), "Satisfactory" (60-74), "Needs Improvement" (<60)
- 3 specific strengths
- 3 specific weaknesses
- Missing STAR components
- Priority improvement (most critical thing to fix)
- Example of how to strengthen the weakest part

Return ONLY valid JSON with this schema:
{{
  "star_scores": {{
    "situation": {{
      "present": true/false,
      "score": 0-10,
      "quote": "...",
      "feedback": "What was good/missing"
    }},
    "task": {{ ... }},
    "action": {{ ... }},
    "result": {{ ... }}
  }},
  "specificity": 0-10,
  "clarity": 0-10,
  "impact": 0-10,
  "ownership": 0-10,
  "overall_score": 0-100,
  "performance_level": "...",
  "strengths": ["...", "...", "..."],
  "weaknesses": ["...", "...", "..."],
  "missing_components": ["Situation", "Task", etc.],
  "priority_improvement": "Most critical improvement...",
  "example_better_answer": "Here's how to improve the [weakest component]: ..."
}}
"""

    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient(provider="openai", model="gpt-4")

    def evaluate(
        self,
        question: str,
        transcript: str
    ) -> BehavioralEvaluation:
        """Evaluate a behavioral interview response"""

        # Basic validation
        if len(transcript.strip()) < 50:
            return self._create_insufficient_response_evaluation()

        prompt = self.EVALUATION_PROMPT.format(
            question=question,
            transcript=transcript
        )

        response = self.llm_client.generate_json(prompt)

        try:
            evaluation = BehavioralEvaluation(**response)
            return evaluation
        except Exception as e:
            raise ValueError(f"Failed to parse evaluation: {e}\nResponse: {response}")

    def _create_insufficient_response_evaluation(self) -> BehavioralEvaluation:
        """Return evaluation for very short/insufficient responses"""
        return BehavioralEvaluation(
            star_scores={
                "situation": STARComponent(present=False, score=0, feedback="No context provided"),
                "task": STARComponent(present=False, score=0, feedback="No task/goal explained"),
                "action": STARComponent(present=False, score=0, feedback="No actions described"),
                "result": STARComponent(present=False, score=0, feedback="No results shared")
            },
            specificity=0,
            clarity=0,
            impact=0,
            ownership=0,
            overall_score=10,
            performance_level="Needs Improvement",
            strengths=[],
            weaknesses=[
                "Response too short",
                "Missing all STAR components",
                "No detail or context provided"
            ],
            missing_components=["Situation", "Task", "Action", "Result"],
            priority_improvement="Provide a complete answer following the STAR framework with at least 1-2 minutes of content."
        )

    def calculate_star_completeness(self, evaluation: BehavioralEvaluation) -> float:
        """Calculate what % of STAR components are present"""
        components = evaluation.star_scores
        present_count = sum(1 for comp in components.values() if comp.present)
        return (present_count / 4) * 100
```

**Success Criteria:**
- ✅ Correctly identify all STAR components
- ✅ Detect missing components
- ✅ Provide specific, actionable feedback
- ✅ Quote examples from response
- ✅ Consistent scoring

---

### **PHASE 6: Technical Response Evaluation** ⏱️ 5-6 hours
**Priority:** CRITICAL (MVP)

#### 6.1 Technical Evaluator
```python
# src/evaluator/technical.py
from src.utils.llm_client import LLMClient
from src.question_generator.technical import TechnicalQuestion
from typing import Dict, Any, Optional, List
from pydantic import BaseModel

class TechnicalEvaluation(BaseModel):
    # Core Scores
    correctness: int  # 0-10
    completeness: int  # 0-10
    depth: int  # 0-10
    communication: int  # 0-10
    problem_solving: Optional[int] = None  # 0-10, for coding questions

    # Overall
    overall_score: int  # 0-100
    weighted_score: float  # Weighted based on question type
    performance_level: str

    # Detailed Feedback
    what_they_got_right: List[str]
    what_they_got_wrong: List[str]
    what_they_missed: List[str]
    conceptual_gaps: List[str]
    improvement_suggestions: List[str]
    follow_up_questions: List[str] = []

class TechnicalEvaluator:
    """Evaluate technical interview responses"""

    EVALUATION_PROMPT = """You are a technical interviewer evaluating a candidate's response.

QUESTION: {question}
DOMAIN: {domain}
QUESTION TYPE: {question_type}
EXPECTED ANSWER OUTLINE: {expected_answer}
SKILLS BEING TESTED: {skills_tested}

CANDIDATE'S ANSWER: {transcript}

Evaluate the technical response systematically:

## 1. CORRECTNESS (0-10):
- Are the core concepts correct?
- Any technical errors or misconceptions?
- Quote specific errors if any
- What did they get right?

## 2. COMPLETENESS (0-10):
- Did they address all parts of the question?
- What aspects did they cover?
- What did they miss?

## 3. DEPTH OF UNDERSTANDING (0-10):
- Surface-level or fundamental understanding?
- Can they explain WHY, not just WHAT?
- Do they understand trade-offs and implications?

## 4. COMMUNICATION (0-10):
- Explained clearly and logically?
- Used examples or analogies?
- Structured response well?
- Technical terminology used correctly?

## 5. PROBLEM-SOLVING (0-10, for coding/design questions):
- Asked clarifying questions?
- Discussed edge cases?
- Considered time/space complexity?
- Explained trade-offs?
- Systematic approach?

Return ONLY valid JSON:
{{
  "correctness": 0-10,
  "completeness": 0-10,
  "depth": 0-10,
  "communication": 0-10,
  "problem_solving": 0-10 or null,
  "overall_score": 0-100,
  "weighted_score": 0-100,
  "performance_level": "Excellent|Good|Satisfactory|Needs Improvement",
  "what_they_got_right": [
    "Correctly explained X",
    "Good understanding of Y"
  ],
  "what_they_got_wrong": [
    "Incorrect about Z - actually it works like...",
    "Misconception about A"
  ],
  "what_they_missed": [
    "Didn't mention B",
    "Failed to discuss C"
  ],
  "conceptual_gaps": [
    "Doesn't understand the difference between X and Y",
    "Weak on Z concept"
  ],
  "improvement_suggestions": [
    "Study X topic more deeply",
    "Practice explaining Y with examples",
    "Review Z fundamentals"
  ],
  "follow_up_questions": [
    "Can you explain how X handles edge case Y?",
    "What would happen if Z occurred?"
  ]
}}

SCORING WEIGHTS (for weighted_score):
- Conceptual questions: correctness (40%), completeness (25%), depth (20%), communication (15%)
- Coding questions: correctness (30%), problem_solving (30%), communication (20%), completeness (20%)
- System design: completeness (30%), problem_solving (25%), depth (25%), communication (20%)
"""

    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient(provider="openai", model="gpt-4")

    def evaluate(
        self,
        question: TechnicalQuestion,
        transcript: str
    ) -> TechnicalEvaluation:
        """Evaluate a technical interview response"""

        # Basic validation
        if len(transcript.strip()) < 30:
            return self._create_insufficient_response_evaluation(question.type)

        prompt = self.EVALUATION_PROMPT.format(
            question=question.question,
            domain=question.domain,
            question_type=question.type,
            expected_answer=question.expected_answer_outline,
            skills_tested=", ".join(question.skills_tested),
            transcript=transcript
        )

        response = self.llm_client.generate_json(prompt)

        try:
            evaluation = TechnicalEvaluation(**response)

            # Calculate weighted score based on question type
            evaluation.weighted_score = self._calculate_weighted_score(
                evaluation,
                question.type
            )

            return evaluation
        except Exception as e:
            raise ValueError(f"Failed to parse evaluation: {e}\nResponse: {response}")

    def _calculate_weighted_score(
        self,
        evaluation: TechnicalEvaluation,
        question_type: str
    ) -> float:
        """Calculate weighted score based on question type"""

        weights = {
            "conceptual": {
                "correctness": 0.40,
                "completeness": 0.25,
                "depth": 0.20,
                "communication": 0.15
            },
            "coding": {
                "correctness": 0.30,
                "problem_solving": 0.30,
                "communication": 0.20,
                "completeness": 0.20
            },
            "system_design": {
                "completeness": 0.30,
                "problem_solving": 0.25,
                "depth": 0.25,
                "communication": 0.20
            }
        }

        weight_map = weights.get(question_type, weights["conceptual"])

        score = 0.0
        score += evaluation.correctness * weight_map.get("correctness", 0)
        score += evaluation.completeness * weight_map.get("completeness", 0)
        score += evaluation.depth * weight_map.get("depth", 0)
        score += evaluation.communication * weight_map.get("communication", 0)

        if evaluation.problem_solving is not None:
            score += evaluation.problem_solving * weight_map.get("problem_solving", 0)

        return score * 10  # Convert to 0-100 scale

    def _create_insufficient_response_evaluation(
        self,
        question_type: str
    ) -> TechnicalEvaluation:
        """Return evaluation for very short/insufficient responses"""
        return TechnicalEvaluation(
            correctness=0,
            completeness=0,
            depth=0,
            communication=0,
            problem_solving=0 if question_type in ["coding", "system_design"] else None,
            overall_score=10,
            weighted_score=10.0,
            performance_level="Needs Improvement",
            what_they_got_right=[],
            what_they_got_wrong=[],
            what_they_missed=["Entire answer - response too short or incomplete"],
            conceptual_gaps=["Unable to assess due to insufficient response"],
            improvement_suggestions=[
                "Provide a complete answer with explanation",
                "Take time to think through the question",
                "Explain your reasoning step by step"
            ]
        )
```

**Success Criteria:**
- ✅ Correctly identify technical errors
- ✅ Assess depth of understanding
- ✅ Provide specific improvement suggestions
- ✅ Weighted scoring based on question type

---

### **PHASE 7: Scoring & Feedback Engine** ⏱️ 3-4 hours
**Priority:** HIGH (MVP)

#### 7.1 Overall Scoring System
```python
# src/scoring/scorer.py
from src.evaluator.behavioral import BehavioralEvaluation
from src.evaluator.technical import TechnicalEvaluation
from typing import List, Dict, Any, Union
from pydantic import BaseModel
import statistics

class InterviewScore(BaseModel):
    overall_score: float  # 0-100
    performance_level: str

    # Component Scores
    component_scores: Dict[str, float]

    # Breakdown
    behavioral_avg: Optional[float] = None
    technical_avg: Optional[float] = None

    # Feedback
    top_strengths: List[str]
    top_weaknesses: List[str]
    priority_improvements: List[str]

    # Confidence
    confidence: str  # "high", "medium", "low"

class Scorer:
    """Calculate overall interview performance scores"""

    PERFORMANCE_LEVELS = {
        (90, 100): "Excellent - Ready for interviews",
        (75, 89): "Good - Minor improvements needed",
        (60, 74): "Satisfactory - Practice key areas",
        (45, 59): "Needs Improvement - Focus on fundamentals",
        (0, 44): "Poor - Significant preparation required"
    }

    def calculate_overall_score(
        self,
        behavioral_evaluations: List[BehavioralEvaluation],
        technical_evaluations: List[TechnicalEvaluation],
        interview_type: str = "mixed"  # "behavioral", "technical", "mixed"
    ) -> InterviewScore:
        """Calculate overall interview performance score"""

        # Calculate averages
        behavioral_avg = None
        if behavioral_evaluations:
            behavioral_avg = statistics.mean([e.overall_score for e in behavioral_evaluations])

        technical_avg = None
        if technical_evaluations:
            technical_avg = statistics.mean([e.weighted_score for e in technical_evaluations])

        # Determine weights based on interview type
        if interview_type == "behavioral":
            weights = {"behavioral": 1.0, "technical": 0.0}
        elif interview_type == "technical":
            weights = {"behavioral": 0.0, "technical": 1.0}
        else:  # mixed
            weights = {"behavioral": 0.5, "technical": 0.5}

        # Calculate overall score
        overall_score = 0.0
        if behavioral_avg is not None:
            overall_score += behavioral_avg * weights["behavioral"]
        if technical_avg is not None:
            overall_score += technical_avg * weights["technical"]

        # Determine performance level
        performance_level = self._get_performance_level(overall_score)

        # Component scores
        component_scores = {
            "content_quality": overall_score * 0.40,
            "communication": self._calculate_communication_score(
                behavioral_evaluations, technical_evaluations
            ) * 0.30,
            "technical_accuracy": technical_avg * 0.20 if technical_avg else 0,
            "behavioral_structure": behavioral_avg * 0.10 if behavioral_avg else 0
        }

        # Aggregate feedback
        top_strengths = self._aggregate_strengths(
            behavioral_evaluations, technical_evaluations
        )
        top_weaknesses = self._aggregate_weaknesses(
            behavioral_evaluations, technical_evaluations
        )
        priority_improvements = self._prioritize_improvements(
            behavioral_evaluations, technical_evaluations
        )

        # Confidence assessment
        confidence = self._assess_confidence(
            behavioral_evaluations, technical_evaluations
        )

        return InterviewScore(
            overall_score=overall_score,
            performance_level=performance_level,
            component_scores=component_scores,
            behavioral_avg=behavioral_avg,
            technical_avg=technical_avg,
            top_strengths=top_strengths[:5],
            top_weaknesses=top_weaknesses[:5],
            priority_improvements=priority_improvements[:5],
            confidence=confidence
        )

    def _get_performance_level(self, score: float) -> str:
        """Map score to performance level"""
        for (low, high), level in self.PERFORMANCE_LEVELS.items():
            if low <= score <= high:
                return level
        return "Unknown"

    def _calculate_communication_score(
        self,
        behavioral_evals: List[BehavioralEvaluation],
        technical_evals: List[TechnicalEvaluation]
    ) -> float:
        """Calculate communication score from evaluations"""
        comm_scores = []

        for be in behavioral_evals:
            comm_scores.append(be.clarity)

        for te in technical_evals:
            comm_scores.append(te.communication)

        return statistics.mean(comm_scores) * 10 if comm_scores else 0

    def _aggregate_strengths(
        self,
        behavioral_evals: List[BehavioralEvaluation],
        technical_evals: List[TechnicalEvaluation]
    ) -> List[str]:
        """Aggregate and deduplicate strengths"""
        all_strengths = []

        for be in behavioral_evals:
            all_strengths.extend(be.strengths)

        for te in technical_evals:
            all_strengths.extend(te.what_they_got_right)

        # Count frequency and return most common
        from collections import Counter
        strength_counts = Counter(all_strengths)
        return [s for s, _ in strength_counts.most_common(5)]

    def _aggregate_weaknesses(
        self,
        behavioral_evals: List[BehavioralEvaluation],
        technical_evals: List[TechnicalEvaluation]
    ) -> List[str]:
        """Aggregate and deduplicate weaknesses"""
        all_weaknesses = []

        for be in behavioral_evals:
            all_weaknesses.extend(be.weaknesses)

        for te in technical_evals:
            all_weaknesses.extend(te.what_they_got_wrong + te.what_they_missed)

        from collections import Counter
        weakness_counts = Counter(all_weaknesses)
        return [w for w, _ in weakness_counts.most_common(5)]

    def _prioritize_improvements(
        self,
        behavioral_evals: List[BehavioralEvaluation],
        technical_evals: List[TechnicalEvaluation]
    ) -> List[str]:
        """Identify and prioritize top improvements"""
        improvements = []

        # Behavioral patterns
        missing_star = {"situation": 0, "task": 0, "action": 0, "result": 0}
        for be in behavioral_evals:
            for component, data in be.star_scores.items():
                if not data.present or data.score < 5:
                    missing_star[component] += 1

        # Find most common missing component
        max_missing = max(missing_star.values())
        if max_missing > 0:
            for component, count in missing_star.items():
                if count == max_missing:
                    improvements.append(
                        f"Consistently include {component.upper()} in your STAR responses ({count}/{len(behavioral_evals)} answers missing this)"
                    )
                    break

        # Add priority improvements from evaluations
        for be in behavioral_evals:
            if be.priority_improvement:
                improvements.append(be.priority_improvement)

        for te in technical_evals:
            improvements.extend(te.improvement_suggestions[:2])

        # Deduplicate and prioritize
        return list(dict.fromkeys(improvements))[:5]

    def _assess_confidence(
        self,
        behavioral_evals: List[BehavioralEvaluation],
        technical_evals: List[TechnicalEvaluation]
    ) -> str:
        """Assess confidence in the scoring"""
        total_questions = len(behavioral_evals) + len(technical_evals)

        if total_questions >= 8:
            return "high"
        elif total_questions >= 4:
            return "medium"
        else:
            return "low"
```

#### 7.2 Feedback Generator
```python
# src/scoring/feedback.py
from src.scoring.scorer import InterviewScore
from typing import Dict, Any

class FeedbackGenerator:
    """Generate human-readable feedback reports"""

    def generate_report(self, score: InterviewScore) -> Dict[str, Any]:
        """Generate comprehensive feedback report"""

        report = {
            "summary": self._generate_summary(score),
            "detailed_scores": self._format_scores(score),
            "strengths": score.top_strengths,
            "areas_for_improvement": score.top_weaknesses,
            "action_items": score.priority_improvements,
            "next_steps": self._generate_next_steps(score)
        }

        return report

    def _generate_summary(self, score: InterviewScore) -> str:
        """Generate overall summary"""
        summary = f"Overall Performance: {score.performance_level}\n"
        summary += f"Score: {score.overall_score:.1f}/100\n\n"

        if score.behavioral_avg and score.technical_avg:
            summary += f"Behavioral: {score.behavioral_avg:.1f}/100\n"
            summary += f"Technical: {score.technical_avg:.1f}/100\n"

        summary += f"\nConfidence in assessment: {score.confidence.upper()}"

        return summary

    def _format_scores(self, score: InterviewScore) -> Dict[str, str]:
        """Format component scores for display"""
        return {
            component: f"{value:.1f}/100"
            for component, value in score.component_scores.items()
        }

    def _generate_next_steps(self, score: InterviewScore) -> List[str]:
        """Generate actionable next steps"""
        next_steps = []

        if score.overall_score < 60:
            next_steps.append("Focus on fundamentals - review STAR framework and technical concepts")
            next_steps.append("Practice with 5-10 more mock questions in weak areas")
            next_steps.append("Record yourself answering questions and review")
        elif score.overall_score < 75:
            next_steps.append("Practice 3-5 more questions in identified weak areas")
            next_steps.append("Work on specific improvements listed above")
        elif score.overall_score < 90:
            next_steps.append("Polish your best answers for common questions")
            next_steps.append("Address minor gaps in technical knowledge")
        else:
            next_steps.append("You're ready! Keep practicing to maintain sharpness")
            next_steps.append("Review your best answers before actual interviews")

        return next_steps
```

**Success Criteria:**
- ✅ Accurate overall score calculation
- ✅ Clear performance level assignment
- ✅ Prioritized, actionable feedback
- ✅ Pattern detection (e.g., always missing Result in STAR)

---

### **PHASE 8: Integration Layer & API** ⏱️ 2-3 hours
**Priority:** CRITICAL (MVP)

#### 8.1 Main API Interface
```python
# src/api.py
from src.resume_parser.parser import ResumeParser
from src.question_generator.behavioral import BehavioralQuestionGenerator
from src.question_generator.technical import TechnicalQuestionGenerator
from src.evaluator.behavioral import BehavioralEvaluator
from src.evaluator.technical import TechnicalEvaluator
from src.scoring.scorer import Scorer
from src.scoring.feedback import FeedbackGenerator
from src.utils.llm_client import LLMClient
from typing import List, Dict, Any, Optional
import os

class PrepWiseAI:
    """
    Main API interface for PrepWise AI/NLP Module

    This is the primary interface that Person 2's backend will use.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        provider: str = "openai",
        model: Optional[str] = None
    ):
        """
        Initialize PrepWise AI

        Args:
            api_key: OpenAI or Anthropic API key (defaults to env var)
            provider: "openai" or "anthropic"
            model: Model name (defaults to gpt-4 or claude-3-5-sonnet)
        """
        self.llm_client = LLMClient(
            provider=provider,
            model=model,
            temperature=0.0
        )

        # Initialize components
        self.resume_parser = ResumeParser(self.llm_client)
        self.behavioral_generator = BehavioralQuestionGenerator(self.llm_client)
        self.technical_generator = TechnicalQuestionGenerator(self.llm_client)
        self.behavioral_evaluator = BehavioralEvaluator(self.llm_client)
        self.technical_evaluator = TechnicalEvaluator(self.llm_client)
        self.scorer = Scorer()
        self.feedback_generator = FeedbackGenerator()

    # ===== RESUME OPERATIONS =====

    def parse_resume(self, file_path: str) -> Dict[str, Any]:
        """
        Parse resume and return structured data

        Args:
            file_path: Path to PDF or DOCX resume

        Returns:
            Structured resume data as dictionary
        """
        parsed_resume = self.resume_parser.parse_resume(file_path)
        return parsed_resume.model_dump()

    # ===== QUESTION GENERATION =====

    def generate_interview_questions(
        self,
        resume_data: Dict[str, Any],
        interview_type: str,
        domain: Optional[str] = None,
        num_questions: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate interview questions based on resume

        Args:
            resume_data: Parsed resume dictionary
            interview_type: "behavioral", "technical", or "both"
            domain: Required if technical - "algorithms", "web_development",
                    "machine_learning", "system_design"
            num_questions: Total number of questions

        Returns:
            List of question dictionaries
        """
        from src.resume_parser.schemas import ParsedResume
        parsed_resume = ParsedResume(**resume_data)

        questions = []

        if interview_type == "behavioral":
            behavioral_questions = self.behavioral_generator.generate_questions(
                parsed_resume, num_questions
            )
            questions = [
                {**q.model_dump(), "type": "behavioral"}
                for q in behavioral_questions
            ]

        elif interview_type == "technical":
            if not domain:
                raise ValueError("domain is required for technical interviews")

            technical_questions = self.technical_generator.generate_questions(
                domain, parsed_resume, num_questions
            )
            questions = [
                {**q.model_dump(), "type": "technical"}
                for q in technical_questions
            ]

        elif interview_type == "both":
            # Split questions between behavioral and technical
            num_behavioral = num_questions // 2
            num_technical = num_questions - num_behavioral

            if not domain:
                raise ValueError("domain is required for technical questions")

            behavioral_questions = self.behavioral_generator.generate_questions(
                parsed_resume, num_behavioral
            )
            technical_questions = self.technical_generator.generate_questions(
                domain, parsed_resume, num_technical
            )

            questions = [
                {**q.model_dump(), "type": "behavioral"}
                for q in behavioral_questions
            ] + [
                {**q.model_dump(), "type": "technical"}
                for q in technical_questions
            ]

        else:
            raise ValueError(f"Invalid interview_type: {interview_type}")

        return questions

    # ===== EVALUATION =====

    def evaluate_response(
        self,
        question: Dict[str, Any],
        transcript: str,
        question_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluate a single interview response

        Args:
            question: Question dictionary
            transcript: Candidate's response transcript
            question_type: "behavioral" or "technical" (auto-detected if not provided)

        Returns:
            Evaluation dictionary with scores and feedback
        """
        # Auto-detect type if not provided
        if not question_type:
            question_type = question.get("type", "behavioral")

        if question_type == "behavioral":
            evaluation = self.behavioral_evaluator.evaluate(
                question.get("question", str(question)),
                transcript
            )
            return {**evaluation.model_dump(), "type": "behavioral"}

        else:  # technical
            from src.question_generator.technical import TechnicalQuestion
            tech_question = TechnicalQuestion(**question)
            evaluation = self.technical_evaluator.evaluate(
                tech_question,
                transcript
            )
            return {**evaluation.model_dump(), "type": "technical"}

    def evaluate_full_interview(
        self,
        questions_and_responses: List[tuple],
        interview_type: str = "mixed"
    ) -> Dict[str, Any]:
        """
        Evaluate entire interview session

        Args:
            questions_and_responses: List of (question_dict, transcript) tuples
            interview_type: "behavioral", "technical", or "mixed"

        Returns:
            Complete interview evaluation with overall score and feedback
        """
        behavioral_evaluations = []
        technical_evaluations = []

        for question, transcript in questions_and_responses:
            question_type = question.get("type", "behavioral")

            if question_type == "behavioral":
                eval_result = self.behavioral_evaluator.evaluate(
                    question["question"],
                    transcript
                )
                behavioral_evaluations.append(eval_result)
            else:
                from src.question_generator.technical import TechnicalQuestion
                tech_question = TechnicalQuestion(**question)
                eval_result = self.technical_evaluator.evaluate(
                    tech_question,
                    transcript
                )
                technical_evaluations.append(eval_result)

        # Calculate overall score
        overall_score = self.scorer.calculate_overall_score(
            behavioral_evaluations,
            technical_evaluations,
            interview_type
        )

        # Generate feedback report
        feedback_report = self.feedback_generator.generate_report(overall_score)

        return {
            "overall_score": overall_score.model_dump(),
            "feedback_report": feedback_report,
            "individual_evaluations": {
                "behavioral": [e.model_dump() for e in behavioral_evaluations],
                "technical": [e.model_dump() for e in technical_evaluations]
            }
        }

    # ===== FEEDBACK =====

    def generate_feedback_report(
        self,
        evaluations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive feedback report from evaluations

        Args:
            evaluations: List of evaluation dictionaries

        Returns:
            Feedback report dictionary
        """
        from src.evaluator.behavioral import BehavioralEvaluation
        from src.evaluator.technical import TechnicalEvaluation

        behavioral_evals = []
        technical_evals = []

        for eval_data in evaluations:
            if eval_data.get("type") == "behavioral":
                behavioral_evals.append(BehavioralEvaluation(**eval_data))
            else:
                technical_evals.append(TechnicalEvaluation(**eval_data))

        overall_score = self.scorer.calculate_overall_score(
            behavioral_evals,
            technical_evals,
            "mixed"
        )

        return self.feedback_generator.generate_report(overall_score)
```

#### 8.2 Example Usage
```python
# examples/usage_examples.py

from src.api import PrepWiseAI

# Initialize
ai = PrepWiseAI(api_key="your-api-key", provider="openai")

# ===== EXAMPLE 1: Complete Flow =====

# Step 1: Parse Resume
resume_data = ai.parse_resume("examples/sample_resumes/john_doe.pdf")
print(f"Parsed resume for: {resume_data['contact']['name']}")

# Step 2: Generate Questions
questions = ai.generate_interview_questions(
    resume_data=resume_data,
    interview_type="both",
    domain="web_development",
    num_questions=10
)
print(f"Generated {len(questions)} questions")

# Step 3: User does interview via VAPI (Person 3's work)
# Transcripts come back...

# Mock transcripts for example
transcripts = [
    "In my role at XYZ Corp, we faced a situation where...",  # Behavioral
    "React's virtual DOM is an in-memory representation...",  # Technical
    # ... more transcripts
]

# Step 4: Evaluate Each Response
evaluations = []
for question, transcript in zip(questions, transcripts):
    evaluation = ai.evaluate_response(
        question=question,
        transcript=transcript
    )
    evaluations.append(evaluation)
    print(f"Q: {question['question'][:50]}... Score: {evaluation.get('overall_score', 0)}")

# Step 5: Get Overall Report
final_report = ai.evaluate_full_interview(
    questions_and_responses=list(zip(questions, transcripts)),
    interview_type="mixed"
)

print("\n===== FINAL REPORT =====")
print(final_report['feedback_report']['summary'])
print("\nTop Strengths:")
for strength in final_report['feedback_report']['strengths']:
    print(f"  ✓ {strength}")
print("\nPriority Improvements:")
for improvement in final_report['feedback_report']['action_items']:
    print(f"  → {improvement}")


# ===== EXAMPLE 2: Behavioral Only =====

behavioral_questions = ai.generate_interview_questions(
    resume_data=resume_data,
    interview_type="behavioral",
    num_questions=5
)

# Mock interview...
behavioral_transcript = "When I was leading the migration project..."

behavioral_eval = ai.evaluate_response(
    question=behavioral_questions[0],
    transcript=behavioral_transcript,
    question_type="behavioral"
)

print(f"\nSTAR Completeness: {behavioral_eval['star_scores']}")
print(f"Priority Improvement: {behavioral_eval['priority_improvement']}")


# ===== EXAMPLE 3: Technical Only =====

technical_questions = ai.generate_interview_questions(
    resume_data=resume_data,
    interview_type="technical",
    domain="algorithms",
    num_questions=5
)

technical_transcript = "To detect a cycle in a linked list, I would use two pointers..."

technical_eval = ai.evaluate_response(
    question=technical_questions[0],
    transcript=technical_transcript,
    question_type="technical"
)

print(f"\nTechnical Correctness: {technical_eval['correctness']}/10")
print(f"What they got right: {technical_eval['what_they_got_right']}")
print(f"What they missed: {technical_eval['what_they_missed']}")
```

**Success Criteria:**
- ✅ Clean, intuitive API
- ✅ Clear documentation with examples
- ✅ Easy for Person 2 to integrate
- ✅ All major workflows covered

---

### **PHASE 9: Testing & Validation** ⏱️ 3-4 hours
**Priority:** HIGH

#### 9.1 Unit Tests
```python
# tests/test_resume_parser.py
# tests/test_question_generator.py
# tests/test_evaluator.py
# tests/test_scorer.py
# tests/test_api.py

# See previous sections for specific test examples
```

#### 9.2 Integration Tests
```python
# tests/test_integration.py

def test_complete_interview_flow():
    """Test entire flow from resume to final report"""
    ai = PrepWiseAI()

    # Parse resume
    resume = ai.parse_resume("examples/sample_resumes/test.pdf")
    assert resume is not None

    # Generate questions
    questions = ai.generate_interview_questions(
        resume, "both", "web_development", 6
    )
    assert len(questions) == 6

    # Mock evaluations
    mock_transcripts = ["..." for _ in questions]

    # Get final report
    report = ai.evaluate_full_interview(
        list(zip(questions, mock_transcripts)),
        "mixed"
    )

    assert report['overall_score'] is not None
    assert 'feedback_report' in report
```

#### 9.3 Manual Testing Checklist
- [ ] Test with 3+ different resume formats
- [ ] Generate questions for all 4 technical domains
- [ ] Evaluate sample good/bad answers
- [ ] Verify feedback is actionable
- [ ] Test edge cases (minimal resume, very long answers, etc.)
- [ ] Integration test with Person 2's backend

**Success Criteria:**
- ✅ All unit tests pass
- ✅ Integration tests pass
- ✅ Manual testing shows expected behavior
- ✅ Edge cases handled gracefully

---

### **PHASE 10: Documentation** ⏱️ 2 hours
**Priority:** MEDIUM

#### 10.1 README.md
```markdown
# PrepWise AI/NLP Module

AI-powered interview preparation intelligence layer.

## Features
- Resume parsing (PDF/DOCX)
- Behavioral question generation (STAR framework)
- Technical question generation (4 domains)
- Response evaluation with detailed feedback
- Overall performance scoring

## Installation
[See Phase 1]

## Quick Start
[See API examples]

## API Reference
[Document all public methods]

## Integration Guide
[For Person 2]

## Testing
```bash
pytest tests/
```

## Architecture
[Diagram and explanation]
```

#### 10.2 API Documentation
- Document all public methods with examples
- Provide JSON schemas for all inputs/outputs
- Include error handling guide

**Success Criteria:**
- ✅ README with clear setup instructions
- ✅ API reference complete
- ✅ Integration guide for teammates

---

## Potential Problems & Mitigations

### 1. Resume Parsing Accuracy
**Problem:**
- Different resume formats (multi-column, tables, scanned PDFs)
- Text extraction may lose structure
- Inconsistent section headers

**Mitigation:**
- ✅ Use LLM-based extraction (more flexible than regex/rules)
- ✅ Start with well-formatted digital PDFs for testing
- ✅ Skip OCR for MVP (add post-hackathon)
- ✅ Pydantic validation ensures output structure
- ⚠️ Test with 5+ diverse resume formats early

---

### 2. LLM Hallucinations & Inconsistency
**Problem:**
- LLM might give inconsistent scores for same answer
- May make up facts or misjudge responses
- Evaluation can be subjective

**Mitigation:**
- ✅ Use temperature=0 for deterministic outputs
- ✅ Very detailed prompts with scoring rubrics and examples
- ✅ Ask LLM to quote evidence from transcript
- ✅ JSON mode for structured outputs
- ✅ Validate outputs with Pydantic schemas
- ⚠️ A/B test prompts with sample answers to calibrate

---

### 3. API Costs
**Problem:**
- Multiple LLM calls per interview (parsing + questions + evaluations)
- GPT-4 is expensive (~$0.03/1K input tokens, ~$0.06/1K output tokens)
- Could get costly with many users

**Mitigation:**
- ✅ Use GPT-4-mini for cheaper operations (parsing, question gen)
- ✅ Reserve GPT-4 for critical evaluation tasks
- ✅ Cache resume parsing results
- ✅ Implement token counting and monitoring
- ✅ Consider Claude for some tasks (better quality/price ratio)
- ⚠️ Calculate costs: ~5-10 API calls per interview session

**Example Cost Calculation:**
- Resume parsing: ~2K tokens in + ~1K out = $0.09 (GPT-4)
- Question generation: ~1K in + ~500 out = $0.06 (GPT-4-mini)
- Per-response evaluation: ~500 in + ~300 out = $0.04 (GPT-4)
- **Total per interview (10 questions):** ~$0.60-$1.00

---

### 4. Generic Questions
**Problem:**
- Questions might not be personalized to candidate
- Could ask "Tell me about yourself" type generic questions
- Defeats the purpose of resume-based customization

**Mitigation:**
- ✅ Explicitly require resume references in prompts
- ✅ Post-processing filter to remove generic questions
- ✅ Validate questions mention specific experiences/companies
- ✅ Fallback question banks if LLM fails
- ⚠️ Manual review of generated questions during testing

---

### 5. Evaluation Consistency
**Problem:**
- Same answer might score differently on different runs
- Subjectivity in what's "good enough" for each STAR component
- Hard to benchmark

**Mitigation:**
- ✅ Temperature=0 for consistency
- ✅ Detailed scoring rubrics in prompts (0-10 with descriptions)
- ✅ Ask for evidence/quotes
- ✅ Test with known good/mediocre/poor sample answers
- ⚠️ Create evaluation benchmark dataset

---

### 6. Integration Complexity with Person 2
**Problem:**
- Data schema mismatches
- Different expectations for API behavior
- Timing coordination

**Mitigation:**
- ✅ Define clear API contract EARLY
- ✅ Use Pydantic for schema validation
- ✅ Provide comprehensive examples and documentation
- ✅ Schedule integration testing time
- ✅ Use JSON for all data exchange
- ⚠️ Meet with Person 2 before starting implementation

---

### 7. Transcript Quality from VAPI
**Problem:**
- Speech-to-text errors ("I" → "eye", technical terms misspelled)
- Filler words ("um", "like", "you know")
- Incomplete sentences, poor grammar

**Mitigation:**
- ✅ LLM evaluation is robust to typos/grammar
- ✅ Focus on content over exact wording
- ✅ Test with realistic (messy) transcripts
- ✅ Don't penalize too heavily for speech-to-text errors
- ⚠️ Get sample VAPI transcripts from Person 3 early

---

### 8. Time Constraints (Hackathon)
**Problem:**
- Specification is extremely comprehensive
- 14 phases is too much for 24-36 hours
- Risk of not finishing MVP

**Mitigation:**
- ✅ **Prioritize Phases 1-8 as MVP** (critical path)
- ✅ Skip/simplify advanced features (analytics, vector DB, OCR)
- ✅ Use LLM for everything (faster than rule-based systems)
- ✅ Leverage libraries (don't reinvent the wheel)
- ⚠️ Have clear MVP definition agreed with team
- ⚠️ Timebox each phase - move on if stuck

**MVP vs Enhancement:**
```
MVP (Must Have):
✅ Resume parsing
✅ Behavioral + technical question generation
✅ STAR evaluation
✅ Technical evaluation
✅ Basic scoring
✅ Feedback generation
✅ API for integration

Enhancement (Nice to Have):
⏸️ Comparative analytics
⏸️ Progress tracking
⏸️ Vector database (LangChain/LlamaIndex)
⏸️ OCR for scanned PDFs
⏸️ All 4 technical domains → Start with 1-2
⏸️ Advanced NLP with spaCy
```

---

### 9. Different Experience Levels
**Problem:**
- New grads have minimal experience for question generation
- Senior candidates need harder, design-focused questions
- One-size-fits-all doesn't work

**Mitigation:**
- ✅ Detect experience level from resume (years, seniority)
- ✅ Adjust question difficulty dynamically
- ✅ Different question mix (junior: conceptual, senior: design)
- ✅ Have tiered question banks as fallback
- ✅ Adjust evaluation expectations

---

### 10. Domain Knowledge Gaps
**Problem:**
- Evaluating technical answers requires deep domain expertise
- LLM knowledge might be outdated or wrong
- Hard to assess cutting-edge technologies

**Mitigation:**
- ✅ Rely on LLM's broad knowledge (generally good for common topics)
- ✅ Include expected answer outlines in question generation
- ✅ Focus on fundamentals over trendy frameworks
- ✅ Test evaluations with domain experts if available
- ⚠️ Be transparent about evaluation limitations

---

### 11. Error Handling
**Problem:**
- API calls can fail (rate limits, timeouts, network errors)
- Invalid inputs (corrupted PDF, gibberish text)
- LLM might return malformed JSON

**Mitigation:**
- ✅ Retry logic with exponential backoff (tenacity library)
- ✅ Validate all inputs and outputs (Pydantic)
- ✅ Try/except blocks with meaningful error messages
- ✅ Fallback responses for critical failures
- ✅ Logging for debugging

---

### 12. Question Relevance for Technical Domains
**Problem:**
- Asking web dev questions to an ML candidate
- Not all candidates fit neatly into one domain
- Resume might span multiple domains

**Mitigation:**
- ✅ User selects domain explicitly (via frontend)
- ✅ Detect dominant domain from skills in resume
- ✅ Support "mixed" technical domain option
- ✅ Allow custom question selection

---

## MVP vs Enhancement Features

### **MVP (Must Have for Demo)**
**Core Functionality:**
- ✅ Resume parsing (PDF/DOCX) with LLM
- ✅ Behavioral question generation (STAR-based, resume-specific)
- ✅ Technical question generation (start with 1-2 domains: algorithms + web dev)
- ✅ STAR framework evaluation
- ✅ Technical evaluation (correctness, completeness, communication)
- ✅ Basic scoring (0-100) and performance levels
- ✅ Feedback generation (strengths, weaknesses, improvements)
- ✅ Clean API for Person 2 integration

**Time Estimate:** 20-24 hours

---

### **Enhancement (Nice to Have)**
**If Time Permits:**
- ⏸️ All 4 technical domains (ML + system design) - **+2 hours**
- ⏸️ Vector database for resume context (LangChain) - **+3 hours**
- ⏸️ Advanced spaCy entity extraction (supplement LLM) - **+2 hours**
- ⏸️ Comparative analytics (peer benchmarking) - **+4 hours**
- ⏸️ Progress tracking across sessions - **+3 hours**
- ⏸️ OCR for scanned PDFs (pytesseract) - **+2 hours**

**Priority Order:**
1. All 4 technical domains
2. Vector database (better question personalization)
3. OCR support
4. Analytics

---

### **Post-Hackathon**
**Future Improvements:**
- Fine-tuned models for evaluation
- Custom scoring models (scikit-learn)
- A/B tested prompts
- Cost optimization strategies
- User feedback integration
- Prompt versioning and management
- Real user testing and iteration

---

## Dependencies & Integration Points

### **You Depend On:**

#### **Person 2 (Backend Developer)**
- **API Contracts:**
  - Define JSON schemas for data exchange
  - Agree on API endpoints and request/response formats
  - Error handling conventions

- **Data Flow:**
  - Person 2 receives resume upload → calls your `parse_resume()`
  - Person 2 requests questions → calls your `generate_interview_questions()`
  - After interview, Person 2 sends transcripts → calls your `evaluate_full_interview()`

- **Coordination:**
  - Meet BEFORE coding to define schemas
  - Share Pydantic models or JSON examples
  - Schedule integration testing session

#### **Person 3 (VAPI/Voice Interface)**
- **Transcript Format:**
  - Need to know exact format of transcripts (plain text, JSON, timestamps?)
  - Need sample transcripts for testing evaluation

- **Speech Metrics:**
  - VAPI provides speech delivery metrics (pace, filler words, clarity)
  - How to incorporate into overall scoring?
  - Get sample output early

#### **Person 1 (Frontend Developer)**
- **Indirect Dependency:**
  - Frontend calls Person 2's backend, which calls your API
  - Need to ensure error messages are user-friendly
  - Response times should be reasonable (<5s for evaluation)

---

### **Others Depend On You:**

#### **Person 2 Needs From You:**
1. **Stable API:** Clear method signatures, consistent data formats
2. **Documentation:** How to use each function, what to expect
3. **Error Handling:** Meaningful error messages, no crashes
4. **Examples:** Sample code showing complete flow
5. **Schemas:** Pydantic models or JSON schema definitions
6. **Response Times:** Know how long each operation takes

#### **Person 1 Needs From You (via Person 2):**
1. **Fast Response Times:** Users waiting for feedback
2. **Actionable Feedback:** Clear, specific improvements
3. **Accurate Scores:** Scores that make sense to users
4. **Good Questions:** Relevant, resume-specific questions

---

### **Critical Coordination Needed:**

#### **Week 1 (Planning):**
- [ ] Meet with Person 2 to define API contracts
- [ ] Get sample VAPI transcript from Person 3
- [ ] Collect 3-5 sample resumes for testing
- [ ] Agree on data schemas with team

#### **During Development:**
- [ ] Share API documentation early
- [ ] Provide example code to Person 2
- [ ] Test with Person 2's backend regularly
- [ ] Share progress and blockers daily

#### **Integration Testing:**
- [ ] Schedule 2-3 hours before demo for integration
- [ ] Test complete flow: resume → questions → evaluation → feedback
- [ ] Verify error handling
- [ ] Load testing (if time permits)

#### **Demo Prep:**
- [ ] Prepare sample resumes and transcripts
- [ ] Rehearse complete flow
- [ ] Have backup plan if API fails (cached responses)

---

### **Data Schema Examples:**

#### **Resume Data (Output from parse_resume)**
```json
{
  "contact": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "555-1234",
    "linkedin": "linkedin.com/in/johndoe"
  },
  "education": [...],
  "experience": [...],
  "skills": {
    "technical": ["Python", "React", "AWS"],
    "tools": ["Git", "Docker"]
  },
  "experience_level": "mid"
}
```

#### **Question Format**
```json
{
  "question": "Tell me about a time when you had to debug a complex production issue at XYZ Corp...",
  "type": "behavioral",
  "competency": "Problem-Solving",
  "difficulty": "medium",
  "resume_reference": "Software Engineer at XYZ Corp"
}
```

#### **Evaluation Format**
```json
{
  "overall_score": 78,
  "performance_level": "Good - Minor improvements needed",
  "star_scores": {
    "situation": {"present": true, "score": 8},
    "task": {"present": true, "score": 7},
    "action": {"present": true, "score": 9},
    "result": {"present": false, "score": 3}
  },
  "priority_improvement": "Add measurable results to your answer"
}
```

---

## Recommended Timeline (Hackathon Context)

**Assumption:** 24-36 hour hackathon, working in sprints

### **Day 1 (12 hours)**

#### **Hours 1-3: Foundation**
- [ ] Project setup and structure
- [ ] Install dependencies
- [ ] Configure API keys
- [ ] Test LLM connectivity
- [ ] Build LLM client wrapper
- **Deliverable:** Working development environment

#### **Hours 4-6: Resume Parser**
- [ ] Implement text extraction (PDF/DOCX)
- [ ] Create Pydantic schemas
- [ ] Build LLM-based parser
- [ ] Test with 3 sample resumes
- **Deliverable:** Working resume parser

#### **Hours 7-9: Question Generation**
- [ ] Behavioral question generator
- [ ] Technical question generator (2 domains)
- [ ] Test with parsed resumes
- **Deliverable:** Relevant, personalized questions

#### **Hours 10-12: Break/Sleep**
- Rest and recharge
- Review progress with team

---

### **Day 2 (14 hours)**

#### **Hours 13-17: Behavioral Evaluation**
- [ ] STAR framework evaluator
- [ ] Prompt engineering for evaluation
- [ ] Test with sample answers (good/bad)
- [ ] Validate output format
- **Deliverable:** STAR evaluation working

#### **Hours 18-22: Technical Evaluation**
- [ ] Technical evaluator (conceptual, coding, design)
- [ ] Domain-specific evaluation logic
- [ ] Test with sample technical answers
- **Deliverable:** Technical evaluation working

#### **Hours 23-25: Scoring & Feedback**
- [ ] Overall scoring algorithm
- [ ] Performance level assignment
- [ ] Feedback generation
- [ ] Priority improvement detection
- **Deliverable:** Complete feedback system

#### **Hours 26-28: Integration & API**
- [ ] Build PrepWiseAI main API class
- [ ] Create example usage code
- [ ] Write documentation
- [ ] Test complete flow
- **Deliverable:** Integration-ready API

#### **Hours 29-30: Integration Testing**
- [ ] Meet with Person 2
- [ ] Test backend integration
- [ ] Fix bugs and issues
- [ ] Verify all workflows

#### **Hours 31-36: Polish & Demo Prep**
- [ ] Fix remaining bugs
- [ ] Optimize prompts
- [ ] Create demo script
- [ ] Prepare sample data
- [ ] Final testing
- [ ] Rehearse presentation

---

### **Buffer Time: 4-6 hours**
- Unexpected issues
- Integration problems
- Bug fixes
- Optimization

---

### **Parallel Work Opportunities:**
While you're building AI/NLP:
- **Person 1:** Frontend UI
- **Person 2:** Backend API structure, database
- **Person 3:** VAPI integration, voice interface

**Sync Points:**
- **Hour 6:** Share resume schema with Person 2
- **Hour 12:** Team sync - show progress
- **Hour 18:** Share question format with Person 2
- **Hour 24:** Team sync - integration discussion
- **Hour 28:** Full integration testing
- **Hour 34:** Final demo rehearsal

---

## Success Metrics

### **Technical Metrics**

#### **Resume Parsing:**
- **Accuracy:** >90% of key information extracted correctly
- **Coverage:** Extract all major sections (contact, education, experience, skills)
- **Robustness:** Handle 3+ different resume formats
- **Speed:** <5 seconds per resume

#### **Question Generation:**
- **Relevance:** 100% of questions reference specific resume content
- **Diversity:** Cover 5+ different competencies/skills
- **Quality:** No generic questions (manual review)
- **Speed:** <3 seconds for 5 questions

#### **Behavioral Evaluation:**
- **STAR Detection:** Correctly identify all 4 components in test cases
- **Consistency:** Same answer gets similar score (±5 points) across runs
- **Specificity:** Provide actionable feedback with quotes
- **Speed:** <4 seconds per evaluation

#### **Technical Evaluation:**
- **Accuracy:** Correctly identify technical errors in test cases
- **Fairness:** Appropriate difficulty assessment for experience level
- **Feedback Quality:** Specific improvement suggestions
- **Speed:** <4 seconds per evaluation

#### **Overall System:**
- **API Response Time:** <10 seconds for complete interview evaluation
- **Error Rate:** <5% API call failures (with retries)
- **Integration:** Zero crashes during demo

---

### **User Experience Metrics**

#### **Question Quality:**
- Questions feel personalized (not generic)
- Appropriate difficulty for candidate level
- Cover relevant skills from resume

#### **Feedback Quality:**
- Feedback is specific and actionable
- Users understand what to improve
- Scores correlate with perceived performance
- Priority improvements are clear

#### **Overall Experience:**
- Complete flow works smoothly
- Error messages are helpful
- Results are delivered quickly
- System feels intelligent and helpful

---

### **Integration Metrics**

#### **Person 2 Integration:**
- Clear API documentation
- Easy to understand and use
- Consistent data formats
- Good error handling
- Reasonable response times

#### **Demo Success:**
- All features work during demo
- No crashes or errors
- Impressive results
- Clear value proposition

---

## Technology Decisions

### **1. LLM Choice: OpenAI vs Claude**

#### **Recommendation: OpenAI GPT-4 (Primary) + GPT-4-mini (Cost Optimization)**

**Pros:**
- ✅ Better JSON mode (strict schema adherence)
- ✅ Cheaper than Claude for equivalent quality
- ✅ Faster response times
- ✅ Better documentation and tooling
- ✅ More predictable output formatting

**Cons:**
- ⚠️ Less nuanced than Claude for evaluation
- ⚠️ May need more detailed prompts

**Alternative Strategy:**
- Use **GPT-4-mini** for: Resume parsing, question generation (cheaper, faster)
- Use **GPT-4** for: Response evaluation (better quality needed)
- Consider **Claude** for: Complex evaluation cases (better at nuance)

**Cost Comparison:**
- GPT-4: $0.03/1K input, $0.06/1K output
- GPT-4-mini: $0.15/1M input, $0.60/1M output (20x cheaper!)
- Claude Sonnet: $0.003/1K input, $0.015/1K output

---

### **2. Resume Parsing: LLM vs Traditional NLP**

#### **Recommendation: LLM-Based Parsing**

**Why LLM:**
- ✅ Handles varied formats flexibly
- ✅ Understands context (distinguishes projects from jobs)
- ✅ Faster development (no regex maintenance)
- ✅ Better entity extraction (recognizes skills, technologies)
- ✅ Can infer missing information

**Why NOT Traditional NLP:**
- ❌ Requires extensive regex patterns
- ❌ Brittle with format changes
- ❌ Doesn't understand context well
- ❌ More development time

**Hybrid Approach (If Time):**
- Use LLM as primary
- Add spaCy for entity validation
- Use regex for specific patterns (email, phone)

**Rationale:** For hackathon, speed of development > cost optimization

---

### **3. Context Management: LangChain vs Direct LLM Calls**

#### **Recommendation: Start Without, Add If Needed**

**MVP: Direct LLM Calls**
- ✅ Simpler, less overhead
- ✅ Easier to debug
- ✅ Sufficient for stateless evaluations
- ✅ Faster to implement

**When to Add LangChain:**
- If you need conversation memory (follow-up questions)
- If you implement vector database for context
- If you need complex prompt chaining

**Enhancement Phase:**
- Use LangChain/LlamaIndex for:
  - Vector embeddings of resume
  - Semantic search for relevant context
  - Conversation memory across questions
  - Prompt template management

**Rationale:** Don't over-engineer for MVP. Add complexity only when needed.

---

### **4. Question Banks: LLM-Only vs Hybrid**

#### **Recommendation: LLM-Primary with Fallback Banks**

**Approach:**
1. **Primary:** LLM generates questions
2. **Validation:** Check if questions are specific enough
3. **Fallback:** Use predefined question banks if LLM fails or produces generic questions

**Benefits:**
- ✅ Best of both worlds (personalization + reliability)
- ✅ Graceful degradation if LLM fails
- ✅ Can still demo if API is down (use cached/fallback)

---

### **5. Data Validation: Pydantic vs Manual**

#### **Recommendation: Pydantic (Strongly Recommended)**

**Why Pydantic:**
- ✅ Automatic validation
- ✅ Type hints improve code quality
- ✅ Easy JSON serialization
- ✅ Clear error messages
- ✅ Self-documenting schemas

**Example:**
```python
from pydantic import BaseModel, EmailStr

class Contact(BaseModel):
    name: str
    email: EmailStr  # Automatically validates email format

# Usage
contact = Contact(name="John", email="invalid")  # Raises ValidationError
```

**Rationale:** Catches errors early, saves debugging time

---

### **6. Testing Strategy**

#### **Recommendation: Unit Tests + Manual Testing**

**Must Have:**
- Unit tests for core functions (parse, generate, evaluate)
- Integration test for complete flow
- Manual testing with real resumes

**Nice to Have:**
- Comprehensive test coverage
- Automated evaluation benchmarks

**Rationale:** Balance thoroughness with time constraints

---

### **7. Error Handling: Retry Logic**

#### **Recommendation: Use Tenacity Library**

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def call_llm(prompt):
    # API call
```

**Why:**
- ✅ Handles transient failures (rate limits, network issues)
- ✅ Exponential backoff prevents hammering API
- ✅ Clean, declarative syntax

---

## Critical Success Factors

### **1. Start with Clear Data Schemas**
- ❗ Define JSON schemas for ALL data exchange BEFORE coding
- ❗ Share schemas with Person 2 immediately
- ❗ Use Pydantic to enforce schemas
- ❗ Don't change schemas mid-way (breaks integration)

### **2. Test with Real Resumes Early**
- ❗ Collect 5+ sample resumes DAY 1
- ❗ Test parsing with varied formats
- ❗ Don't wait until end to discover format issues
- ❗ Use your own resume + teammates' resumes

### **3. Coordinate with Person 2 Frequently**
- ❗ Meet before starting implementation
- ❗ Share progress every 4-6 hours
- ❗ Sync on integration points
- ❗ Schedule dedicated integration testing time
- ❗ Integration issues are the #1 hackathon killer

### **4. Keep Prompts Modular**
- ❗ Store prompts in separate files or constants
- ❗ Use f-strings or .format() for templating
- ❗ Easy to iterate and improve
- ❗ Version prompts if making significant changes

### **5. Build MVP First**
- ❗ Don't get distracted by fancy features
- ❗ Phases 1-8 are critical path
- ❗ Test each phase before moving to next
- ❗ If behind schedule, cut scope (not quality)

### **6. Document as You Go**
- ❗ Don't leave documentation for the end
- ❗ Write docstrings immediately
- ❗ Create example code while building
- ❗ Add comments for complex logic
- ❗ Person 2 needs to understand your code

### **7. Have a Demo Plan**
- ❗ Prepare sample data ahead of time
- ❗ Rehearse complete flow
- ❗ Have backup plan if API fails (cached responses)
- ❗ Know exactly what you'll show and in what order

### **8. Prioritize Ruthlessly**
- ❗ If stuck on something for >30 mins, ask for help or move on
- ❗ Focus on what matters for demo
- ❗ MVP > Perfect
- ❗ Working demo > Beautiful code

### **9. Monitor API Usage & Costs**
- ❗ Set up cost alerts
- ❗ Monitor token usage
- ❗ Don't accidentally spend $100 debugging
- ❗ Use GPT-4-mini where possible

### **10. Communicate Blockers Immediately**
- ❗ Don't hide problems
- ❗ Ask for help early
- ❗ Team can adjust if they know issues
- ❗ Surprises at integration time are bad

---

## Next Steps

### **Immediate (Before Coding)**

#### **1. Team Alignment Meeting** (30 mins)
- [ ] Review this plan with team
- [ ] Get feedback and buy-in
- [ ] Clarify any questions
- [ ] Agree on MVP scope

#### **2. API Contract Definition with Person 2** (1 hour)
- [ ] Define all data schemas (JSON examples)
- [ ] Agree on API method signatures
- [ ] Discuss error handling approach
- [ ] Share Pydantic models or JSON schema
- [ ] Document in shared doc

#### **3. Get Sample Data** (30 mins)
- [ ] Collect 5+ sample resumes (PDF and DOCX)
- [ ] Get sample VAPI transcript from Person 3
- [ ] Create test answers (good, mediocre, poor) for evaluation testing
- [ ] Store in `examples/` directory

#### **4. Environment Setup** (30 mins)
- [ ] Create git repository
- [ ] Set up project structure
- [ ] Create virtual environment
- [ ] Install base dependencies
- [ ] Configure API keys (.env)
- [ ] Test LLM connectivity

---

### **Start Coding (Phase 1)**

#### **Hour 1-3: Foundation**
Begin with Phase 1 implementation:
1. Create project structure
2. Set up requirements.txt
3. Build LLM client wrapper
4. Test API connectivity
5. Create Pydantic schemas

**Ready to start?** Let me know if you want me to:
1. Start implementing the code (beginning with Phase 1)
2. Create specific files (schemas, LLM client, etc.)
3. Set up the project structure
4. Help with API contract definition
5. Clarify any part of the plan

---

## Appendix: Prompt Library

### **Resume Parsing Prompt**
```
[See Phase 2.3 for full prompt]
```

### **Behavioral Question Generation Prompt**
```
[See Phase 3.1 for full prompt]
```

### **Technical Question Generation Prompt**
```
[See Phase 4.1 for full prompt]
```

### **Behavioral Evaluation Prompt**
```
[See Phase 5.1 for full prompt]
```

### **Technical Evaluation Prompt**
```
[See Phase 6.1 for full prompt]
```

---

## Appendix: Code Templates

### **Main API Interface Template**
```python
[See Phase 8.1 for complete code]
```

### **LLM Client Template**
```python
[See Phase 1.5 for complete code]
```

### **Pydantic Schemas Template**
```python
[See Phase 2.1 for complete code]
```

---

## Version History
- **v1.0 (2025-11-15):** Initial comprehensive plan

---

**End of Implementation Plan**

Good luck with the hackathon! 🚀
