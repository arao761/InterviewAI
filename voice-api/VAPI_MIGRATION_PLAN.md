# Migration Plan: Whisper to Vapi

## Overview

This document outlines the plan to migrate from OpenAI Whisper to Vapi while maintaining all Phases 1-3 functionality.

## Strategy: Adapter Pattern

We'll create a Vapi-based transcription service that:
1. **Maintains the same interface** as the current TranscriptionService
2. **Keeps all Phase 1-3 code working** without changes
3. **Adds Vapi as an alternative provider** (can support both)

## Implementation Approach

### Option 1: Replace Whisper with Vapi (Recommended)
- Create new `VapiTranscriptionService` class
- Update `TranscriptionService` to use Vapi instead of Whisper
- Maintain exact same method signatures and return formats

### Option 2: Support Both Providers
- Create provider abstraction layer
- Allow switching between Whisper and Vapi via config
- More complex but provides flexibility

## What Needs to Change

### Files to Modify:
1. `voice/utils/transcription_service.py` - Replace Whisper calls with Vapi
2. `voice/config.py` - Add Vapi API key configuration
3. `voice/requirements.txt` - Add Vapi SDK (if available) or use REST API
4. `voice/main.py` - No changes needed (uses TranscriptionService interface)

### Files That Stay the Same:
- All Phase 1 code (backend API setup)
- All Phase 2 code (frontend recording)
- All Phase 3 API endpoints (same interface)
- All tests (same interface)

## Vapi Integration Points

### What We Need from Vapi:
1. **Transcription endpoint** - Convert audio to text
2. **Timestamps** - Word-level and segment-level
3. **Confidence scores** - Per-word confidence
4. **Language support** - Multi-language transcription
5. **File format support** - webm, mp3, wav, etc.

## Next Steps

1. Research Vapi API documentation
2. Get Vapi API key and credentials
3. Implement Vapi transcription service
4. Test with existing Phase 1-3 code
5. Update configuration

