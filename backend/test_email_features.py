#!/usr/bin/env python3
"""
Test script for new email verification features.
Tests admin endpoints and email status in registration.
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000/api/v1"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_success(msg):
    print(f"✅ {msg}")

def print_error(msg):
    print(f"❌ {msg}")

def print_info(msg):
    print(f"ℹ️  {msg}")

def test_smtp_health():
    """Test SMTP health check endpoint."""
    print_section("1. Testing SMTP Health Check")
    try:
        response = requests.get(f"{BASE_URL}/admin/smtp-health")
        if response.status_code == 200:
            data = response.json()
            print_success(f"SMTP Health Check Response:")
            print(f"   Configured: {data.get('configured')}")
            print(f"   Can Connect: {data.get('can_connect')}")
            if data.get('error'):
                print_error(f"Error: {data.get('error')}")
            else:
                print_success("SMTP is properly configured!")
            return data.get('configured') and data.get('can_connect')
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Failed to check SMTP health: {e}")
        return False

def test_list_unverified_users():
    """Test listing unverified users."""
    print_section("2. Testing List Unverified Users")
    try:
        response = requests.get(f"{BASE_URL}/admin/unverified-users")
        if response.status_code == 200:
            users = response.json()
            print_success(f"Found {len(users)} unverified user(s)")
            for user in users:
                print(f"   - {user.get('email')} ({user.get('name')})")
                if user.get('verification_token'):
                    print(f"     Token: {user.get('verification_token')[:30]}...")
            return True
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Failed to list unverified users: {e}")
        return False

def test_get_user(email):
    """Test getting user by email."""
    print_section(f"3. Testing Get User: {email}")
    try:
        response = requests.get(f"{BASE_URL}/admin/user/{email}")
        if response.status_code == 200:
            user = response.json()
            print_success(f"User found: {user.get('email')}")
            print(f"   Name: {user.get('name')}")
            print(f"   Verified: {user.get('email_verified')}")
            print(f"   Has Token: {user.get('has_verification_token')}")
            return True
        elif response.status_code == 404:
            print_info(f"User not found: {email}")
            return False
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Failed to get user: {e}")
        return False

def test_manual_verify(email):
    """Test manually verifying a user."""
    print_section(f"4. Testing Manual Verification: {email}")
    try:
        response = requests.post(
            f"{BASE_URL}/admin/verify-user",
            json={"email": email},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            data = response.json()
            print_success(f"User verified: {data.get('message')}")
            return True
        elif response.status_code == 404:
            print_info(f"User not found: {email}")
            return False
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Failed to verify user: {e}")
        return False

def test_registration_with_email_status():
    """Test registration returns email_sent status."""
    print_section("5. Testing Registration Email Status")
    import random
    test_email = f"test_{random.randint(1000, 9999)}@example.com"
    test_name = "Test User"
    test_password = "TestPassword123"
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json={
                "email": test_email,
                "name": test_name,
                "password": test_password
            },
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 201:
            user = response.json()
            print_success(f"Registration successful: {user.get('email')}")
            email_sent = user.get('email_sent')
            if email_sent is not None:
                print_success(f"Email status included in response: email_sent={email_sent}")
                if not email_sent:
                    print_error("⚠️  Email was NOT sent! Check SMTP configuration.")
                else:
                    print_success("Email was sent successfully!")
            else:
                print_error("⚠️  email_sent field missing from response!")
            return True
        else:
            print_error(f"Registration failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Failed to test registration: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("  EMAIL VERIFICATION FEATURES TEST")
    print("="*60)
    print(f"\nTesting against: {BASE_URL}")
    print("⚠️  Make sure your backend is running on http://localhost:8000")
    
    results = {}
    
    # Test 1: SMTP Health
    results['smtp_health'] = test_smtp_health()
    
    # Test 2: List Unverified Users
    results['list_unverified'] = test_list_unverified_users()
    
    # Test 3: Get User (test with a known email or skip)
    test_email = input("\nEnter an email to test get-user endpoint (or press Enter to skip): ").strip()
    if test_email:
        results['get_user'] = test_get_user(test_email)
    
    # Test 4: Manual Verification (optional)
    verify_email = input("\nEnter an email to manually verify (or press Enter to skip): ").strip()
    if verify_email:
        results['manual_verify'] = test_manual_verify(verify_email)
    
    # Test 5: Registration with email status
    results['registration_status'] = test_registration_with_email_status()
    
    # Summary
    print_section("Test Summary")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:30} {status}")
    
    print("\n" + "="*60)
    print("  Testing Complete")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)

