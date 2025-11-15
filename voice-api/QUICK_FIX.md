# Quick Fix: Add Your OpenAI API Key

## Step 1: Navigate to the voice directory

From your current location, run:
```bash
cd /Users/mahajans/Claude-Hackathon/voice-api/voice
```

Or from the project root:
```bash
cd voice
```

## Step 2: Edit the .env file

Open the `.env` file in your editor:
```bash
# Using nano (simple text editor)
nano .env

# Or using vim
vim .env

# Or open in your IDE/editor
code .env  # VS Code
```

## Step 3: Add your API key

Find this line:
```
OPENAI_API_KEY=
```

Change it to (replace with your actual key):
```
OPENAI_API_KEY=sk-your-actual-key-here
```

**Important:**
- No quotes around the key
- No spaces around the `=`
- The key should start with `sk-`
- Save the file

## Step 4: Verify it worked

```bash
cd /Users/mahajans/Claude-Hackathon/voice-api/voice
source venv/bin/activate
python -c "from config import Config; print('✅ Working!' if Config.OPENAI_API_KEY else '❌ Not found')"
```

## Step 5: Start the backend

```bash
python main.py
```

You should see:
```
✅ Configuration validated successfully
🚀 Starting PrepWise Voice API...
📍 Server will be available at: http://localhost:8000
```

## Get Your API Key

If you don't have one:
1. Go to https://platform.openai.com/api-keys
2. Sign in
3. Click "Create new secret key"
4. Copy it (starts with `sk-`)
5. Paste into `.env` file

## File Location

Full path:
```
/Users/mahajans/Claude-Hackathon/voice-api/voice/.env
```

