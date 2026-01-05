#!/usr/bin/env python3
"""
Test script for email verification system.
Tests the complete flow: registration -> email sending -> login (should fail) -> verification -> login (should succeed)
"""
import sys
import requests
import json
from datetime import datetime
import time

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
TEST_EMAIL = f"test_{int(time.time())}@example.com"  # Unique email for each test run
TEST_PASSWORD = "TestPassword123!"
TEST_NAME = "Test User"

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_success(message):
    """Print a success message."""
    print(f"✅ {message}")

def print_error(message):
    """Print an error message."""
    print(f"❌ {message}")

def print_info(message):
    """Print an info message."""
    print(f"ℹ️  {message}")

def test_registration():
    """Test user registration."""
    print_section("1. Testing User Registration")
    
    url = f"{BASE_URL}/auth/register"
    data = {
        "email": TEST_EMAIL,
        "name": TEST_NAME,
        "password": TEST_PASSWORD
    }
    
    print_info(f"Registering user: {TEST_EMAIL}")
    try:
        response = requests.post(url, json=data, timeout=10)
        print_info(f"Response status: {response.status_code}")
        
        if response.status_code == 201:
            user_data = response.json()
            print_success(f"User registered successfully!")
            print_info(f"User ID: {user_data.get('id')}")
            print_info(f"Email verified: {user_data.get('email_verified', False)}")
            return True, user_data
        else:
            error = response.json() if response.content else {"detail": response.text}
            print_error(f"Registration failed: {error.get('detail', 'Unknown error')}")
            return False, None
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend. Is the server running on http://localhost:8000?")
        return False, None
    except Exception as e:
        print_error(f"Registration error: {e}")
        return False, None

def test_login_unverified():
    """Test login with unverified email (should fail)."""
    print_section("2. Testing Login with Unverified Email (Should Fail)")
    
    url = f"{BASE_URL}/auth/login"
    data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    print_info(f"Attempting to login with unverified email: {TEST_EMAIL}")
    try:
        response = requests.post(url, json=data, timeout=10)
        print_info(f"Response status: {response.status_code}")
        
        if response.status_code == 403:
            error_data = response.json()
            print_success("Login correctly blocked - email not verified!")
            print_info(f"Error message: {error_data.get('detail', 'No detail')}")
            return True
        elif response.status_code == 200:
            print_error("Login succeeded when it should have failed! Email verification check is not working.")
            return False
        else:
            error_data = response.json() if response.content else {"detail": response.text}
            print_error(f"Unexpected response: {error_data.get('detail', 'Unknown error')}")
            return False
    except Exception as e:
        print_error(f"Login test error: {e}")
        return False

def get_verification_token_from_db(email):
    """Get verification token from database (for testing purposes)."""
    try:
        # Try to import database utilities
        import os
        import sys
        # Add parent directory to path to import app modules
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app.core.database import SessionLocal
        from app.models.models import User
        
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
            if user and user.verification_token:
                return user.verification_token
            return None
        finally:
            db.close()
    except Exception as e:
        print_info(f"Could not get token from database: {e}")
        print_info("You can manually query: SELECT verification_token FROM users WHERE email = ?")
        return None

def test_verify_email(token):
    """Test email verification endpoint."""
    print_section("4. Testing Email Verification")
    
    if not token:
        print_error("No verification token provided. Cannot test verification.")
        print_info("To get the token:")
        print_info("  1. Check backend logs after registration")
        print_info("  2. Or query database: SELECT verification_token FROM users WHERE email = ?")
        return False
    
    url = f"{BASE_URL}/auth/verify-email"
    data = {
        "token": token
    }
    
    print_info(f"Verifying email with token: {token[:20]}...")
    try:
        response = requests.post(url, json=data, timeout=10)
        print_info(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print_success("Email verified successfully!")
            print_info(f"Message: {result.get('message', 'No message')}")
            return True
        else:
            error_data = response.json() if response.content else {"detail": response.text}
            print_error(f"Verification failed: {error_data.get('detail', 'Unknown error')}")
            return False
    except Exception as e:
        print_error(f"Verification test error: {e}")
        return False

def test_login_verified():
    """Test login after email verification (should succeed)."""
    print_section("5. Testing Login After Verification (Should Succeed)")
    
    url = f"{BASE_URL}/auth/login"
    data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    print_info(f"Attempting to login with verified email: {TEST_EMAIL}")
    try:
        response = requests.post(url, json=data, timeout=10)
        print_info(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            print_success("Login succeeded after email verification!")
            print_info(f"Token type: {token_data.get('token_type', 'N/A')}")
            print_info(f"Access token: {token_data.get('access_token', 'N/A')[:50]}...")
            return True, token_data.get('access_token')
        else:
            error_data = response.json() if response.content else {"detail": response.text}
            print_error(f"Login failed: {error_data.get('detail', 'Unknown error')}")
            return False, None
    except Exception as e:
        print_error(f"Login test error: {e}")
        return False, None

def test_resend_verification():
    """Test resend verification email endpoint."""
    print_section("6. Testing Resend Verification Email")
    
    url = f"{BASE_URL}/auth/resend-verification"
    data = {
        "email": TEST_EMAIL
    }
    
    print_info(f"Requesting resend verification email for: {TEST_EMAIL}")
    try:
        response = requests.post(url, json=data, timeout=10)
        print_info(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print_success("Resend verification request successful!")
            print_info(f"Message: {result.get('message', 'No message')}")
            return True
        else:
            error_data = response.json() if response.content else {"detail": response.text}
            print_error(f"Resend failed: {error_data.get('detail', 'Unknown error')}")
            return False
    except Exception as e:
        print_error(f"Resend test error: {e}")
        return False

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("  EMAIL VERIFICATION SYSTEM TEST")
    print("=" * 60)
    print(f"\nTest Configuration:")
    print(f"  Backend URL: {BASE_URL}")
    print(f"  Test Email: {TEST_EMAIL}")
    print(f"  Test Name: {TEST_NAME}")
    print(f"\n⚠️  Make sure your backend server is running on http://localhost:8000")
    print(f"⚠️  Make sure SMTP is configured in your .env file")
    
    results = {}
    
    # Test 1: Registration
    success, user_data = test_registration()
    results['registration'] = success
    if not success:
        print_error("\n❌ Registration failed. Cannot continue with other tests.")
        return
    
    # Test 2: Login with unverified email (should fail)
    results['login_unverified'] = test_login_unverified()
    
    # Test 3: Resend verification
    results['resend_verification'] = test_resend_verification()
    
    # Test 4: Email verification (get token from database or user input)
    print_section("4. Email Verification")
    print_info("Attempting to get verification token from database...")
    token = get_verification_token_from_db(TEST_EMAIL)
    
    if not token:
        print_info("Token not found in database. Options:")
        print_info("  1. Check your email inbox for the verification email")
        print_info("  2. Check backend logs for the verification token")
        print_info("  3. Enter token manually:")
        token = input("\nEnter verification token (or press Enter to skip): ").strip()
    
    if token:
        print_success(f"Found verification token: {token[:30]}...")
        results['verify_email'] = test_verify_email(token)
        
        # Test 5: Login after verification (should succeed)
        if results.get('verify_email'):
            results['login_verified'], access_token = test_login_verified()
        else:
            print_info("Skipping login test - email not verified")
    else:
        print_info("Skipping email verification test (no token available)")
        results['verify_email'] = None
        results['login_verified'] = None
    
    # Summary
    print_section("TEST SUMMARY")
    print(f"Registration:           {'✅ PASS' if results.get('registration') else '❌ FAIL'}")
    print(f"Login (unverified):     {'✅ PASS' if results.get('login_unverified') else '❌ FAIL'}")
    print(f"Resend verification:    {'✅ PASS' if results.get('resend_verification') else '❌ FAIL'}")
    if results.get('verify_email') is not None:
        print(f"Email verification:     {'✅ PASS' if results.get('verify_email') else '❌ FAIL'}")
        print(f"Login (verified):      {'✅ PASS' if results.get('login_verified') else '❌ FAIL'}")
    else:
        print(f"Email verification:     ⏭️  SKIPPED")
        print(f"Login (verified):      ⏭️  SKIPPED")
    
    all_passed = all(
        v for k, v in results.items() 
        if v is not None and k in ['registration', 'login_unverified', 'resend_verification']
    )
    
    if all_passed:
        print_success("\n🎉 Core email verification flow is working!")
    else:
        print_error("\n⚠️  Some tests failed. Check the errors above.")
    
    print(f"\nTest email used: {TEST_EMAIL}")
    print("You can use this email to test manually or clean it up from the database.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

