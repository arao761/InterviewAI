# Quick Setup: Vapi for AI Interviewer Transcription

## 🎯 Goal
Transcribe what the user is saying for your AI interviewer application.

## ✅ Recommended Solution: Use Deepgram

Vapi uses Deepgram for transcription. For best results, use Deepgram directly:

### Step 1: Get Deepgram API Key

1. Sign up at [deepgram.com](https://deepgram.com) (free tier available)
2. Get your API key from the dashboard
3. Add to `voice/.env`:

```env
# Deepgram (Vapi's transcription provider)
DEEPGRAM_API_KEY=your_deepgram_key_here
USE_DEEPGRAM_VIA_VAPI=true

# Vapi (still needed)
VAPI_API_KEY=your_vapi_key
TRANSCRIPTION_PROVIDER=vapi
```

### Step 2: Restart Backend

```bash
cd voice
source venv/bin/activate
python3 main.py
```

### Step 3: Test

- Record audio in frontend
- Transcribe
- Should work! ✅

## 🔄 Alternative: Use Vapi Calls (For Full Interviewer)

If you want to use Vapi's full AI interviewer features:

1. **Create Assistant in Vapi:**
   - Go to [dashboard.vapi.ai](https://dashboard.vapi.ai)
   - Create assistant for interviews
   - Copy Assistant ID

2. **Configure:**
   ```env
   VAPI_API_KEY=your_vapi_key
   VAPI_ASSISTANT_ID=your_assistant_id
   TRANSCRIPTION_PROVIDER=vapi
   ```

3. **Note:** This creates actual calls with your assistant (more complex, but enables full interviewer features)

## 📊 Comparison

| Feature | Deepgram Direct | Vapi Calls |
|---------|----------------|------------|
| Speed | ⚡ Fast | 🐢 Slower (creates call) |
| Cost | 💰 Lower | 💰💰 Higher |
| Setup | ✅ Simple | ⚙️ Complex |
| Transcription | ✅ Yes | ✅ Yes |
| AI Interviewer | ❌ No | ✅ Yes |
| Real-time | ✅ Yes | ✅ Yes |

## 🎯 Recommendation

**For now:** Use Deepgram (Option 1) to get transcription working quickly.

**Later:** Extend to Vapi calls when you need full AI interviewer features.

---

**Quick Start:** Add `DEEPGRAM_API_KEY` and `USE_DEEPGRAM_VIA_VAPI=true` to `.env`!

