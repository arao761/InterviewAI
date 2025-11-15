#!/usr/bin/env python3
"""
Test script for OpenAI Whisper API integration
Tests speech-to-text transcription functionality
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from openai import OpenAI
from config import Config
import os


def test_whisper_transcription():
    """
    Test OpenAI Whisper API with a sample audio file
    """
    print("=" * 60)
    print("🎤 Testing OpenAI Whisper API (Speech-to-Text)")
    print("=" * 60)

    # Check if API key is configured
    if not Config.OPENAI_API_KEY:
        print("❌ ERROR: OPENAI_API_KEY not set in .env file")
        print("Please add your OpenAI API key to the .env file:")
        print("   OPENAI_API_KEY=your_api_key_here")
        return False

    print(f"✅ API Key configured: {Config.OPENAI_API_KEY[:8]}...")

    # Check for sample audio file
    sample_audio_path = Path(__file__).parent / "test_audio_samples" / "sample.mp3"

    if not sample_audio_path.exists():
        print("\n⚠️  Sample audio file not found")
        print(f"Expected location: {sample_audio_path}")
        print("\nTo test Whisper API:")
        print("1. Add a sample audio file (MP3, WAV, M4A, etc.) to:")
        print(f"   {sample_audio_path.parent}/")
        print("2. Name it 'sample.mp3' (or update this script)")
        print("3. Run this test again")
        print("\nAlternatively, you can record a short audio clip or download")
        print("a sample from: https://freesound.org/")
        return None

    print(f"✅ Sample audio found: {sample_audio_path.name}")

    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=Config.OPENAI_API_KEY)

        print(f"\n📤 Uploading audio file to Whisper API...")
        print(f"   Model: {Config.WHISPER_MODEL}")
        print(f"   Format: {Config.WHISPER_RESPONSE_FORMAT}")

        # Transcribe audio
        with open(sample_audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model=Config.WHISPER_MODEL,
                file=audio_file,
                response_format=Config.WHISPER_RESPONSE_FORMAT
            )

        print("\n✅ Whisper API Test SUCCESSFUL!")
        print("\n" + "=" * 60)
        print("📝 TRANSCRIPTION RESULT:")
        print("=" * 60)
        print(transcript)
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n❌ Whisper API Test FAILED")
        print(f"Error: {str(e)}")
        print("\nPossible issues:")
        print("• Invalid API key")
        print("• Audio file format not supported")
        print("• Network connection problem")
        print("• API rate limit exceeded")
        return False


def test_whisper_with_options():
    """
    Test Whisper API with different response formats
    """
    print("\n" + "=" * 60)
    print("🎤 Testing Whisper API with different options")
    print("=" * 60)

    sample_audio_path = Path(__file__).parent / "test_audio_samples" / "sample.mp3"

    if not sample_audio_path.exists():
        print("⚠️  Sample audio file not found. Skipping options test.")
        return None

    if not Config.OPENAI_API_KEY:
        print("❌ API key not configured. Skipping options test.")
        return False

    try:
        client = OpenAI(api_key=Config.OPENAI_API_KEY)

        # Test with verbose JSON format
        print("\n📤 Testing with verbose_json format...")
        with open(sample_audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model=Config.WHISPER_MODEL,
                file=audio_file,
                response_format="verbose_json"
            )

        print("✅ Verbose JSON response received:")
        print(f"   Language: {transcript.language}")
        print(f"   Duration: {transcript.duration}s")
        print(f"   Text: {transcript.text[:100]}...")

        return True

    except Exception as e:
        print(f"❌ Options test failed: {str(e)}")
        return False


if __name__ == "__main__":
    print("\n🚀 Starting Whisper API Tests\n")

    # Run basic test
    result1 = test_whisper_transcription()

    # Run options test if basic test passed
    if result1:
        result2 = test_whisper_with_options()

    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    if result1:
        print("✅ Basic Whisper API test: PASSED")
    elif result1 is None:
        print("⚠️  Basic Whisper API test: SKIPPED (no sample audio)")
    else:
        print("❌ Basic Whisper API test: FAILED")

    print("\n💡 Next steps:")
    print("   • Add sample audio files to test_audio_samples/")
    print("   • Configure your OpenAI API key in .env")
    print("   • Run the tests again to verify the integration")
    print("=" * 60 + "\n")
