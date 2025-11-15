# Verify Your API Key is Saved

## Quick Check

Run this command to see if your API key is actually in the file:

```bash
cd /Users/mahajans/Claude-Hackathon/voice-api/voice
cat .env | grep OPENAI_API_KEY
```

**Expected output if key is there:**
```
OPENAI_API_KEY=sk-proj-abc123xyz...
```

**If you see this (key is missing):**
```
OPENAI_API_KEY=
```

Then the key wasn't saved properly.

## How to Add It Properly

1. **Open the file:**
   ```bash
   cd /Users/mahajans/Claude-Hackathon/voice-api/voice
   nano .env
   # or use your preferred editor
   ```

2. **Find this line:**
   ```
   OPENAI_API_KEY=
   ```

3. **Add your key AFTER the = sign (no spaces):**
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

4. **Save the file:**
   - In nano: Press `Ctrl+X`, then `Y`, then `Enter`
   - In other editors: Use Save (Cmd+S or Ctrl+S)

5. **Verify it saved:**
   ```bash
   cat .env | grep OPENAI_API_KEY
   ```
   
   You should see your key (not just `OPENAI_API_KEY=`)

6. **Test it loads:**
   ```bash
   source venv/bin/activate
   python -c "from config import Config; print('✅ Key loaded!' if Config.OPENAI_API_KEY else '❌ Not found')"
   ```

## Common Issues

- **Didn't save:** Make sure you actually saved the file after editing
- **Wrong file:** Make sure you're editing `/Users/mahajans/Claude-Hackathon/voice-api/voice/.env`
- **Spaces/quotes:** Don't add spaces or quotes around the key
- **Hidden characters:** Make sure there are no extra spaces before or after the key

## File Location

The exact file path is:
```
/Users/mahajans/Claude-Hackathon/voice-api/voice/.env
```

