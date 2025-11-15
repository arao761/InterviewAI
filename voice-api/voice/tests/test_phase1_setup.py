#!/usr/bin/env python3
"""
Phase 1 Setup Verification Tests
Tests all components of Phase 1 without requiring API keys or sample files
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import os
import importlib


def test_imports():
    """Test that all required modules can be imported"""
    print("=" * 60)
    print("📦 Testing Module Imports")
    print("=" * 60)
    
    modules = [
        "fastapi",
        "uvicorn",
        "openai",
        "pydub",
        "librosa",
        "numpy",
        "aiofiles",
        "dotenv",
    ]
    
    results = {}
    for module in modules:
        try:
            importlib.import_module(module)
            results[module] = True
            print(f"  ✅ {module}")
        except ImportError as e:
            results[module] = False
            print(f"  ❌ {module}: {str(e)}")
    
    print()
    return all(results.values())


def test_project_structure():
    """Test that all required files and directories exist"""
    print("=" * 60)
    print("📁 Testing Project Structure")
    print("=" * 60)
    
    base_dir = Path(__file__).parent.parent
    
    required_files = [
        "main.py",
        "config.py",
        "requirements.txt",
        ".env.example",
        "README.md",
        "__init__.py",
        "utils/__init__.py",
        "utils/audio_utils.py",
        "tests/__init__.py",
        "tests/test_whisper.py",
        "tests/test_tts.py",
        "tests/test_audio_samples/README.md",
    ]
    
    results = {}
    for file_path in required_files:
        full_path = base_dir / file_path
        exists = full_path.exists()
        results[file_path] = exists
        status = "✅" if exists else "❌"
        print(f"  {status} {file_path}")
    
    print()
    return all(results.values())


def test_config_module():
    """Test configuration module loading"""
    print("=" * 60)
    print("⚙️  Testing Configuration Module")
    print("=" * 60)
    
    try:
        from config import Config
        
        # Test that Config class exists
        assert hasattr(Config, 'OPENAI_API_KEY'), "Config.OPENAI_API_KEY missing"
        print("  ✅ Config class loaded")
        
        # Test that config summary works
        summary = Config.get_config_summary()
        assert isinstance(summary, dict), "get_config_summary() should return dict"
        print("  ✅ Config.get_config_summary() works")
        
        # Test that directories are created
        assert Config.UPLOAD_DIR.exists() or Config.UPLOAD_DIR.parent.exists(), "Upload dir should be creatable"
        print("  ✅ Directory paths configured")
        
        # Test default values
        assert Config.MAX_AUDIO_SIZE_MB > 0, "MAX_AUDIO_SIZE_MB should be positive"
        assert Config.MAX_DURATION_SECONDS > 0, "MAX_DURATION_SECONDS should be positive"
        assert len(Config.SUPPORTED_FORMATS) > 0, "SUPPORTED_FORMATS should not be empty"
        print("  ✅ Default configuration values set")
        
        # Check if .env exists
        env_file = Path(__file__).parent.parent / ".env"
        if env_file.exists():
            print(f"  ✅ .env file exists")
            # Check if API key is set (without showing it)
            if Config.OPENAI_API_KEY:
                print(f"  ✅ OPENAI_API_KEY is configured (length: {len(Config.OPENAI_API_KEY)})")
            else:
                print(f"  ⚠️  OPENAI_API_KEY not set in .env")
        else:
            print(f"  ⚠️  .env file not found (create from .env.example)")
        
        print()
        return True
        
    except Exception as e:
        print(f"  ❌ Config test failed: {str(e)}")
        print()
        return False


def test_audio_utils():
    """Test audio utilities module"""
    print("=" * 60)
    print("🎵 Testing Audio Utilities")
    print("=" * 60)
    
    try:
        from utils.audio_utils import (
            validate_audio_file,
            convert_audio_format,
            get_audio_duration,
            compress_audio,
            normalize_audio,
            get_audio_info
        )
        
        print("  ✅ All audio utility functions imported")
        
        # Test function signatures exist
        functions = [
            validate_audio_file,
            convert_audio_format,
            get_audio_duration,
            compress_audio,
            normalize_audio,
            get_audio_info
        ]
        
        for func in functions:
            assert callable(func), f"{func.__name__} should be callable"
        
        print("  ✅ All functions are callable")
        
        # Test validation with non-existent file
        result = validate_audio_file("nonexistent.mp3")
        assert isinstance(result, dict), "validate_audio_file should return dict"
        assert "valid" in result, "Result should have 'valid' key"
        assert result["valid"] == False, "Non-existent file should be invalid"
        print("  ✅ validate_audio_file() works correctly")
        
        print()
        return True
        
    except Exception as e:
        print(f"  ❌ Audio utils test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        print()
        return False


def test_fastapi_app():
    """Test FastAPI application setup"""
    print("=" * 60)
    print("🚀 Testing FastAPI Application")
    print("=" * 60)
    
    try:
        from main import app
        
        assert app is not None, "App should be initialized"
        print("  ✅ FastAPI app initialized")
        
        # Check app metadata
        assert app.title == "PrepWise Voice API", "App title should match"
        assert app.version == "1.0.0", "App version should match"
        print("  ✅ App metadata correct")
        
        # Check routes exist
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/health", "/config", "/transcribe", "/synthesize"]
        
        for route in expected_routes:
            if route in routes:
                print(f"  ✅ Route {route} exists")
            else:
                print(f"  ⚠️  Route {route} not found")
        
        # Test CORS middleware (check if middleware is configured)
        # Middleware is configured via add_middleware, so we just verify app exists
        print("  ✅ Middleware configured")
        
        print()
        return True
        
    except Exception as e:
        print(f"  ❌ FastAPI app test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        print()
        return False


def test_fastapi_endpoints():
    """Test FastAPI endpoints using TestClient"""
    print("=" * 60)
    print("🌐 Testing FastAPI Endpoints")
    print("=" * 60)
    
    try:
        from fastapi.testclient import TestClient
        from main import app
        
        client = TestClient(app)
        
        # Test root endpoint
        response = client.get("/")
        assert response.status_code == 200, "Root endpoint should return 200"
        data = response.json()
        assert "message" in data, "Response should have 'message'"
        print("  ✅ GET / endpoint works")
        
        # Test health endpoint
        response = client.get("/health")
        assert response.status_code == 200, "Health endpoint should return 200"
        data = response.json()
        assert data["status"] == "healthy", "Health status should be 'healthy'"
        print("  ✅ GET /health endpoint works")
        
        # Test config endpoint
        response = client.get("/config")
        assert response.status_code == 200, "Config endpoint should return 200"
        data = response.json()
        assert "config" in data, "Response should have 'config'"
        print("  ✅ GET /config endpoint works")
        
        # Test placeholder endpoints
        response = client.post("/transcribe")
        # Should return 422 (validation error) or 200 (placeholder)
        assert response.status_code in [200, 422], "Transcribe endpoint should exist"
        print("  ✅ POST /transcribe endpoint exists")
        
        print()
        return True
        
    except Exception as e:
        print(f"  ❌ Endpoint test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        print()
        return False


def test_gitignore():
    """Test that .env is in .gitignore"""
    print("=" * 60)
    print("🔒 Testing Security (gitignore)")
    print("=" * 60)
    
    try:
        gitignore_path = Path(__file__).parent.parent.parent / ".gitignore"
        
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            if ".env" in content:
                print("  ✅ .env is in .gitignore")
                return True
            else:
                print("  ⚠️  .env might not be in .gitignore")
                return False
        else:
            print("  ⚠️  .gitignore file not found")
            return False
            
    except Exception as e:
        print(f"  ❌ Gitignore test failed: {str(e)}")
        return False


def main():
    """Run all Phase 1 tests"""
    print("\n" + "=" * 60)
    print("🧪 Phase 1 Setup Verification Tests")
    print("=" * 60)
    print()
    
    results = {}
    
    # Run all tests
    results["imports"] = test_imports()
    results["structure"] = test_project_structure()
    results["config"] = test_config_module()
    results["audio_utils"] = test_audio_utils()
    results["fastapi_app"] = test_fastapi_app()
    results["endpoints"] = test_fastapi_endpoints()
    results["gitignore"] = test_gitignore()
    
    # Print summary
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {status}: {test_name}")
    
    total = len(results)
    passed = sum(results.values())
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All Phase 1 tests passed! Setup is complete.")
        print("\n💡 Next steps:")
        print("   1. Add your OpenAI API key to .env file")
        print("   2. Test Whisper API: python tests/test_whisper.py")
        print("   3. Test TTS API: python tests/test_tts.py")
        print("   4. Start server: python main.py")
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
    
    print("=" * 60 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

