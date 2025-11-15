# PrepWise AI - Setup Guide

## Phase 1 Complete! ✅

Your project structure has been created and Phase 1 is implemented.

## Quick Start

### 1. Install Dependencies

```bash
cd prepwise-ai

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model (for future NLP tasks)
python -m spacy download en_core_web_sm
```

### 2. Configure API Keys

```bash
# Edit the .env file and add your OpenAI API key
# Open .env in your editor and replace:
# OPENAI_API_KEY=your_openai_api_key_here

# With your actual API key from: https://platform.openai.com/api-keys
```

### 3. Test Your Setup

```bash
# Run the setup test script
python test_setup.py
```

This will verify:
- ✅ Environment variables are configured
- ✅ All packages are installed
- ✅ LLM client can connect to OpenAI
- ✅ Pydantic schemas work correctly
- ✅ Validators are functional

### 4. Expected Output

If everything is working, you should see:

```
🎉 All tests passed! Phase 1 setup is complete!

Next steps:
1. Start implementing Phase 2 (Resume Parser)
2. Add sample resumes to examples/sample_resumes/
3. Test with real resume data
```

## Project Structure

```
prepwise-ai/
├── src/
│   ├── __init__.py
│   ├── api.py                    # Main API interface (to implement)
│   ├── resume_parser/
│   │   ├── __init__.py
│   │   ├── extractors.py         # PDF/DOCX extraction (to implement)
│   │   ├── parser.py             # LLM-based parsing (to implement)
│   │   └── schemas.py            # ✅ Pydantic models (DONE)
│   ├── question_generator/
│   │   ├── __init__.py
│   │   ├── behavioral.py         # STAR questions (to implement)
│   │   ├── technical.py          # Technical questions (to implement)
│   │   └── question_banks.py     # Fallback questions (to implement)
│   ├── evaluator/
│   │   ├── __init__.py
│   │   ├── behavioral.py         # STAR evaluation (to implement)
│   │   └── technical.py          # Technical evaluation (to implement)
│   ├── scoring/
│   │   ├── __init__.py
│   │   ├── scorer.py             # Overall scoring (to implement)
│   │   └── feedback.py           # Feedback generation (to implement)
│   └── utils/
│       ├── __init__.py
│       ├── llm_client.py         # ✅ LLM wrapper (DONE)
│       └── validators.py         # ✅ Validators (DONE)
├── prompts/                      # LLM prompt templates (to create)
├── tests/                        # Unit tests (to implement)
├── examples/
│   ├── sample_resumes/           # Add your test resumes here
│   └── usage_examples.py         # Example code (to create)
├── .env                          # ⚠️  ADD YOUR API KEY HERE
├── .env.example                  # Template
├── .gitignore                    # ✅ Git ignore rules
├── requirements.txt              # ✅ Dependencies
├── setup.py                      # ✅ Package setup
├── README.md                     # ✅ Documentation
└── test_setup.py                 # ✅ Phase 1 test script
```

## What's Implemented (Phase 1)

### ✅ LLM Client (`src/utils/llm_client.py`)
- Unified interface for OpenAI and Anthropic
- Automatic retry logic with exponential backoff
- JSON mode support
- Token counting
- Error handling

### ✅ Validators (`src/utils/validators.py`)
- File path validation
- Email/URL validation
- Text sanitization
- Score validation
- Years of experience extraction

### ✅ Resume Schemas (`src/resume_parser/schemas.py`)
- Complete Pydantic models for all resume sections
- Automatic experience level detection
- Helper methods (summary, counts, etc.)
- Input validation and sanitization

### ✅ Configuration
- `.env` file for API keys
- `requirements.txt` with all dependencies
- `.gitignore` for clean git commits
- `setup.py` for package installation

## Next Phase: Resume Parser (Phase 2)

Once your setup test passes, you'll implement:

1. **Text Extraction** (`extractors.py`)
   - PDF text extraction (PyPDF2)
   - DOCX text extraction (python-docx)
   - Text cleaning

2. **LLM-Based Parsing** (`parser.py`)
   - Resume parsing with GPT-4
   - Entity extraction
   - Structured data output

## Troubleshooting

### "OPENAI_API_KEY not set"
- Open `.env` file
- Replace `your_openai_api_key_here` with your actual API key
- Get API key from: https://platform.openai.com/api-keys

### "Package not installed"
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

### "API call failed"
- Check your API key is valid
- Check your OpenAI account has credits
- Check internet connection

### Import errors
- Make sure you're in the `prepwise-ai` directory
- Make sure virtual environment is activated
- Try: `pip install -e .` to install in development mode

## Cost Estimation

Phase 1 testing uses minimal tokens:
- Test API call: ~$0.0001
- JSON test: ~$0.0002
- **Total: < $0.001** per test run

## Need Help?

1. Check the detailed implementation plan: `../AI_NLP_IMPLEMENTATION_PLAN.md`
2. Review the README: `README.md`
3. Ask your teammates (especially Person 2 for integration)

## Ready to Continue?

Once setup test passes:
```bash
# You're ready to start Phase 2!
# Next: Implement resume parser
```

Good luck! 🚀
