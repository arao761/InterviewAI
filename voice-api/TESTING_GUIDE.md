# Comprehensive Testing Guide: Phases 1-3

This guide explains how to run comprehensive tests for all three phases of the PrepWise Voice API project.

## Test Files

### Backend Tests
- **`voice/tests/test_phases_1_3_comprehensive.py`** - Python test suite for backend
- **`voice/tests/test_phase1_setup.py`** - Phase 1 specific tests

### Frontend Tests
- **`frontend/test-phases-1-3.html`** - Interactive browser-based test suite
- **`frontend/test-phase2.html`** - Phase 2 specific tests with UI

## Running Backend Tests

### Prerequisites
```bash
cd voice
source venv/bin/activate  # or venv\Scripts\activate on Windows
# Note: pytest is optional - tests work without it!
# pip install pytest  # Only if you want to use pytest features
```

### Run Comprehensive Test Suite
```bash
# Make sure you're in the voice directory with venv activated
cd voice
source venv/bin/activate  # or venv\Scripts\activate on Windows
python3 tests/test_phases_1_3_comprehensive.py
```

**Note**: The test suite works without pytest installed. It will run in standalone mode.

### Run with pytest (if installed)
```bash
pytest tests/test_phases_1_3_comprehensive.py -v
```

### Run Specific Test Classes
```bash
# Test Phase 1 only
pytest tests/test_phases_1_3_comprehensive.py::TestPhase1BackendAPI -v

# Test Phase 3 only
pytest tests/test_phases_1_3_comprehensive.py::TestPhase3TranscriptionService -v
```

## Running Frontend Tests

### Prerequisites
```bash
cd frontend
npm install
```

### Start Development Server
```bash
npm run dev
```

### Open Test Pages

1. **Comprehensive Test Suite:**
   ```
   http://localhost:5173/test-phases-1-3.html
   ```
   - Tests all phases
   - Interactive UI
   - Real-time results
   - Test logging

2. **Phase 2 Specific Tests:**
   ```
   http://localhost:5173/test-phase2.html
   ```
   - Full audio recording tests
   - Transcription testing
   - Waveform visualization

## What Gets Tested

### Phase 1: Backend API Setup ✅
- [x] Root endpoint (`/`)
- [x] Health check endpoint (`/health`)
- [x] Config endpoint (`/config`)
- [x] CORS middleware configuration
- [x] API structure and responses

### Phase 2: Frontend Audio Recording ✅
- [x] AudioRecorder class instantiation
- [x] MediaRecorder API support detection
- [x] Microphone permission handling
- [x] Recording start/stop functionality
- [x] Audio validation
- [x] AudioVisualizer initialization
- [x] Waveform visualization

### Phase 3: Transcription Service ✅
- [x] API client connection
- [x] Transcription endpoint availability
- [x] File upload handling
- [x] Query parameter support
- [x] Response format handling
- [x] Timestamps inclusion
- [x] Confidence scores
- [x] Error handling

### Integration Tests ✅
- [x] End-to-end workflow
- [x] Full recording → transcription flow
- [x] Error handling across phases
- [x] Response format consistency

## Test Coverage

### Backend Tests
- **Unit Tests**: Individual functions and classes
- **Integration Tests**: API endpoints
- **Error Handling**: Various error scenarios
- **Configuration**: Config validation

### Frontend Tests
- **Component Tests**: AudioRecorder, AudioVisualizer
- **API Integration**: VoiceApiClient
- **Browser Compatibility**: MediaRecorder support
- **User Interaction**: Recording flow

## Expected Results

### Backend Tests
```
🧪 Comprehensive Test Suite for Phases 1-3
======================================================================

📋 Phase 1: Backend API Setup
----------------------------------------------------------------------
  ✅ Root endpoint
  ✅ Health check endpoint
  ✅ Config endpoint
  ✅ CORS headers

📋 Phase 2: Audio Processing Utilities
----------------------------------------------------------------------
  ✅ Audio utilities imports
  ✅ Audio file validation
  ✅ Audio info structure

📋 Phase 3: Transcription Service
----------------------------------------------------------------------
  ✅ Transcription service initialization
  ✅ Transcription service constants
  ✅ Audio file preparation logic
  ✅ Retry logic structure

📋 Phase 3: Enhanced API Endpoint
----------------------------------------------------------------------
  ✅ Transcribe endpoint exists
  ✅ Query parameters accepted
  ✅ All query parameters work

📋 Integration: Phases 1-3
----------------------------------------------------------------------
  ✅ Full workflow structure
  ✅ Error handling
  ✅ Response format structure

📋 Configuration Management
----------------------------------------------------------------------
  ✅ Config imports
  ✅ Config constants
  ✅ Config directories
  ✅ Config summary

======================================================================
✅ Test Suite Complete
======================================================================
```

### Frontend Tests
- Visual test results in browser
- Real-time status updates
- Test logging
- Summary statistics

## Troubleshooting

### Backend Tests Fail

**Issue**: Import errors
```bash
# Solution: Ensure you're in the virtual environment
cd voice
source venv/bin/activate
pip install -r requirements.txt
```

**Issue**: API key not configured
```bash
# Solution: Tests will skip API-dependent tests
# Add OPENAI_API_KEY to .env file for full testing
```

**Issue**: FastAPI not found
```bash
# Solution: Install dependencies
pip install fastapi uvicorn
```

**Issue**: pytest not found
```bash
# Solution: pytest is optional! The test suite works without it.
# Just run: python3 tests/test_phases_1_3_comprehensive.py
# If you want pytest for advanced features:
pip install pytest
```

### Frontend Tests Fail

**Issue**: Module not found
```bash
# Solution: Install dependencies
cd frontend
npm install
```

**Issue**: Backend not running
```bash
# Solution: Start backend first
cd ../voice
python main.py
```

**Issue**: CORS errors
```bash
# Solution: Ensure backend CORS is configured
# Check voice/main.py for CORS middleware
```

## Running Tests in CI/CD

### GitHub Actions Example
```yaml
name: Test Phases 1-3

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          cd voice
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd voice
          python tests/test_phases_1_3_comprehensive.py
```

## Manual Testing Checklist

### Phase 1: Backend API
- [ ] Start backend: `cd voice && python main.py`
- [ ] Visit: `http://localhost:8000/`
- [ ] Visit: `http://localhost:8000/health`
- [ ] Visit: `http://localhost:8000/config`
- [ ] Visit: `http://localhost:8000/docs`

### Phase 2: Frontend Recording
- [ ] Start frontend: `cd frontend && npm run dev`
- [ ] Open: `http://localhost:5173/test-phase2.html`
- [ ] Test recording functionality
- [ ] Test waveform visualization
- [ ] Test audio playback

### Phase 3: Transcription
- [ ] Ensure backend is running
- [ ] Ensure API key is configured
- [ ] Record audio in frontend
- [ ] Test transcription
- [ ] Verify timestamps
- [ ] Verify confidence scores

### Integration
- [ ] Record audio → Transcribe → Verify results
- [ ] Test error scenarios
- [ ] Test with different audio formats
- [ ] Test with large files (chunking)

## Next Steps

After running tests:

1. ✅ Review test results
2. ✅ Fix any failing tests
3. ✅ Verify all features work
4. ✅ Document any issues
5. ✅ Update tests if needed

---

**Happy Testing! 🧪**

