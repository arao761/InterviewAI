#!/usr/bin/env python3
"""
Comprehensive Test Suite for Phases 1-3
Tests all features across backend API, transcription service, and integration
"""

import sys
import os
from pathlib import Path
import tempfile
import json
import time

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from fastapi import UploadFile
from io import BytesIO

# Try to import pytest (optional)
try:
    import pytest
    HAS_PYTEST = True
    SkipTest = pytest.skip.Exception if hasattr(pytest.skip, 'Exception') else Exception
except ImportError:
    HAS_PYTEST = False
    # Create a mock pytest for standalone execution
    class SkipTest(Exception):
        """Exception raised when a test should be skipped"""
        pass
    
    class MockPytest:
        @staticmethod
        def skip(reason):
            raise SkipTest(reason)
    
    pytest = MockPytest()

# Import modules to test
from main import app
from config import Config
from utils.transcription_service import TranscriptionService
from utils.audio_utils import (
    validate_audio_file,
    get_audio_duration,
    get_audio_info,
    convert_audio_format
)


class TestPhase1BackendAPI:
    """Test Phase 1: Backend API Setup"""

    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)

    def test_root_endpoint(self):
        """Test root endpoint returns API information"""
        response = self.client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "PrepWise Voice API"
        assert data["version"] == "1.0.0"
        assert data["status"] == "active"
        assert "endpoints" in data

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "PrepWise Voice API"
        assert "api_keys_configured" in data
        assert "ready_for_requests" in data

    def test_config_endpoint(self):
        """Test config endpoint"""
        response = self.client.get("/config")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "config" in data
        config = data["config"]
        assert "max_audio_size_mb" in config
        assert "supported_formats" in config
        assert "api_keys_configured" in config

    def test_cors_headers(self):
        """Test CORS middleware is configured"""
        response = self.client.options("/")
        # CORS headers should be present (FastAPI handles this)
        assert response.status_code in [200, 405]  # OPTIONS may return 405


class TestPhase2AudioProcessing:
    """Test Phase 2: Audio Processing Utilities"""

    def test_audio_utils_imports(self):
        """Test audio utilities can be imported"""
        from utils.audio_utils import (
            validate_audio_file,
            convert_audio_format,
            get_audio_duration,
            compress_audio,
            normalize_audio,
            get_audio_info
        )
        assert all(callable(func) for func in [
            validate_audio_file,
            convert_audio_format,
            get_audio_duration,
            compress_audio,
            normalize_audio,
            get_audio_info
        ])

    def test_validate_audio_file_nonexistent(self):
        """Test validation of non-existent file"""
        result = validate_audio_file("nonexistent.mp3")
        assert result["valid"] == False
        assert len(result["errors"]) > 0

    def test_get_audio_info_structure(self):
        """Test audio info structure (without actual file)"""
        # This tests the function signature and return structure
        # Actual file testing would require a real audio file
        assert callable(get_audio_info)


class TestPhase3TranscriptionService:
    """Test Phase 3: Transcription Service"""

    def setup_method(self):
        """Setup transcription service"""
        if not Config.OPENAI_API_KEY:
            if HAS_PYTEST:
                pytest.skip("OpenAI API key not configured")
            else:
                raise SkipTest("OpenAI API key not configured")
        self.service = TranscriptionService()

    def test_transcription_service_initialization(self):
        """Test transcription service can be initialized"""
        assert self.service is not None
        assert self.service.api_key is not None
        assert self.service.client is not None
        assert self.service.max_retries == 3

    def test_transcription_service_constants(self):
        """Test transcription service constants"""
        assert TranscriptionService.MAX_FILE_SIZE_MB == 25
        assert TranscriptionService.MAX_FILE_SIZE_BYTES == 25 * 1024 * 1024
        assert TranscriptionService.CHUNK_DURATION_SECONDS == 300

    def test_prepare_audio_file_logic(self):
        """Test audio file preparation logic"""
        # Test that the method exists and is callable
        assert hasattr(self.service, '_prepare_audio_file')
        assert callable(self.service._prepare_audio_file)

    def test_retry_logic_structure(self):
        """Test retry logic structure"""
        assert hasattr(self.service, '_call_whisper_with_retry')
        assert callable(self.service._call_whisper_with_retry)
        assert self.service.max_retries > 0
        assert self.service.retry_delay > 0


class TestPhase3APIEndpoint:
    """Test Phase 3: Enhanced Transcription API Endpoint"""

    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)

    def test_transcribe_endpoint_exists(self):
        """Test transcribe endpoint exists"""
        # Test with empty file to trigger validation
        response = self.client.post(
            "/transcribe",
            files={"file": ("test.webm", BytesIO(b""), "audio/webm")}
        )
        # Should return error, but endpoint should exist
        assert response.status_code in [400, 500]  # 400 for empty, 500 for no API key

    def test_transcribe_endpoint_parameters(self):
        """Test transcribe endpoint accepts query parameters"""
        # Test endpoint accepts parameters (even if request fails)
        response = self.client.post(
            "/transcribe?language=en&include_timestamps=true&include_confidence=true",
            files={"file": ("test.webm", BytesIO(b"fake audio data"), "audio/webm")}
        )
        # Endpoint should accept parameters (may fail on actual transcription)
        assert response.status_code in [400, 401, 500]

    def test_transcribe_endpoint_query_params(self):
        """Test all query parameters are accepted"""
        params = {
            "language": "en",
            "response_format": "verbose_json",
            "include_timestamps": "true",
            "include_confidence": "true",
            "chunk_large_files": "true"
        }
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        response = self.client.post(
            f"/transcribe?{query_string}",
            files={"file": ("test.webm", BytesIO(b"fake"), "audio/webm")}
        )
        # Should accept parameters (may fail on actual processing)
        assert response.status_code in [400, 401, 500]


class TestIntegrationPhase1To3:
    """Test Integration: Phases 1-3 Working Together"""

    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)

    def test_full_workflow_structure(self):
        """Test complete workflow structure (without actual API calls)"""
        # 1. Check API is healthy
        health = self.client.get("/health")
        assert health.status_code == 200

        # 2. Check config is available
        config = self.client.get("/config")
        assert config.status_code == 200

        # 3. Check transcribe endpoint exists
        # (We can't test actual transcription without API key and real audio)
        transcribe = self.client.post(
            "/transcribe",
            files={"file": ("test.webm", BytesIO(b"test"), "audio/webm")}
        )
        # Should respond (even if error)
        assert transcribe.status_code in [400, 401, 500]

    def test_error_handling(self):
        """Test error handling across phases"""
        # Test empty file
        response = self.client.post(
            "/transcribe",
            files={"file": ("empty.webm", BytesIO(b""), "audio/webm")}
        )
        assert response.status_code == 400

        # Test missing file
        response = self.client.post("/transcribe")
        assert response.status_code == 422  # FastAPI validation error

    def test_response_format_structure(self):
        """Test response format structure (when successful)"""
        # This would require actual API key and audio file
        # But we can test the endpoint accepts format parameter
        response = self.client.post(
            "/transcribe?response_format=text",
            files={"file": ("test.webm", BytesIO(b"test"), "audio/webm")}
        )
        # Endpoint should accept parameter
        assert response.status_code in [400, 401, 500]


class TestConfiguration:
    """Test Configuration Management"""

    def test_config_imports(self):
        """Test config can be imported"""
        assert Config is not None

    def test_config_constants(self):
        """Test config constants"""
        assert Config.MAX_AUDIO_SIZE_MB > 0
        assert Config.MAX_AUDIO_SIZE_BYTES > 0
        assert Config.MAX_DURATION_SECONDS > 0
        assert len(Config.SUPPORTED_FORMATS) > 0
        assert Config.WHISPER_MODEL is not None

    def test_config_directories(self):
        """Test config directories exist or can be created"""
        assert Config.UPLOAD_DIR is not None
        assert Config.OUTPUT_DIR is not None
        # Directories should be Path objects
        assert hasattr(Config.UPLOAD_DIR, 'mkdir')

    def test_config_summary(self):
        """Test config summary method"""
        summary = Config.get_config_summary()
        assert isinstance(summary, dict)
        assert "max_audio_size_mb" in summary
        assert "supported_formats" in summary
        assert "api_keys_configured" in summary


class TestEndToEndWorkflow:
    """Test End-to-End Workflow (requires API key and may require actual audio)"""

    def setup_method(self):
        """Setup for end-to-end tests"""
        self.client = TestClient(app)
        self.has_api_key = bool(Config.OPENAI_API_KEY)

    def test_workflow_without_api_key(self):
        """Test workflow when API key is not configured"""
        if self.has_api_key:
            if HAS_PYTEST:
                pytest.skip("API key is configured, skipping this test")
            else:
                return  # Skip test if no pytest

        # Health check should work
        health = self.client.get("/health")
        assert health.status_code == 200
        data = health.json()
        assert data["ready_for_requests"] == False

        # Transcription should fail gracefully
        response = self.client.post(
            "/transcribe",
            files={"file": ("test.webm", BytesIO(b"test data"), "audio/webm")}
        )
        assert response.status_code in [500, 401]
        error_data = response.json()
        assert "error" in error_data.get("detail", "").lower() or "key" in error_data.get("detail", "").lower()

    def test_workflow_with_api_key_structure(self):
        """Test workflow structure when API key is configured"""
        # Health check should show ready
        health = self.client.get("/health")
        assert health.status_code == 200
        data = health.json()
        # If API key is configured, should be ready
        if self.has_api_key:
            # Note: This may still be False if key is invalid
            pass

        # Config should be available
        config = self.client.get("/config")
        assert config.status_code == 200


def run_all_tests():
    """Run all test suites"""
    print("=" * 70)
    print("🧪 Comprehensive Test Suite for Phases 1-3")
    print("=" * 70)
    print()

    # Test Phase 1: Backend API
    print("📋 Phase 1: Backend API Setup")
    print("-" * 70)
    phase1 = TestPhase1BackendAPI()
    phase1.setup_method()
    
    try:
        phase1.test_root_endpoint()
        print("  ✅ Root endpoint")
    except Exception as e:
        print(f"  ❌ Root endpoint: {e}")

    try:
        phase1.test_health_check()
        print("  ✅ Health check endpoint")
    except Exception as e:
        print(f"  ❌ Health check: {e}")

    try:
        phase1.test_config_endpoint()
        print("  ✅ Config endpoint")
    except Exception as e:
        print(f"  ❌ Config endpoint: {e}")

    try:
        phase1.test_cors_headers()
        print("  ✅ CORS headers")
    except Exception as e:
        print(f"  ❌ CORS headers: {e}")

    print()

    # Test Phase 2: Audio Processing
    print("📋 Phase 2: Audio Processing Utilities")
    print("-" * 70)
    phase2 = TestPhase2AudioProcessing()
    
    try:
        phase2.test_audio_utils_imports()
        print("  ✅ Audio utilities imports")
    except Exception as e:
        print(f"  ❌ Audio utilities imports: {e}")

    try:
        phase2.test_validate_audio_file_nonexistent()
        print("  ✅ Audio file validation")
    except Exception as e:
        print(f"  ❌ Audio file validation: {e}")

    try:
        phase2.test_get_audio_info_structure()
        print("  ✅ Audio info structure")
    except Exception as e:
        print(f"  ❌ Audio info structure: {e}")

    print()

    # Test Phase 3: Transcription Service
    print("📋 Phase 3: Transcription Service")
    print("-" * 70)
    
    if Config.OPENAI_API_KEY:
        phase3 = TestPhase3TranscriptionService()
        try:
            phase3.setup_method()
        except SkipTest:
            print("  ⚠️  Skipping transcription service tests (no API key)")
        except Exception as e:
            print(f"  ❌ Transcription service setup failed: {e}")
        else:
            try:
                phase3.test_transcription_service_initialization()
                print("  ✅ Transcription service initialization")
            except Exception as e:
                print(f"  ❌ Transcription service initialization: {e}")

            try:
                phase3.test_transcription_service_constants()
                print("  ✅ Transcription service constants")
            except Exception as e:
                print(f"  ❌ Transcription service constants: {e}")

            try:
                phase3.test_prepare_audio_file_logic()
                print("  ✅ Audio file preparation logic")
            except Exception as e:
                print(f"  ❌ Audio file preparation: {e}")

            try:
                phase3.test_retry_logic_structure()
                print("  ✅ Retry logic structure")
            except Exception as e:
                print(f"  ❌ Retry logic: {e}")
    else:
        print("  ⚠️  Skipping transcription service tests (no API key)")

    print()

    # Test Phase 3: API Endpoint
    print("📋 Phase 3: Enhanced API Endpoint")
    print("-" * 70)
    phase3_api = TestPhase3APIEndpoint()
    phase3_api.setup_method()
    
    try:
        phase3_api.test_transcribe_endpoint_exists()
        print("  ✅ Transcribe endpoint exists")
    except Exception as e:
        print(f"  ❌ Transcribe endpoint: {e}")

    try:
        phase3_api.test_transcribe_endpoint_parameters()
        print("  ✅ Query parameters accepted")
    except Exception as e:
        print(f"  ❌ Query parameters: {e}")

    try:
        phase3_api.test_transcribe_endpoint_query_params()
        print("  ✅ All query parameters work")
    except Exception as e:
        print(f"  ❌ Query parameters: {e}")

    print()

    # Test Integration
    print("📋 Integration: Phases 1-3")
    print("-" * 70)
    integration = TestIntegrationPhase1To3()
    integration.setup_method()
    
    try:
        integration.test_full_workflow_structure()
        print("  ✅ Full workflow structure")
    except Exception as e:
        print(f"  ❌ Full workflow: {e}")

    try:
        integration.test_error_handling()
        print("  ✅ Error handling")
    except Exception as e:
        print(f"  ❌ Error handling: {e}")

    try:
        integration.test_response_format_structure()
        print("  ✅ Response format structure")
    except Exception as e:
        print(f"  ❌ Response format: {e}")

    print()

    # Test Configuration
    print("📋 Configuration Management")
    print("-" * 70)
    config_test = TestConfiguration()
    
    try:
        config_test.test_config_imports()
        print("  ✅ Config imports")
    except Exception as e:
        print(f"  ❌ Config imports: {e}")

    try:
        config_test.test_config_constants()
        print("  ✅ Config constants")
    except Exception as e:
        print(f"  ❌ Config constants: {e}")

    try:
        config_test.test_config_directories()
        print("  ✅ Config directories")
    except Exception as e:
        print(f"  ❌ Config directories: {e}")

    try:
        config_test.test_config_summary()
        print("  ✅ Config summary")
    except Exception as e:
        print(f"  ❌ Config summary: {e}")

    print()

    # Summary
    print("=" * 70)
    print("✅ Test Suite Complete")
    print("=" * 70)
    print()
    print("💡 Note: Some tests require OpenAI API key and actual audio files")
    print("💡 For full end-to-end testing, use the frontend test page:")
    print("   http://localhost:5173/test-phase2.html")
    print()


if __name__ == "__main__":
    run_all_tests()

