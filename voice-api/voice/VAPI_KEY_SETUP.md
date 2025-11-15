# How to Add Your Vapi Private API Key

## 📍 Location

Add your Vapi private API key to this file:
```
voice/.env
```

## 📝 Step-by-Step Instructions

### Step 1: Get Your Private API Key

1. Go to [dashboard.vapi.ai](https://dashboard.vapi.ai)
2. Log in to your account
3. Click on your account menu (top right)
4. Select "API Keys"
5. Find the **Private Key** section
6. Click the "Copy" icon to copy your private key

### Step 2: Open the `.env` File

The `.env` file is located at:
```
voice/.env
```

You can edit it with any text editor:
```bash
cd voice
nano .env        # Using nano
# OR
code .env        # Using VS Code
# OR
open -e .env     # Using TextEdit (Mac)
```

### Step 3: Add Your Vapi Key

Add these two lines to your `.env` file:

```env
# Vapi API Configuration (for transcription)
VAPI_API_KEY=your_private_vapi_api_key_here

# Transcription Provider: "vapi" or "whisper" (defaults to "vapi")
TRANSCRIPTION_PROVIDER=vapi
```

**Important:**
- Replace `your_private_vapi_api_key_here` with your actual private key
- No quotes around the key
- No spaces around the `=` sign
- Use your **PRIVATE** key (not the public one!)

### Step 4: Example `.env` File

Your complete `.env` file should look like this:

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-proj-...

# Vapi API Configuration (for transcription)
VAPI_API_KEY=your_actual_private_key_here

# Transcription Provider: "vapi" or "whisper"
TRANSCRIPTION_PROVIDER=vapi

# Optional: ElevenLabs API (for future use)
# ELEVENLABS_API_KEY=
```

### Step 5: Save and Restart

1. **Save the file**
2. **Restart your backend server** to load the new key:
   ```bash
   cd voice
   source venv/bin/activate
   python3 main.py
   ```

## ✅ Verify It's Working

After adding your key, test it:

```bash
cd voice
source venv/bin/activate
python3 -c "from config import Config; print('Vapi key loaded:', 'YES' if Config.VAPI_API_KEY else 'NO'); print('Provider:', Config.TRANSCRIPTION_PROVIDER)"
```

Should output:
```
Vapi key loaded: YES
Provider: vapi
```

Or check the health endpoint:
```bash
curl http://localhost:8000/health
```

Should show:
```json
{
  "api_keys_configured": {
    "vapi": true
  },
  "transcription_provider": "vapi"
}
```

## 🔒 Security Notes

- ✅ The `.env` file is already in `.gitignore` (won't be committed to git)
- ✅ Never share your private API key
- ✅ Never commit the `.env` file to version control
- ✅ Use your **PRIVATE** key (not public)

## 🐛 Troubleshooting

**"Vapi key loaded: NO"**
- Check you added `VAPI_API_KEY=` (not `VAPI_API_KEY =` with spaces)
- Verify no quotes around the key value
- Make sure you saved the file
- Restart the server

**"Vapi API error: 401 Unauthorized"**
- Verify you copied the **PRIVATE** key (not public)
- Check for typos or extra characters
- Make sure the key hasn't been revoked in Vapi dashboard

**"Transcription provider not set"**
- Add `TRANSCRIPTION_PROVIDER=vapi` to your `.env` file
- Default is "vapi" but it's good to be explicit

---

**That's it! Your Vapi key is now configured!** 🎉

