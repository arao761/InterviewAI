# Vapi API Key Guide: Private vs Public

## Which Key Should You Use?

### ✅ **Use PRIVATE API Key** (For Backend)

For this backend service, you **must use your PRIVATE API key**.

**Why?**
- Backend runs on your server (secure environment)
- Private key has full access to Vapi API
- Never exposed to users or frontend code
- Stored securely in `.env` file on server

### ❌ **Do NOT Use Public Key** (For Frontend Only)

Public keys are only for:
- Client-side JavaScript applications
- Browser-based integrations
- When the key might be visible in frontend code

**Why not for backend?**
- Limited permissions
- Not designed for server-side use
- May not have access to all API features

## How to Get Your Private API Key

1. **Go to Vapi Dashboard:**
   - Visit [dashboard.vapi.ai](https://dashboard.vapi.ai)
   - Log in to your account

2. **Navigate to API Keys:**
   - Click on your account menu (top right)
   - Select "API Keys"

3. **Copy Private Key:**
   - Find the **Private Key** section
   - Click the "Copy" icon to copy it
   - ⚠️ **This is the one you need!**

## Configuration

Add to `voice/.env`:

```env
# Use your PRIVATE API key
VAPI_API_KEY=your_private_key_here
TRANSCRIPTION_PROVIDER=vapi
```

## Security Best Practices

### ✅ Do:
- ✅ Use private key in backend `.env` file
- ✅ Keep `.env` in `.gitignore` (never commit it)
- ✅ Restrict file permissions: `chmod 600 .env`
- ✅ Use environment variables in production
- ✅ Rotate keys if compromised

### ❌ Don't:
- ❌ Commit API keys to git
- ❌ Share keys in public repositories
- ❌ Expose keys in frontend code
- ❌ Use public key for backend
- ❌ Hardcode keys in source code

## Verification

After adding your private key, verify it works:

```bash
# Start backend
cd voice
source venv/bin/activate
python3 main.py

# Check health endpoint
curl http://localhost:8000/health

# Should show:
# {
#   "api_keys_configured": {
#     "vapi": true
#   },
#   "transcription_provider": "vapi"
# }
```

## Troubleshooting

**"Vapi API key not configured"**
- Make sure you're using the **PRIVATE** key (not public)
- Check the key is in `voice/.env` file
- Verify no extra spaces or quotes around the key

**"Vapi API error: 401 Unauthorized"**
- Verify you copied the **PRIVATE** key correctly
- Check for typos or extra characters
- Make sure the key hasn't been revoked

**"Vapi API error: 403 Forbidden"**
- Your private key might not have transcription permissions
- Check your Vapi account plan/limits
- Contact Vapi support if needed

## Summary

- **Backend (this project):** Use **PRIVATE** API key ✅
- **Frontend/client-side:** Use **PUBLIC** API key (if needed)
- **Security:** Never expose private keys!

---

**For this backend service, always use your PRIVATE Vapi API key!** 🔒

