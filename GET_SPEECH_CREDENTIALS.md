# How to Get Azure Speech Services Credentials

Since you already have the Speech endpoints, you likely have a Speech Services resource. Here's how to get your credentials:

## Step-by-Step Instructions

1. **Go to Azure Portal**: https://portal.azure.com

2. **Find Your Speech Services Resource**:
   - In the search bar at the top, type "Speech" or "Cognitive Services"
   - Look for a resource that matches your endpoints (eastus region)
   - Or go to "All resources" and filter by "Speech Services"

3. **Get Your Key**:
   - Click on your Speech Services resource
   - In the left menu, click on **"Keys and Endpoint"**
   - You'll see:
     - **Key 1** (copy this - this is your `NEXT_PUBLIC_AZURE_SPEECH_KEY`)
     - **Key 2** (backup, can use either)
     - **Location/Region** (should be `eastus` - this is your `NEXT_PUBLIC_AZURE_SPEECH_REGION`)

4. **Update Your .env File**:
   ```bash
   NEXT_PUBLIC_AZURE_SPEECH_KEY=paste-your-key-1-here
   NEXT_PUBLIC_AZURE_SPEECH_REGION=eastus
   ```

## Quick Checklist

- [ ] Found Speech Services resource in Azure Portal
- [ ] Copied Key 1 from "Keys and Endpoint"
- [ ] Confirmed region is `eastus`
- [ ] Updated `frontend/.env` with the key and region
- [ ] Restarted Next.js dev server

## If You Don't Have a Speech Services Resource

If you can't find a Speech resource, you need to create one:

1. In Azure Portal, click **"Create a resource"**
2. Search for **"Speech"**
3. Select **"Speech Services"**
4. Click **"Create"**
5. Fill in:
   - **Subscription**: Your subscription
   - **Resource Group**: Create new or use existing
   - **Region**: `East US` (to match your endpoints)
   - **Name**: e.g., "InterviewAI-Speech"
   - **Pricing Tier**: `Free F0` (for testing) or `Standard S0` (for production)
6. Click **"Review + create"**, then **"Create"**
7. Once created, go to "Keys and Endpoint" to get your credentials

## Free Tier Limits

- **Free F0**: 5 hours of speech-to-text per month, 5 hours of text-to-speech per month
- Good for testing and development

## After Adding Credentials

1. Save your `.env` file
2. Restart your Next.js dev server:
   ```bash
   cd frontend
   pnpm dev
   ```
3. Test the voice interview feature

## Troubleshooting

- **"Key not found"**: Make sure you copied the entire key (no spaces, all characters)
- **"Region mismatch"**: Make sure you're using `eastus` (lowercase, no spaces)
- **"Resource not found"**: You may need to create a new Speech Services resource
