#!/usr/bin/env python3
"""
Email Service Debugging Script
"""
import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("EMAIL SERVICE DEBUGGING")
print("=" * 60)
print()

# Check environment variables
print("1. ENVIRONMENT VARIABLES:")
print("-" * 60)
smtp_host = os.getenv('SMTP_HOST', '')
smtp_port = os.getenv('SMTP_PORT', '')
smtp_user = os.getenv('SMTP_USER', '')
smtp_password = os.getenv('SMTP_PASSWORD', '')
from_email = os.getenv('FROM_EMAIL', '')

print(f"SMTP_HOST: {smtp_host}")
print(f"SMTP_PORT: {smtp_port}")
print(f"SMTP_USER: {smtp_user}")
print(f"SMTP_PASSWORD: {'*' * len(smtp_password) if smtp_password else 'NOT SET'} (length: {len(smtp_password)})")
print(f"FROM_EMAIL: {from_email}")
print()

# Check password format
print("2. PASSWORD ANALYSIS:")
print("-" * 60)
if not smtp_password:
    print("❌ SMTP_PASSWORD is not set!")
    sys.exit(1)

# Store original for comparison
original_password = smtp_password
print(f"Original password length: {len(original_password)} characters")
print(f"Original password repr: {repr(original_password)}")

# Strip all whitespace (spaces, tabs, newlines, etc.)
smtp_password = smtp_password.strip()
if original_password != smtp_password:
    print(f"⚠️  Password had leading/trailing whitespace - stripped")
    print(f"   Before: {repr(original_password)}")
    print(f"   After:  {repr(smtp_password)}")

# Remove any remaining spaces
if ' ' in smtp_password:
    print(f"⚠️  Password contains spaces")
    smtp_password = smtp_password.replace(' ', '')
    print(f"   Removed spaces, new length: {len(smtp_password)}")

# Check for other whitespace characters
whitespace_chars = ['\t', '\n', '\r', '\v', '\f']
found_whitespace = [c for c in smtp_password if c in whitespace_chars]
if found_whitespace:
    print(f"⚠️  Password contains other whitespace: {found_whitespace}")
    for char in whitespace_chars:
        smtp_password = smtp_password.replace(char, '')
    print(f"   Cleaned password length: {len(smtp_password)}")

if len(smtp_password) != 16:
    print(f"❌ Password length is {len(smtp_password)}, expected exactly 16")
    print(f"   This might be the issue!")
else:
    print(f"✅ Password length is correct (16 characters)")

# Check for non-alphanumeric (Gmail app passwords are alphanumeric)
non_alnum = [c for c in smtp_password if not c.isalnum()]
if non_alnum:
    print(f"⚠️  Password contains non-alphanumeric characters: {non_alnum}")
    print(f"   Gmail app passwords should only contain letters and numbers")
else:
    print(f"✅ Password contains only alphanumeric characters")

# Show character breakdown
print(f"Password characters: {list(smtp_password)}")
print(f"Password preview: {smtp_password[:4]}...{smtp_password[-4:]}")
print(f"Final password to use: {repr(smtp_password)}")
print()

# Check email format
print("3. EMAIL FORMAT CHECK:")
print("-" * 60)
if '@' not in smtp_user or '@' not in from_email:
    print("❌ Invalid email format")
    sys.exit(1)
print(f"✅ Email format looks valid")
if smtp_user != from_email:
    print(f"⚠️  SMTP_USER and FROM_EMAIL don't match")
else:
    print(f"✅ SMTP_USER and FROM_EMAIL match")
print()

# Test SMTP connection
print("4. SMTP CONNECTION TEST:")
print("-" * 60)
try:
    print(f"Connecting to {smtp_host}:{smtp_port}...")
    server = smtplib.SMTP(smtp_host, int(smtp_port), timeout=10)
    print("✅ Connected to SMTP server")
    
    print("Starting TLS...")
    server.starttls()
    print("✅ TLS started successfully")
    
    print(f"Attempting login with user: {smtp_user}")
    print(f"Password length: {len(smtp_password)}")
    server.login(smtp_user, smtp_password)
    print("✅✅✅ LOGIN SUCCESSFUL! ✅✅✅")
    
    # Try to send a test email
    print()
    print("5. SENDING TEST EMAIL:")
    print("-" * 60)
    
    # Get test recipient email (user who should receive the email)
    test_email = os.getenv('TEST_EMAIL', '')
    if not test_email:
        # If no TEST_EMAIL env var, prompt for it
        print("No TEST_EMAIL environment variable set.")
        print("Enter a test email address to receive the test email:")
        test_email = input("Test email address: ").strip()
        if not test_email:
            print("⚠️  No test email provided. Skipping test email send.")
            server.quit()
            print()
            print("=" * 60)
            print("✅ SMTP CONNECTION TEST PASSED!")
            print("=" * 60)
            sys.exit(0)
    
    if '@' not in test_email:
        print(f"❌ Invalid test email format: {test_email}")
        server.quit()
        sys.exit(1)
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Test Email from InterviewAI Debug Script'
    msg['From'] = from_email  # Interview AI is the sender
    msg['To'] = test_email  # User should receive the email
    
    text = 'This is a test email from the InterviewAI email debugging script.'
    msg.attach(MIMEText(text, 'plain'))
    
    print(f"Sending test email FROM {from_email} TO {test_email}...")
    server.send_message(msg)
    print("✅✅✅ TEST EMAIL SENT SUCCESSFULLY! ✅✅✅")
    print(f"   Interview AI ({from_email}) sent email to {test_email}")
    print(f"   Check the inbox at {test_email}")
    
    server.quit()
    print()
    print("=" * 60)
    print("✅ ALL TESTS PASSED - EMAIL SERVICE IS WORKING!")
    print("=" * 60)
    
except smtplib.SMTPAuthenticationError as e:
    print(f"❌ AUTHENTICATION FAILED")
    print(f"   Error code: {e.smtp_code}")
    print(f"   Error message: {e.smtp_error.decode() if e.smtp_error else str(e)}")
    print()
    print("=" * 60)
    print("TROUBLESHOOTING STEPS:")
    print("=" * 60)
    print()
    print("The password format looks correct, but Gmail is rejecting it.")
    print("This usually means one of the following:")
    print()
    print("1. ⚠️  2-Step Verification MUST be enabled:")
    print("   - Go to: https://myaccount.google.com/security")
    print("   - Make sure 2-Step Verification is ON")
    print("   - App Passwords only work with 2-Step Verification enabled")
    print()
    print("2. 🔑 Generate a FRESH App Password:")
    print("   - Go to: https://myaccount.google.com/apppasswords")
    print("   - If you don't see this option, 2-Step Verification is not enabled")
    print("   - Select 'Mail' as the app")
    print("   - Select your device (or 'Other' and type 'InterviewAI')")
    print("   - Copy the 16-character password IMMEDIATELY (it's shown only once)")
    print("   - Update SMTP_PASSWORD in your .env file")
    print()
    print("3. 🔒 Check for security blocks:")
    print("   - Go to: https://myaccount.google.com/security")
    print("   - Look for any security alerts or blocks")
    print("   - Check 'Recent security activity' for any issues")
    print()
    print("4. 📧 Verify account status:")
    print(f"   - Make sure {smtp_user} is a valid Gmail account")
    print("   - Try logging into Gmail web interface to verify account is active")
    print()
    print("5. 🔄 Try regenerating the App Password:")
    print("   - Delete the old app password")
    print("   - Generate a completely new one")
    print("   - Make sure to copy it exactly (no spaces, all 16 characters)")
    print()
    print("Current password analysis:")
    print(f"   - Length: {len(smtp_password)} characters (should be 16)")
    print(f"   - Format: {smtp_password[:4]}...{smtp_password[-4:]}")
    print(f"   - Alphanumeric only: {smtp_password.isalnum()}")
    print()
    sys.exit(1)
    
except smtplib.SMTPException as e:
    print(f"❌ SMTP ERROR: {e}")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ UNEXPECTED ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

