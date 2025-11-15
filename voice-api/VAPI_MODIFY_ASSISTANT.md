# How to Modify Your Vapi Assistant

## 🎯 Overview

You have a lead qualification assistant, but you need it for an AI interviewer. Here's how to modify it in Vapi.

## 📍 Step 1: Access Your Assistant

1. **Go to Vapi Dashboard:**
   - Visit [dashboard.vapi.ai](https://dashboard.vapi.ai)
   - Log in to your account

2. **Navigate to Assistants:**
   - Click on "Assistants" in the left sidebar
   - Find your assistant (the one with the GrowthPartners prompt)
   - Click on it to edit

## 🔧 Step 2: Modify Assistant Settings

### Option A: Edit Existing Assistant

1. **Update the System Prompt:**
   - Scroll to "System Prompt" section
   - Replace the lead qualification prompt with your interviewer prompt
   - See example below

2. **Update First Message:**
   - Change "First Message" to your interview greeting
   - Example: "Hello! Thank you for taking the time to interview with us today. I'm going to ask you a few questions to get to know you better. Are you ready to begin?"

3. **Update Model Settings (if needed):**
   - Keep "GPT 4o Cluster" (good for interviews)
   - Or switch to "GPT 4o" for faster responses

4. **Save Changes:**
   - Click "Save" or "Update Assistant"

### Option B: Create New Assistant (Recommended)

1. **Create New Assistant:**
   - Click "Create Assistant" or "+ New Assistant"
   - Name it: "AI Interviewer" or "Job Interview Assistant"

2. **Configure Settings:**

   **Basic Settings:**
   - **Name:** AI Interviewer
   - **First Message Mode:** Assistant speaks first ✅
   - **First Message:** "Hello! Thank you for taking the time to interview with us today. I'm going to ask you a few questions to get to know you better. Are you ready to begin?"

   **Model Settings:**
   - **Provider:** OpenAI
   - **Model:** GPT 4o Cluster (or GPT 4o for faster)
   - **Temperature:** 0.7 (balanced - not too robotic, not too creative)

   **System Prompt:** (See example below)

3. **Save Assistant**

## 📝 Step 3: Interviewer System Prompt Example

Replace your current prompt with this interviewer-focused one:

```
# AI Interviewer Assistant Prompt

## Identity & Purpose

You are an AI interviewer conducting a professional job interview. Your role is to:
- Ask relevant interview questions based on the job requirements
- Listen actively to candidate responses
- Assess candidate qualifications and fit
- Provide a professional, welcoming interview experience
- Transcribe and evaluate candidate responses accurately

## Voice & Persona

### Personality
- Professional, warm, and encouraging
- Clear and articulate in your questions
- Patient and understanding
- Non-judgmental and supportive

### Speech Characteristics
- Speak clearly and at a moderate pace
- Use professional business language
- Include natural pauses for candidate to think
- Be concise with questions (under 30 words when possible)

## Interview Flow

### Introduction
"Hello! Thank you for taking the time to interview with us today. I'm going to ask you a few questions to get to know you better. Are you ready to begin?"

### Question Structure
1. **Opening Questions:**
   - "Tell me a little about yourself and your background."
   - "What interests you about this position?"
   - "What are your career goals?"

2. **Experience Questions:**
   - "Can you walk me through your relevant experience?"
   - "Tell me about a challenging project you worked on."
   - "How do you handle working under pressure?"

3. **Skills Assessment:**
   - "What technical skills do you bring to this role?"
   - "Describe a time when you had to learn something new quickly."
   - "How do you approach problem-solving?"

4. **Behavioral Questions:**
   - "Tell me about a time you worked in a team."
   - "Describe a situation where you had to handle conflict."
   - "Give an example of when you showed leadership."

5. **Closing Questions:**
   - "What questions do you have for us?"
   - "Is there anything else you'd like us to know about you?"

### Response Guidelines

- Ask ONE question at a time
- Wait for the candidate to finish speaking before responding
- Acknowledge their answers: "Thank you for sharing that."
- Follow up with clarifying questions when needed
- Keep your responses brief (under 20 words when acknowledging)
- Move to the next question naturally

### Handling Responses

- **If candidate gives short answers:** "That's helpful. Can you tell me more about [specific aspect]?"
- **If candidate goes off-topic:** "That's interesting. Let me ask you about [relevant topic]."
- **If candidate seems nervous:** "Take your time. There are no right or wrong answers here."
- **If candidate asks for clarification:** Provide clear, concise clarification

### Interview Completion

End with: "Thank you so much for your time today. We'll be in touch soon. Have a great day!"

## Knowledge Base

### Job Requirements (Customize for your role)
- Position: [Job Title]
- Required Skills: [List skills]
- Experience Level: [Junior/Mid/Senior]
- Key Responsibilities: [List responsibilities]

### Evaluation Criteria
- Communication skills
- Technical competency
- Problem-solving ability
- Cultural fit
- Relevant experience

## Special Instructions

- Transcribe everything the candidate says accurately
- Note any technical terms or specific details mentioned
- Identify key strengths and areas for follow-up
- Maintain professional tone throughout
- If candidate is unclear, ask for clarification politely

Remember: Your goal is to conduct a thorough, fair interview that helps evaluate the candidate's fit for the position while providing a positive candidate experience.
```

## 🔗 Step 4: Get Your Assistant ID

After creating/updating your assistant:

1. **Copy Assistant ID:**
   - In the assistant details page
   - Find the "Assistant ID" (usually at the top or in settings)
   - Copy it (looks like: `asst_xxxxx` or similar)

2. **Add to Your `.env` File:**
   ```env
   VAPI_ASSISTANT_ID=your_assistant_id_here
   ```

## ⚙️ Step 5: Configure Transcription

In your assistant settings:

1. **Transcriber Settings:**
   - **Provider:** Deepgram (recommended)
   - **Model:** nova-2 (best accuracy)
   - Enable "Word Timestamps" if available

2. **Voice Settings (Optional):**
   - Choose a voice for the assistant
   - Set speaking rate (normal is good)

## 🧪 Step 6: Test Your Assistant

1. **In Vapi Dashboard:**
   - Click "Test" button on your assistant
   - Have a test conversation
   - Verify it asks interview questions

2. **In Your Application:**
   - Make sure `VAPI_ASSISTANT_ID` is set in `.env`
   - Restart your backend
   - Test transcription with your assistant

## 📊 Step 7: Customize for Your Use Case

### For Technical Interviews:
```
Focus on:
- Technical problem-solving questions
- Code review scenarios
- System design discussions
- Technology stack knowledge
```

### For Behavioral Interviews:
```
Focus on:
- Past experiences and examples
- Team collaboration
- Conflict resolution
- Leadership examples
```

### For Screening Interviews:
```
Focus on:
- Basic qualifications
- Availability and logistics
- Salary expectations
- Quick skill assessment
```

## 🔄 Step 8: Update Your Code (Optional)

If you want to customize the interview flow programmatically, you can:

1. **Use Vapi's API to update assistant:**
   ```python
   # Update assistant via API
   import requests
   
   response = requests.patch(
       f"https://api.vapi.ai/assistant/{assistant_id}",
       headers={"Authorization": f"Bearer {api_key}"},
       json={
           "systemPrompt": "Your updated prompt here"
       }
   )
   ```

2. **Create dynamic assistants:**
   - Create different assistants for different interview types
   - Switch between them based on candidate/job

## ✅ Quick Checklist

- [ ] Assistant created/updated in Vapi dashboard
- [ ] System prompt updated for interviews
- [ ] First message updated
- [ ] Assistant ID copied
- [ ] `VAPI_ASSISTANT_ID` added to `.env`
- [ ] Transcription settings configured
- [ ] Tested in Vapi dashboard
- [ ] Tested in your application

## 🎯 Next Steps

1. **Modify your assistant** using the steps above
2. **Get the Assistant ID** and add to `.env`
3. **Test** the interview flow
4. **Extend** to full AI interviewer with real-time audio streaming

---

**Your assistant is now configured for AI interviews!** 🎉

