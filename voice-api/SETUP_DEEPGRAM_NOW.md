# Quick Fix: Set Up Deepgram for Transcription

## 🎯 The Problem

Vapi doesn't have a direct transcription endpoint. You need to use **Deepgram** (which Vapi uses internally) for transcription.

## ✅ Quick Solution (2 Steps)

### Step 1: Get Deepgram API Key

1. **Sign up for Deepgram:**
   - Go to [deepgram.com](https://deepgram.com)
   - Click "Sign Up" (free tier available)
   - Create an account

2. **Get Your API Key:**
   - After signing up, go to your dashboard
   - Navigate to "API Keys" section
   - Click "Create API Key"
   - Copy the key (starts with something like `xxxxx`)

### Step 2: Add to `.env` File

Open `voice/.env` and add these two lines:

```env
# Deepgram API (for transcription via Vapi)
DEEPGRAM_API_KEY=your_deepgram_api_key_here
USE_DEEPGRAM_VIA_VAPI=true
```

**Important:**
- Replace `your_deepgram_api_key_here` with your actual key
- No quotes around the key
- No spaces around the `=` sign

### Step 3: Restart Backend

```bash
# Stop current server (Ctrl+C)
# Then restart:
cd voice
source venv/bin/activate
python3 main.py
```

## 🧪 Test It

1. **Record audio** in frontend
2. **Click "Transcribe Recording"**
3. **Should work now!** ✅

## 📋 Complete `.env` Example

Your `voice/.env` should look like:

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-proj-...

# Vapi API Configuration
VAPI_API_KEY=your_vapi_key
TRANSCRIPTION_PROVIDER=vapi

# Deepgram API (for transcription)
DEEPGRAM_API_KEY=your_deepgram_key_here
USE_DEEPGRAM_VIA_VAPI=true

# Optional: Vapi Assistant (for full AI interviewer)
# VAPI_ASSISTANT_ID=your_assistant_id
```

## 🎯 Why Deepgram?

- ✅ Vapi uses Deepgram internally for transcription
- ✅ Direct access = faster transcription
- ✅ Lower cost for transcription-only
- ✅ Same quality Vapi uses
- ✅ Free tier available

## ✅ Verify Setup

After adding the key, verify:

```bash
cd voice
source venv/bin/activate
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()

deepgram_key = os.getenv('DEEPGRAM_API_KEY')
use_deepgram = os.getenv('USE_DEEPGRAM_VIA_VAPI', 'false').lower() == 'true'

print('Deepgram Key:', '✅ Set' if deepgram_key else '❌ Missing')
print('Use Deepgram:', '✅ Enabled' if use_deepgram else '❌ Disabled')
"
```

Should output:
```
Deepgram Key: ✅ Set
Use Deepgram: ✅ Enabled
```

## 🐛 Troubleshooting

**"Deepgram API error: 401"**
- Check your API key is correct
- Make sure no extra spaces or quotes

**"Deepgram API error: 403"**
- Check your Deepgram account has credits
- Verify API key has transcription permissions

**Still getting 404?**
- Make sure `USE_DEEPGRAM_VIA_VAPI=true` (not `false`)
- Restart backend after adding key
- Check `.env` file is in `voice/` directory

---

**That's it! Add your Deepgram key and transcription will work!** 🚀

