# Quick Test Guide - How to Test Phases 1-3

This guide shows you exactly how to run all the tests yourself.

## 🚀 Quick Start (2 minutes)

### Option 1: Backend Tests (Python)

1. **Open terminal and navigate to the voice directory:**
   ```bash
   cd voice
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```
   (On Windows: `venv\Scripts\activate`)

3. **Run the comprehensive test suite:**
   ```bash
   python3 tests/test_phases_1_3_comprehensive.py
   ```

4. **You should see:**
   ```
   ======================================================================
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
   
   ... (more tests)
   
   ======================================================================
   ✅ Test Suite Complete
   ======================================================================
   ```

### Option 2: Frontend Tests (Browser)

1. **Start the backend server** (in one terminal):
   ```bash
   cd voice
   source venv/bin/activate
   python3 main.py
   ```
   You should see: `🚀 Starting PrepWise Voice API...`

2. **Start the frontend dev server** (in another terminal):
   ```bash
   cd frontend
   npm install  # if you haven't already
   npm run dev
   ```
   You should see: `Local: http://localhost:5173/`

3. **Open your browser and go to:**
   ```
   http://localhost:5173/test-phases-1-3.html
   ```

4. **Click "Run All Tests"** button

5. **Watch the tests run in real-time!**

---

## 📋 Detailed Step-by-Step

### Backend Python Tests

#### Step 1: Navigate to the voice directory
```bash
cd /Users/mahajans/Claude-Hackathon/voice-api/voice
```

#### Step 2: Activate virtual environment
```bash
source venv/bin/activate
```
You should see `(venv)` in your terminal prompt.

#### Step 3: Run the tests
```bash
python3 tests/test_phases_1_3_comprehensive.py
```

#### What you'll see:
- ✅ Green checkmarks for passing tests
- ❌ Red X marks for failing tests
- ⚠️ Warnings for skipped tests (like when API key is missing)

#### Expected output:
All tests should pass! You'll see a summary at the end.

---

### Frontend Browser Tests

#### Step 1: Start Backend (Terminal 1)
```bash
cd /Users/mahajans/Claude-Hackathon/voice-api/voice
source venv/bin/activate
python3 main.py
```

**Keep this terminal open!** The server should be running on `http://localhost:8000`

#### Step 2: Start Frontend (Terminal 2)
```bash
cd /Users/mahajans/Claude-Hackathon/voice-api/frontend
npm run dev
```

**Keep this terminal open too!** The dev server should be running on `http://localhost:5173`

#### Step 3: Open Test Page
Open your browser and navigate to:
```
http://localhost:5173/test-phases-1-3.html
```

#### Step 4: Run Tests
1. Click the **"Run All Tests"** button
2. Watch the tests run in real-time
3. See results update as tests complete
4. Check the test log at the bottom for details

#### What you'll see:
- Test items that turn green when they pass
- Test items that turn red when they fail
- A summary showing total/passed/failed/pending tests
- A log showing all test activity

---

## 🎯 Testing Individual Phases

### Test Only Phase 1 (Backend API)
```bash
cd voice
source venv/bin/activate
python3 -c "
from tests.test_phases_1_3_comprehensive import TestPhase1BackendAPI
test = TestPhase1BackendAPI()
test.setup_method()
test.test_root_endpoint()
test.test_health_check()
test.test_config_endpoint()
print('✅ Phase 1 tests passed!')
"
```

### Test Only Phase 2 (Frontend)
In the browser test page, click **"Test Phase 2"** button.

### Test Only Phase 3 (Transcription)
In the browser test page, click **"Test Phase 3"** button.

---

## 🧪 Interactive Testing (Full Features)

For the most complete testing experience, use the Phase 2 test page:

1. **Start backend:**
   ```bash
   cd voice
   source venv/bin/activate
   python3 main.py
   ```

2. **Start frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open in browser:**
   ```
   http://localhost:5173/test-phase2.html
   ```

4. **Test features:**
   - Record audio with your microphone
   - See waveform visualization
   - Transcribe your recording
   - See timestamps and confidence scores
   - Test all Phase 2 and Phase 3 features interactively

---

## ✅ What Should Pass

### Backend Tests (21 tests total)
- ✅ Phase 1: Backend API Setup (4 tests)
- ✅ Phase 2: Audio Processing (3 tests)
- ✅ Phase 3: Transcription Service (4 tests)
- ✅ Phase 3: API Endpoint (3 tests)
- ✅ Integration Tests (3 tests)
- ✅ Configuration (4 tests)

### Frontend Tests
- ✅ All API endpoints accessible
- ✅ AudioRecorder class works
- ✅ MediaRecorder API supported
- ✅ Transcription features available

---

## 🔧 Troubleshooting

### "Module not found" errors
```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### "Backend not running" errors
```bash
# Start the backend first
cd voice
source venv/bin/activate
python3 main.py
```

### "Frontend not loading"
```bash
# Make sure frontend dependencies are installed
cd frontend
npm install

# Start the dev server
npm run dev
```

### "API key not configured"
- This is OK! Tests will skip API-dependent tests
- To test transcription, add `OPENAI_API_KEY` to `voice/.env` file

---

## 📊 Understanding Test Results

### Backend Test Output
- **✅** = Test passed
- **❌** = Test failed (check error message)
- **⚠️** = Test skipped (usually because API key is missing)

### Frontend Test Output
- **Green border** = Test passed
- **Red border** = Test failed
- **Gray border** = Test pending
- **Blue border** = Test running

---

## 🎉 Success!

If all tests pass, you're good to go! Your Phases 1-3 implementation is working correctly.

---

## 💡 Pro Tips

1. **Run tests after making changes** to ensure nothing broke
2. **Check the test log** for detailed information about what's being tested
3. **Use the interactive test page** (`test-phase2.html`) for hands-on testing
4. **Keep both servers running** when testing frontend features

---

**Happy Testing! 🧪**

