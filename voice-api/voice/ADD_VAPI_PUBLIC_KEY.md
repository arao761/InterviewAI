# Add Vapi Public API Key

## Quick Setup

Add your Vapi PUBLIC API key to `.env` so the frontend can use it automatically:

```bash
cd voice
echo 'VAPI_PUBLIC_API_KEY=your_public_key_here' >> .env
```

## Get Your Public Key

1. Go to [dashboard.vapi.ai](https://dashboard.vapi.ai)
2. Navigate to "API Keys"
3. Copy your **PUBLIC** key (not private!)
4. Add to `.env` file

## After Adding

Restart your backend, and the frontend will automatically use it - no more prompts!

---

**That's it! The test page will start immediately now!** 🚀

