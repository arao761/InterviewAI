# PrepWise AI - Quick Start Guide

## ✅ Phase 1 Complete!

All setup tests are passing. You're ready to start building!

## Using the Virtual Environment

**IMPORTANT**: Always activate the virtual environment before working:

```bash
# Activate virtual environment
source venv/bin/activate

# You'll see (venv) in your terminal prompt
# (venv) user@computer:~/prepwise-ai$
```

When you're done:
```bash
deactivate
```

## Running Tests

```bash
# Make sure venv is activated!
source venv/bin/activate

# Run setup test
python test_setup.py

# Run unit tests (when implemented)
pytest tests/

# Run specific test file
pytest tests/test_resume_parser.py
```

## What Works Now

✅ **Environment**: API keys configured, dependencies installed
✅ **LLM Client**: Can make calls to OpenAI GPT-4
✅ **Schemas**: Complete Pydantic models for resume data
✅ **Validators**: Input validation and sanitization utilities
✅ **Project Structure**: All files and directories created

## What's Next: Phase 2 - Resume Parser

Implement these files (4-6 hours):

### 1. Text Extractors (`src/resume_parser/extractors.py`)
- Extract text from PDF files (PyPDF2)
- Extract text from DOCX files (python-docx)
- Clean and sanitize extracted text

### 2. Resume Parser (`src/resume_parser/parser.py`)
- Use LLM to extract structured data from resume text
- Convert to ParsedResume Pydantic model
- Calculate experience level and metadata

### 3. Test (`tests/test_resume_parser.py`)
- Unit tests for text extraction
- Unit tests for parsing
- Test with sample resumes

## Development Workflow

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Make your changes to code

# 3. Test frequently
python test_setup.py  # Quick sanity check
pytest tests/         # Full test suite

# 4. Format code (optional but recommended)
black src/ tests/

# 5. Commit your changes
git add .
git commit -m "Implement Phase 2: Resume Parser"
```

## Project Commands Cheat Sheet

```bash
# Virtual Environment
source venv/bin/activate              # Activate
deactivate                             # Deactivate
which python                           # Check if venv is active

# Dependencies
pip install -r requirements.txt        # Install all dependencies
pip freeze > requirements.txt          # Update requirements (if needed)
pip install <package>                  # Install new package

# Testing
python test_setup.py                   # Phase 1 setup test
pytest tests/                          # All tests
pytest tests/ -v                       # Verbose output
pytest tests/ --cov=src                # With coverage

# Code Quality
black src/ tests/                      # Format code
flake8 src/ tests/                     # Lint code
mypy src/                              # Type checking

# Python Interactive
python                                 # Start Python REPL
python -i src/utils/llm_client.py     # Load module interactively
```

## Testing LLM Client Interactively

```python
# In Python REPL (after activating venv)
from src.utils.llm_client import LLMClient

# Initialize client
client = LLMClient(provider="openai", model="gpt-4o-mini")

# Test simple generation
response = client.generate("What is 2+2?")
print(response)

# Test JSON generation
json_response = client.generate_json(
    "Return a JSON with 'name': 'PrepWise' and 'status': 'ready'"
)
print(json_response)
```

## Common Issues & Solutions

### Virtual environment not activated
**Symptom**: `ModuleNotFoundError: No module named 'openai'`
**Solution**: `source venv/bin/activate`

### Wrong Python version
**Symptom**: Dependencies won't install
**Solution**: Use Python 3.9+ (`python3 --version`)

### API call fails
**Symptom**: `OpenAI API error`
**Solution**:
1. Check API key in `.env` is correct
2. Check you have credits in OpenAI account
3. Check internet connection

### Import errors
**Symptom**: `ModuleNotFoundError` even with venv active
**Solution**: `pip install -r requirements.txt` again

## File Locations Quick Reference

```
Current working directory: /Users/ankitrao/Claude-Hackathon/prepwise-ai

Key files:
- .env                          # Your API keys (EDIT THIS)
- test_setup.py                 # Phase 1 test (RUN THIS)
- src/utils/llm_client.py      # LLM wrapper (DONE ✅)
- src/resume_parser/schemas.py # Pydantic models (DONE ✅)
- src/resume_parser/parser.py  # Resume parser (TODO 📝)

Next to implement:
- src/resume_parser/extractors.py
- src/resume_parser/parser.py
- tests/test_resume_parser.py
```

## Cost Tracking

Phase 1 testing costs:
- Setup test: ~$0.001 per run
- API connectivity test: ~$0.0001

Phase 2 estimated costs:
- Resume parsing: ~$0.05-0.10 per resume (using GPT-4)
- Can use GPT-4-mini to reduce costs by 20x

Monitor your usage:
- OpenAI Dashboard: https://platform.openai.com/usage

## Team Coordination

### Before Phase 2
- [ ] Share resume data schema with Person 2
- [ ] Get sample VAPI transcripts from Person 3
- [ ] Collect 3-5 test resumes

### During Phase 2
- [ ] Update Person 2 on progress
- [ ] Test with different resume formats
- [ ] Document any schema changes

### Before Phase 8 (Integration)
- [ ] Define complete API contract with Person 2
- [ ] Provide example usage code
- [ ] Schedule integration testing time

## Next Steps

1. **Add sample resumes** to `examples/sample_resumes/`
   - Get your own resume
   - Ask teammates for theirs
   - Download 1-2 public resumes for testing

2. **Implement Phase 2: Resume Parser**
   - Start with `src/resume_parser/extractors.py`
   - Then `src/resume_parser/parser.py`
   - Test as you go

3. **Stay in sync with team**
   - Daily standup/updates
   - Share schemas and progress
   - Ask for help when stuck

## Ready to Code?

```bash
# Let's go!
source venv/bin/activate
python  # Start coding interactively, or
# Start editing src/resume_parser/extractors.py
```

Good luck! 🚀
