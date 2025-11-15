# PrepWise AI/NLP Module

AI-powered interview preparation intelligence layer for PrepWise platform.

## Features

- **Resume Parsing**: Extract structured data from PDF/DOCX resumes
- **Behavioral Questions**: Generate STAR framework questions tailored to candidate's resume
- **Technical Questions**: Generate domain-specific technical questions (algorithms, web dev, ML, system design)
- **Response Evaluation**: Evaluate behavioral (STAR) and technical responses
- **Feedback Generation**: Provide actionable feedback and improvement suggestions
- **Performance Scoring**: Calculate overall interview performance (0-100)

## Quick Start

### 1. Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
# OPENAI_API_KEY=your_key_here
```

### 3. Usage

```python
from src.api import PrepWiseAI

# Initialize
ai = PrepWiseAI(api_key="your-openai-key")

# Parse resume
resume_data = ai.parse_resume("path/to/resume.pdf")

# Generate questions
questions = ai.generate_interview_questions(
    resume_data=resume_data,
    interview_type="both",
    domain="web_development",
    num_questions=10
)

# Evaluate responses (after interview)
evaluation = ai.evaluate_response(
    question=questions[0],
    transcript="candidate's answer..."
)

# Get full report
report = ai.evaluate_full_interview(
    questions_and_responses=list(zip(questions, transcripts)),
    interview_type="mixed"
)
```

## Project Structure

```
prepwise-ai/
├── src/
│   ├── resume_parser/      # Resume parsing and extraction
│   ├── question_generator/ # Question generation (behavioral + technical)
│   ├── evaluator/          # Response evaluation
│   ├── scoring/            # Scoring and feedback
│   ├── utils/              # Utilities (LLM client, validators)
│   └── api.py              # Main API interface
├── prompts/                # LLM prompt templates
├── tests/                  # Unit and integration tests
├── examples/               # Usage examples and sample data
└── requirements.txt        # Dependencies
```

## API Reference

### Main API Class: `PrepWiseAI`

#### `parse_resume(file_path: str) -> dict`
Parse resume and return structured data.

#### `generate_interview_questions(resume_data, interview_type, domain=None, num_questions=5) -> list`
Generate interview questions based on resume.

#### `evaluate_response(question, transcript, question_type=None) -> dict`
Evaluate a single interview response.

#### `evaluate_full_interview(questions_and_responses, interview_type="mixed") -> dict`
Evaluate entire interview session and generate comprehensive report.

## Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_resume_parser.py
```

## Development

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

## Technology Stack

- **LLM**: OpenAI GPT-4 / Anthropic Claude
- **Resume Parsing**: PyPDF2, python-docx
- **NLP**: spaCy, LangChain
- **Data Validation**: Pydantic
- **Testing**: pytest

## License

MIT License - PrepWise Hackathon Project

## Team

**Person 4**: AI/NLP Engineer
- Resume parsing
- Question generation
- Response evaluation
- Feedback and scoring

## Documentation

For detailed implementation plan, see: [AI_NLP_IMPLEMENTATION_PLAN.md](../AI_NLP_IMPLEMENTATION_PLAN.md)
