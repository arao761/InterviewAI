"""
Test Setup Script
Verify Phase 1 setup is working correctly
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_environment():
    """Test that environment variables are set"""
    print("=" * 60)
    print("PHASE 1: Testing Environment Configuration")
    print("=" * 60)

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("❌ OPENAI_API_KEY not set!")
        print("   Please create .env file and add your API key")
        print("   Copy .env.example to .env and fill in your key")
        return False

    print(f"✅ OPENAI_API_KEY is set (length: {len(api_key)})")

    model = os.getenv("DEFAULT_MODEL", "gpt-4")
    print(f"✅ Default model: {model}")

    temperature = os.getenv("TEMPERATURE", "0.0")
    print(f"✅ Temperature: {temperature}")

    return True


def test_imports():
    """Test that all required packages can be imported"""
    print("\n" + "=" * 60)
    print("Testing Package Imports")
    print("=" * 60)

    required_packages = [
        ("openai", "OpenAI"),
        ("anthropic", "Anthropic"),
        ("pydantic", "Pydantic"),
        ("dotenv", "python-dotenv"),
        ("tenacity", "Tenacity"),
    ]

    all_success = True

    for package_name, display_name in required_packages:
        try:
            __import__(package_name)
            print(f"✅ {display_name} installed")
        except ImportError:
            print(f"❌ {display_name} NOT installed")
            print(f"   Run: pip install {package_name}")
            all_success = False

    return all_success


def test_llm_client():
    """Test LLM client functionality"""
    print("\n" + "=" * 60)
    print("Testing LLM Client")
    print("=" * 60)

    try:
        from src.utils.llm_client import LLMClient

        print("✅ LLMClient imported successfully")

        # Initialize client
        client = LLMClient(provider="openai", model="gpt-4o-mini")
        print(f"✅ LLMClient initialized: {client}")

        # Test basic generation
        print("\n📡 Testing API connection with simple prompt...")
        response = client.generate(
            prompt="Say 'Hello from PrepWise AI!' in exactly those words.",
            temperature=0.0,
            max_tokens=50
        )
        print(f"✅ API Response: {response}")

        # Test JSON generation
        print("\n📡 Testing JSON generation...")
        json_response = client.generate_json(
            prompt="Return a JSON object with two fields: 'status' (set to 'success') and 'message' (set to 'PrepWise AI is ready')"
        )
        print(f"✅ JSON Response: {json_response}")

        assert json_response.get("status") == "success", "JSON parsing failed"
        print("✅ JSON parsing working correctly")

        # Test token counting
        text = "This is a test of the token counting functionality."
        token_count = client.count_tokens(text)
        print(f"✅ Token counting: '{text}' = ~{token_count} tokens")

        return True

    except ImportError as e:
        print(f"❌ Failed to import LLMClient: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing LLM client: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False


def test_schemas():
    """Test Pydantic schemas"""
    print("\n" + "=" * 60)
    print("Testing Pydantic Schemas")
    print("=" * 60)

    try:
        from src.resume_parser.schemas import (
            Contact, Education, Experience, Skills, ParsedResume
        )

        print("✅ All schemas imported successfully")

        # Test Contact
        contact = Contact(
            name="John Doe",
            email="john@example.com",
            phone="555-1234"
        )
        print(f"✅ Contact schema: {contact.name}")

        # Test Skills
        skills = Skills(
            technical=["Python", "JavaScript"],
            tools=["Git", "Docker"]
        )
        print(f"✅ Skills schema: {len(skills.technical)} technical skills")

        # Test ParsedResume
        resume = ParsedResume(
            contact=contact,
            skills=skills,
            total_years_experience=3.5
        )
        print(f"✅ ParsedResume schema: {resume.experience_level} level")
        print(f"✅ Resume summary: {resume.get_summary()}")

        return True

    except Exception as e:
        print(f"❌ Error testing schemas: {e}")
        return False


def test_validators():
    """Test validator functions"""
    print("\n" + "=" * 60)
    print("Testing Validators")
    print("=" * 60)

    try:
        from src.utils.validators import (
            validate_email,
            validate_url,
            sanitize_text,
            validate_score
        )

        print("✅ Validators imported successfully")

        # Test email validation
        assert validate_email("test@example.com") == True
        assert validate_email("invalid-email") == False
        print("✅ Email validation working")

        # Test URL validation
        assert validate_url("https://example.com") == True
        assert validate_url("not-a-url") == False
        print("✅ URL validation working")

        # Test text sanitization
        dirty_text = "  Too   much    space  "
        clean_text = sanitize_text(dirty_text)
        assert clean_text == "Too much space"
        print("✅ Text sanitization working")

        # Test score validation
        assert validate_score(75) == True
        assert validate_score(150) == False
        print("✅ Score validation working")

        return True

    except Exception as e:
        print(f"❌ Error testing validators: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("PrepWise AI - Phase 1 Setup Test")
    print("=" * 60 + "\n")

    results = []

    # Run all tests
    results.append(("Environment", test_environment()))
    results.append(("Package Imports", test_imports()))
    results.append(("Pydantic Schemas", test_schemas()))
    results.append(("Validators", test_validators()))
    results.append(("LLM Client", test_llm_client()))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")

    total_passed = sum(1 for _, success in results if success)
    total_tests = len(results)

    print(f"\nTotal: {total_passed}/{total_tests} tests passed")

    if total_passed == total_tests:
        print("\n🎉 All tests passed! Phase 1 setup is complete!")
        print("\nNext steps:")
        print("1. Start implementing Phase 2 (Resume Parser)")
        print("2. Add sample resumes to examples/sample_resumes/")
        print("3. Test with real resume data")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
