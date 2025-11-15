# Phase 1 Testing Guide

This guide shows you how to test all components of Phase 1 setup.

## Quick Test (Recommended)

Run the comprehensive test script that verifies everything:

```bash
cd voice
source venv/bin/activate  # On Windows: venv\Scripts\activate
python tests/test_phase1_setup.py
```

This will test:
- ✅ All required Python packages are installed
- ✅ Project structure is complete
- ✅ Configuration module works
- ✅ Audio utilities are functional
- ✅ FastAPI application is set up correctly
- ✅ All API endpoints respond correctly
- ✅ Security (.env in .gitignore)

## Manual Testing Steps

### 1. Test Module Imports

```bash
cd voice
source venv/bin/activate
python -c "from config import Config; from main import app; from utils.audio_utils import validate_audio_file; print('✅ All imports successful')"
```

### 2. Test Configuration

```bash
python -c "from config import Config; print(Config.get_config_summary())"
```

This should show your configuration without exposing API keys.

### 3. Test FastAPI Server

**Start the server:**
```bash
python main.py
```

You should see:
```
🚀 Starting PrepWise Voice API...
📍 Server will be available at: http://localhost:8000
📚 API Documentation: http://localhost:8000/docs
❤️  Health Check: http://localhost:8000/health
```

**Note:** If you don't have `OPENAI_API_KEY` set in `.env`, the server will fail to start. That's expected - the validation happens on startup.

**Test endpoints (in another terminal):**

```bash
# Root endpoint
curl http://localhost:8000/

# Health check
curl http://localhost:8000/health

# Config endpoint
curl http://localhost:8000/config
```

Or visit in your browser:
- http://localhost:8000/docs - Interactive API documentation
- http://localhost:8000/health - Health check
- http://localhost:8000/ - Root endpoint

### 4. Test Audio Utilities

```bash
python -c "
from utils.audio_utils import validate_audio_file
result = validate_audio_file('nonexistent.mp3')
print('Validation result:', result)
"
```

### 5. Test with API Keys (After Configuration)

Once you've added your `OPENAI_API_KEY` to `.env`:

#### Test Whisper API:
```bash
# First, add a sample audio file
# Place a file at: tests/test_audio_samples/sample.mp3

python tests/test_whisper.py
```

#### Test TTS API:
```bash
python tests/test_tts.py
```

This will generate a test audio file at `tests/test_audio_samples/tts_test_output.mp3`

## Testing Checklist

- [ ] Run `test_phase1_setup.py` - All tests pass
- [ ] Verify imports work
- [ ] Check configuration loads
- [ ] Test FastAPI server starts (if API key is set)
- [ ] Visit `/docs` endpoint in browser
- [ ] Test `/health` endpoint
- [ ] Test `/config` endpoint
- [ ] Test audio utilities with sample file (optional)
- [ ] Test Whisper API with sample audio (requires API key)
- [ ] Test TTS API (requires API key)

## Common Issues

### Server Won't Start
**Problem:** `ValueError: OPENAI_API_KEY not set in .env file`

**Solution:** 
1. Copy `.env.example` to `.env`
2. Add your OpenAI API key to `.env`
3. Restart the server

### Import Errors
**Problem:** `ModuleNotFoundError`

**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Port Already in Use
**Problem:** `Address already in use`

**Solution:** 
- Kill the process using port 8000, or
- Change the port in `main.py` (line 143)

## Next Steps After Testing

Once all Phase 1 tests pass:

1. **Add API Keys** - Configure your `.env` file with actual API keys
2. **Test Real APIs** - Run Whisper and TTS tests with actual API calls
3. **Start Development** - Begin Phase 2: Frontend Audio Recording

## Automated Testing

For continuous testing, you can add this to your workflow:

```bash
# Run all Phase 1 tests
python tests/test_phase1_setup.py

# Run API tests (requires API keys and sample files)
python tests/test_whisper.py
python tests/test_tts.py
```

