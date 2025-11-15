# Setting Up Your OpenAI API Key

## Quick Setup

1. **Open the `.env` file** in the `voice/` directory:
   ```bash
   cd voice
   # Edit .env file
   ```

2. **Add your API key** in this format (no quotes, no spaces):
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

3. **Save the file**

4. **Restart the backend server** to load the new key

## File Location

The `.env` file should be located at:
```
voice/.env
```

## Format Requirements

✅ **Correct format:**
```
OPENAI_API_KEY=sk-proj-abc123xyz...
```

❌ **Wrong formats:**
```
OPENAI_API_KEY="sk-proj-abc123xyz..."  # No quotes
OPENAI_API_KEY = sk-proj-abc123xyz...  # No spaces around =
OPENAI_API_KEY= sk-proj-abc123xyz...   # No space after =
```

## Verify It's Working

After adding your key, test it:
```bash
cd voice
source venv/bin/activate
python -c "from config import Config; print('Key loaded:', 'YES' if Config.OPENAI_API_KEY else 'NO')"
```

Should output: `Key loaded: YES`

## Get Your API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Paste it into your `.env` file

## Security Note

⚠️ **Never commit the `.env` file to git!** It's already in `.gitignore` for your protection.

## Troubleshooting

### Key not loading?
- Check for typos in the variable name
- Ensure no quotes around the value
- Make sure there are no spaces around the `=`
- Restart the server after making changes

### Still not working?
- Check the `.env` file is in the `voice/` directory (not `voice-api/`)
- Verify the file is named exactly `.env` (not `.env.txt` or similar)
- Make sure you saved the file

