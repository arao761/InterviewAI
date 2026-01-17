# How to Find or Create Your Azure OpenAI Deployment Name

## Option 1: Find Existing Deployment

If you already have a deployment:

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Azure OpenAI resource: **theinterviewai**
3. In the left menu, click **"Deployments"**
4. You'll see a list of deployments with their names
5. Common names: `gpt-4`, `gpt-35-turbo`, `gpt-4o`, `gpt-4-turbo`, etc.
6. Copy the name → this is your `NEXT_PUBLIC_AZURE_OPENAI_DEPLOYMENT_NAME`

## Option 2: Create a New Deployment

If you don't have a deployment:

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Azure OpenAI resource: **theinterviewai**
3. In the left menu, click **"Deployments"**
4. Click **"+ Create"** button
5. Fill in:
   - **Model**: Choose a model (e.g., `gpt-4`, `gpt-35-turbo`, `gpt-4o`)
   - **Deployment name**: Give it a name (e.g., `gpt-4`, `interview-ai`, `gpt-35-turbo`)
   - **Advanced options**: Leave defaults or adjust as needed
6. Click **"Create"**
7. Wait for deployment to complete (usually 1-2 minutes)
8. Once created, use the deployment name you chose

## Option 3: Use Foundry Endpoint Format (No Deployment Needed)

If you have a Microsoft Foundry endpoint (not Azure OpenAI), you can use that format instead:

1. Check if you have a Foundry project endpoint (different from Azure OpenAI)
2. If yes, use that endpoint format (no deployment name needed)
3. The endpoint would look like: `https://{foundry-project}.services.ai.azure.com/api/projects/{project-name}`

## Quick Test

After setting up, test the endpoint format:

**With deployment name:**
```
https://theinterviewai.openai.azure.com/openai/deployments/YOUR-DEPLOYMENT-NAME/chat/completions?api-version=2024-02-15-preview
```

**Without deployment name (Foundry format):**
```
https://YOUR-FOUNDRY-ENDPOINT/chat/completions?api-version=2024-02-15-preview
```

## Recommendation

Since your endpoint is `theinterviewai.openai.azure.com`, you should:
1. Check if you have existing deployments
2. If yes, use one of them
3. If no, create a new deployment (recommended: `gpt-4` or `gpt-35-turbo`)

The deployment name is just a label you give to a model instance - it can be anything you want!
