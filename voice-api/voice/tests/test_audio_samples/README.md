# Test Audio Samples Directory

This directory is for storing sample audio files used for testing the Whisper API and other audio processing features.

## Usage

1. **For Whisper API Testing:**
   - Add a sample audio file (MP3, WAV, M4A, OGG, or WEBM format)
   - Name it `sample.mp3` (or update the test script to use your filename)
   - Run `python tests/test_whisper.py` to test transcription

2. **For TTS Testing:**
   - TTS test output files will be saved here automatically
   - Files are named `tts_test_output.mp3` and `tts_voice_*.mp3`

## Getting Sample Audio Files

You can get sample audio files from:
- Record your own voice using a microphone
- Download from [freesound.org](https://freesound.org/) (free, requires account)
- Use any audio file you have (must be in supported format)

## Supported Formats

- MP3
- WAV
- M4A
- OGG
- WEBM

## File Size Limits

- Maximum file size: 25 MB (configurable in config.py)
- Maximum duration: 10 minutes (600 seconds)

## Note

Audio files in this directory are ignored by git (see .gitignore) to avoid committing large files. Only the README.md file is tracked.

