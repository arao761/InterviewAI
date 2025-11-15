# Quick Setup: Add Your Vapi API Key

## ⚠️ Security Note

**Never share your API key with anyone, including AI assistants!** 
- API keys are like passwords - keep them secret
- This guide shows you how to add it safely yourself

## 🚀 Quick Setup (3 Steps)

### Option 1: Using the Setup Script (Easiest)

```bash
cd voice
source venv/bin/activate
./QUICK_KEY_SETUP.sh
```

The script will:
1. Ask you to paste your private key (it won't show on screen)
2. Add it to `.env` file automatically
3. Set `TRANSCRIPTION_PROVIDER=vapi`

### Option 2: Manual Setup (Recommended)

1. **Get your PRIVATE API key:**
   - Go to [dashboard.vapi.ai](https://dashboard.vapi.ai)
   - Navigate to "API Keys" → Copy your **PRIVATE** key

2. **Open the `.env` file:**
   ```bash
   cd voice
   nano .env
   # OR use: code .env, open -e .env, etc.
   ```

3. **Add these lines:**
   ```env
   # Vapi API Configuration
   VAPI_API_KEY=paste_your_private_key_here
   TRANSCRIPTION_PROVIDER=vapi
   ```

4. **Save the file** (Ctrl+X, then Y, then Enter in nano)

5. **Verify it worked:**
   ```bash
   python3 -c "from config import Config; print('✅ Key loaded!' if Config.VAPI_API_KEY else '❌ Key not found')"
   ```

## ✅ Verify Setup

After adding your key, test it:

```bash
cd voice
source venv/bin/activate

# Check if key is loaded
python3 -c "from config import Config; print('Vapi key:', '✅ Loaded' if Config.VAPI_API_KEY and Config.VAPI_API_KEY != 'your_private_vapi_api_key_here' else '❌ Not configured'); print('Provider:', Config.TRANSCRIPTION_PROVIDER)"
```

Should output:
```
Vapi key: ✅ Loaded
Provider: vapi
```

## 🔒 Security Best Practices

- ✅ Add key to `.env` file (already in `.gitignore`)
- ✅ Use PRIVATE key (not public)
- ✅ Never commit `.env` to git
- ✅ Never share your key
- ✅ Rotate key if compromised

## 🐛 Troubleshooting

**"Key not found"**
- Check you saved the `.env` file
- Verify no quotes around the key
- Make sure no spaces around `=`

**"401 Unauthorized"**
- Verify you used the PRIVATE key (not public)
- Check for typos
- Make sure key hasn't been revoked

---

**You're all set! Your key is now configured securely!** 🔐

