# Vapi Web SDK Setup for Web-Based Interviews

## 🎯 Overview

For web-based interviews (browser-to-browser), use **Vapi's Web SDK** directly in the frontend. This is the recommended approach for web calls.

## ✅ What You Need

1. **Vapi PUBLIC API Key** (not private!)
   - Go to [dashboard.vapi.ai](https://dashboard.vapi.ai)
   - Get your **PUBLIC** API key (different from private key)
   - Public key is safe to use in frontend code

2. **Assistant ID**
   - Your assistant ID: `143899d5-4754-4cec-bf65-0743d3962ce1`

## 📦 Installation

### Option 1: CDN (Easiest - Already in test page)

The test page uses CDN, no installation needed!

### Option 2: NPM (For production)

```bash
cd frontend
npm install @vapi-ai/web
```

## 🚀 Quick Start

### Step 1: Get Your Public API Key

1. Go to [dashboard.vapi.ai](https://dashboard.vapi.ai)
2. Navigate to API Keys
3. Copy your **PUBLIC** key (not private!)

### Step 2: Update Test Page

The test page will prompt you for the key, or you can hardcode it:

```javascript
const vapiPublicKey = 'your-public-key-here';
```

### Step 3: Test

1. Start backend (optional - only needed for getting assistant ID)
2. Open: `http://localhost:5173/test-vapi-realtime.html`
3. Enter your PUBLIC API key when prompted
4. Click "Start Interview"
5. Speak - transcripts appear in real-time!

## 📝 How It Works

1. **Frontend** uses Vapi Web SDK directly
2. **No backend needed** for web calls (SDK handles everything)
3. **Real-time streaming** via WebRTC/WebSocket
4. **Transcripts** appear as you speak

## 🔧 Code Example

```javascript
import Vapi from '@vapi-ai/web';

const vapi = new Vapi('your-public-key');

// Start call with assistant
await vapi.start('your-assistant-id');

// Listen for transcripts
vapi.on('user-speech-end', (event) => {
  console.log('User said:', event.transcript);
});

// Stop call
await vapi.stop();
```

## 🎯 Benefits

- ✅ No phone number needed
- ✅ Works directly in browser
- ✅ Real-time streaming
- ✅ No backend required
- ✅ Simple setup

## 📋 Test Checklist

- [ ] Get Vapi PUBLIC API key
- [ ] Open test page
- [ ] Enter public key
- [ ] Click "Start Interview"
- [ ] Grant microphone permission
- [ ] Speak and see transcripts
- [ ] Assistant responds (if configured)

---

**Web-based interviews are ready! Just use Vapi's Web SDK!** 🎉

