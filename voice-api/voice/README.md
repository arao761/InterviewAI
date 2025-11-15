# PrepWise Voice API - Phase 1 Setup

## Overview
Voice and transcription service for PrepWise interview preparation platform. This API provides speech-to-text (Whisper) and text-to-speech (TTS) capabilities for conducting AI-powered voice interviews.

## Setup Instructions

### 1. Environment Setup

```bash
cd voice
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Note:** If the virtual environment already exists, just activate it:
```bash
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### 2. Verify Python Version

Ensure you have Python 3.10 or higher:
```bash
python3 --version
```

### 3. Configure API Keys

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```
   OPENAI_API_KEY=your_actual_openai_key_here
   ELEVENLABS_API_KEY=your_actual_elevenlabs_key_here  # Optional
   ```

3. **Important:** Never commit the `.env` file to git (it's already in `.gitignore`)

### 4. Run the Server

```bash
python main.py
```

The server will start at: **http://localhost:8000**

- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **Root Endpoint:** http://localhost:8000/

### 5. Test the Setup

#### Test Whisper API (Speech-to-Text)
```bash
# First, add a sample audio file to tests/test_audio_samples/sample.mp3
python tests/test_whisper.py
```

#### Test TTS API (Text-to-Speech)
```bash
python tests/test_tts.py
```

## API Endpoints

### Health Check
```
GET /health
```
Returns API status and configuration validation.

### Root
```
GET /
```
Returns API information and available endpoints.

### Configuration
```
GET /config
```
Returns non-sensitive configuration information.

### Placeholder Endpoints (Phase 2)
- `POST /transcribe` - Transcribe audio to text (to be implemented)
- `POST /synthesize` - Convert text to speech (to be implemented)

## Project Structure

```
/voice
├── __init__.py
├── main.py                # FastAPI application
├── config.py              # Configuration and API keys
├── requirements.txt       # Python dependencies
├── .env.example          # Template for environment variables
├── .env                  # Actual API keys (gitignored)
├── utils/
│   ├── __init__.py
│   └── audio_utils.py    # Audio processing utilities
├── tests/
│   ├── __init__.py
│   ├── test_whisper.py   # Whisper API test
│   ├── test_tts.py       # TTS API test
│   └── test_audio_samples/
│       └── README.md     # Instructions for test files
└── README.md             # This file
```

## Tech Stack

- **Python 3.10+**
- **FastAPI** - Modern web framework for building APIs
- **OpenAI Whisper API** - Speech-to-Text transcription
- **OpenAI TTS API** - Text-to-Speech synthesis
- **pydub** - Audio file manipulation
- **librosa** - Audio analysis and processing
- **numpy** - Numerical computing

## Configuration

All configuration is managed through environment variables in the `.env` file:

- `OPENAI_API_KEY` - **Required** - Your OpenAI API key
- `ELEVENLABS_API_KEY` - **Optional** - ElevenLabs API key for alternative TTS
- `MAX_AUDIO_SIZE_MB` - Maximum audio file size (default: 25 MB)
- `MAX_DURATION_SECONDS` - Maximum audio duration (default: 600 seconds / 10 minutes)

Additional settings can be found in `config.py`.

## Testing

### Adding Test Audio Files

1. Place sample audio files in `tests/test_audio_samples/`
2. For Whisper testing, name the file `sample.mp3` (or update the test script)
3. Supported formats: MP3, WAV, M4A, OGG, WEBM

### Running Tests

```bash
# Test Whisper API
python tests/test_whisper.py

# Test TTS API
python tests/test_tts.py
```

## Troubleshooting

### API Key Not Found
- Ensure `.env` file exists in the `voice/` directory
- Verify `OPENAI_API_KEY` is set correctly
- Check for typos or extra spaces in the `.env` file

### Import Errors
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` to install dependencies
- Verify you're in the correct directory

### Server Won't Start
- Check if port 8000 is already in use
- Verify all dependencies are installed
- Check the console for error messages

### Audio File Issues
- Ensure audio file format is supported
- Check file size (must be < 25 MB)
- Verify file duration (must be < 10 minutes)

## Next Steps

### Phase 2: Frontend Audio Recording
- Implement audio recording from browser
- Add real-time audio streaming
- Create upload endpoints

### Phase 3: Transcription Service
- Complete `/transcribe` endpoint
- Add batch transcription support
- Implement transcription caching

### Phase 4: Speech Analysis
- Add speech quality metrics
- Implement sentiment analysis
- Create feedback system

## Development

### Running in Development Mode

The server runs with auto-reload enabled by default:
```bash
python main.py
```

Changes to Python files will automatically restart the server.

### API Documentation

FastAPI automatically generates interactive API documentation:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Security Notes

- **Never commit `.env` files** - They contain sensitive API keys
- Use environment variables for all secrets
- Configure CORS properly for production (currently allows all origins)
- Add rate limiting in production
- Use HTTPS in production

## License

Part of the PrepWise interview preparation platform.

## Support

For issues or questions, please refer to the project documentation or contact the development team.

