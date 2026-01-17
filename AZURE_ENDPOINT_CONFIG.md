# Azure Endpoint Configuration Guide

Based on your Azure setup, here's how to configure your `.env` file:

## Your Azure Endpoints

- **Azure OpenAI endpoint**: `https://theinterviewai.openai.azure.com/`
- **Speech to text endpoint**: `https://eastus.stt.speech.microsoft.com`
- **Text to speech endpoint**: `https://eastus.tts.speech.microsoft.com`
- **Azure AI Services endpoint**: `https://theinterviewai.cognitiveservices.azure.com/`

## Required Configuration

Add these to your `frontend/.env` file:

```bash
# Azure OpenAI / Microsoft Foundry Configuration
NEXT_PUBLIC_FOUNDRY_ENDPOINT=https://theinterviewai.openai.azure.com
NEXT_PUBLIC_FOUNDRY_API_KEY=your-azure-openai-api-key-here
NEXT_PUBLIC_AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name

# Azure Speech Services Configuration
# Option 1: Use region-based (recommended)
NEXT_PUBLIC_AZURE_SPEECH_KEY=your-speech-services-key-here
NEXT_PUBLIC_AZURE_SPEECH_REGION=eastus

# Option 2: Use custom endpoint (alternative)
# NEXT_PUBLIC_AZURE_SPEECH_KEY=your-speech-services-key-here
# NEXT_PUBLIC_AZURE_SPEECH_ENDPOINT=https://eastus.stt.speech.microsoft.com
```

## How to Get Your Credentials

### 1. Azure OpenAI API Key and Deployment Name

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Azure OpenAI resource (theinterviewai)
3. Go to "Keys and Endpoint" in the left menu
4. Copy **Key 1** (this is your `NEXT_PUBLIC_FOUNDRY_API_KEY`)
5. Go to "Deployments" in the left menu
6. Note the name of your deployment (this is your `NEXT_PUBLIC_AZURE_OPENAI_DEPLOYMENT_NAME`)
   - Common names: `gpt-4`, `gpt-35-turbo`, `gpt-4o`, etc.

### 2. Azure Speech Services Key

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Speech Services resource
3. Go to "Keys and Endpoint" in the left menu
4. Copy **Key 1** (this is your `NEXT_PUBLIC_AZURE_SPEECH_KEY`)
5. Copy the **Location/Region** (should be `eastus` based on your endpoints)

## Important Notes

1. **Deployment Name**: The Azure OpenAI endpoint requires a deployment name. Make sure you have a deployment created in your Azure OpenAI resource.

2. **Region**: Based on your endpoints, your region is `eastus`. Use this for `NEXT_PUBLIC_AZURE_SPEECH_REGION`.

3. **API Version**: The code uses `api-version=2024-02-15-preview` for Azure OpenAI. This should work with most deployments.

4. **Security**: These keys are exposed to the browser (NEXT_PUBLIC_ prefix). Make sure to:
   - Enable domain restrictions in Azure Portal
   - Use IP whitelisting for production
   - Monitor usage

## Testing

After configuring, restart your Next.js dev server:

```bash
cd frontend
pnpm dev
```

Then test the interview feature to verify the connection works.
