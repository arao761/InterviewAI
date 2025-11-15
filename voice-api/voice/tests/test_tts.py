#!/usr/bin/env python3
"""
Test script for Text-to-Speech API integration
Tests both OpenAI TTS and ElevenLabs TTS (optional)
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from openai import OpenAI
from config import Config
import os


def test_openai_tts():
    """
    Test OpenAI Text-to-Speech API
    """
    print("=" * 60)
    print("🔊 Testing OpenAI TTS API (Text-to-Speech)")
    print("=" * 60)

    # Check if API key is configured
    if not Config.OPENAI_API_KEY:
        print("❌ ERROR: OPENAI_API_KEY not set in .env file")
        print("Please add your OpenAI API key to the .env file:")
        print("   OPENAI_API_KEY=your_api_key_here")
        return False

    print(f"✅ API Key configured: {Config.OPENAI_API_KEY[:8]}...")

    # Create output directory if it doesn't exist
    output_dir = Path(__file__).parent / "test_audio_samples"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "tts_test_output.mp3"

    sample_text = (
        "Hello! This is a test of the text-to-speech system for PrepWise "
        "interview preparation. The system should produce clear, natural-sounding speech."
    )

    print(f"\n📝 Sample text: {sample_text[:50]}...")
    print(f"🎤 Voice: {Config.TTS_VOICE}")
    print(f"🤖 Model: {Config.TTS_MODEL}")

    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=Config.OPENAI_API_KEY)

        print(f"\n📤 Generating speech with OpenAI TTS API...")

        # Generate speech
        response = client.audio.speech.create(
            model=Config.TTS_MODEL,
            voice=Config.TTS_VOICE,
            input=sample_text,
            speed=Config.TTS_SPEED
        )

        # Save the audio file
        response.stream_to_file(str(output_path))

        print("\n✅ OpenAI TTS Test SUCCESSFUL!")
        print(f"📁 Audio saved to: {output_path}")
        print(f"💡 Play the file to verify quality")
        print(f"   File size: {output_path.stat().st_size / 1024:.2f} KB")

        return True

    except Exception as e:
        print(f"\n❌ OpenAI TTS Test FAILED")
        print(f"Error: {str(e)}")
        print("\nPossible issues:")
        print("• Invalid API key")
        print("• Network connection problem")
        print("• API rate limit exceeded")
        print("• Insufficient API credits")
        return False


def test_elevenlabs_tts():
    """
    Test ElevenLabs TTS API (optional)
    """
    print("\n" + "=" * 60)
    print("🔊 Testing ElevenLabs TTS API (Optional)")
    print("=" * 60)

    if not Config.ELEVENLABS_API_KEY:
        print("⚠️  ElevenLabs API key not configured - skipping test")
        print("To use ElevenLabs TTS, add ELEVENLABS_API_KEY to your .env file")
        return None

    print(f"✅ ElevenLabs API Key configured: {Config.ELEVENLABS_API_KEY[:8]}...")
    print("\n⚠️  ElevenLabs integration coming soon...")
    print("This feature will be implemented in a future phase.")
    print("For now, OpenAI TTS is the primary text-to-speech provider.")

    return None


def test_tts_voices():
    """
    Test different OpenAI TTS voices
    """
    print("\n" + "=" * 60)
    print("🎭 Testing Different OpenAI TTS Voices")
    print("=" * 60)

    if not Config.OPENAI_API_KEY:
        print("❌ API key not configured. Skipping voice test.")
        return False

    # Available OpenAI TTS voices
    voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    sample_text = "This is a test of different voice options."

    output_dir = Path(__file__).parent / "test_audio_samples"
    output_dir.mkdir(exist_ok=True)

    try:
        client = OpenAI(api_key=Config.OPENAI_API_KEY)

        print(f"\nGenerating samples for {len(voices)} voices...")
        for voice in voices:
            output_path = output_dir / f"tts_voice_{voice}.mp3"
            print(f"  • Generating {voice}...", end=" ")

            response = client.audio.speech.create(
                model=Config.TTS_MODEL,
                voice=voice,
                input=sample_text
            )

            response.stream_to_file(str(output_path))
            print(f"✅ Saved to {output_path.name}")

        print("\n✅ All voice samples generated successfully!")
        print("💡 Play the files to compare voice qualities")

        return True

    except Exception as e:
        print(f"❌ Voice test failed: {str(e)}")
        return False


if __name__ == "__main__":
    print("\n🚀 Starting TTS API Tests\n")

    # Run OpenAI TTS test
    result1 = test_openai_tts()

    # Run ElevenLabs test (optional)
    result2 = test_elevenlabs_tts()

    # Run voice comparison test if basic test passed
    if result1:
        print("\n" + "=" * 60)
        response = input("Generate samples for all available voices? (y/n): ")
        if response.lower() == 'y':
            test_tts_voices()

    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    if result1:
        print("✅ OpenAI TTS test: PASSED")
    else:
        print("❌ OpenAI TTS test: FAILED")

    if result2 is None:
        print("⚠️  ElevenLabs TTS test: SKIPPED (not configured)")

    print("\n💡 Next steps:")
    print("   • Review the generated audio files")
    print("   • Test different voices and models")
    print("   • Integrate TTS into your application")
    print("=" * 60 + "\n")

