#!/usr/bin/env python3
"""
Security Configuration Checker for PrepWise

This script checks for common security misconfigurations and helps ensure
your deployment follows security best practices.

Usage:
    python security_check.py

SECURITY NOTE: This is a basic check. It does not replace proper security
audits, penetration testing, or code review.
"""
import os
import sys
from pathlib import Path
from typing import List, Tuple

# ANSI color codes for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def check_env_file() -> List[Tuple[str, str, str]]:
    """Check .env file for security issues."""
    issues = []
    env_file = Path('.env')

    if not env_file.exists():
        issues.append(('ERROR', '.env file not found', 'Create .env file from .env.example'))
        return issues

    with open(env_file, 'r') as f:
        content = f.read()

    # Check for default/placeholder values
    if 'your-secret-key-change-in-production' in content:
        issues.append(('ERROR', 'SECRET_KEY is still set to default', 'Generate strong secret key'))

    if 'your-openai-api-key-here' in content:
        issues.append(('WARNING', 'OPENAI_API_KEY is placeholder', 'Set your actual OpenAI API key'))

    # Check for insecure configurations
    if 'DEBUG=True' in content:
        issues.append(('WARNING', 'DEBUG mode is enabled', 'Set DEBUG=False in production'))

    if 'ENVIRONMENT=development' in content:
        issues.append(('INFO', 'Environment is set to development', 'Set ENVIRONMENT=production for production'))

    # Check for CORS wildcards
    if 'CORS_ORIGINS=*' in content or 'CORS_ORIGINS="*"' in content:
        issues.append(('ERROR', 'CORS allows all origins (*)', 'Specify explicit allowed origins'))

    # Check for weak SECRET_KEY
    if 'SECRET_KEY=' in content:
        for line in content.split('\n'):
            if line.startswith('SECRET_KEY='):
                key = line.split('=', 1)[1].strip().strip('"\'')
                if len(key) < 32:
                    issues.append(('ERROR', 'SECRET_KEY is too short', 'Use at least 32 characters'))

    return issues


def check_gitignore() -> List[Tuple[str, str, str]]:
    """Check .gitignore for security patterns."""
    issues = []
    gitignore_file = Path('.gitignore')

    if not gitignore_file.exists():
        issues.append(('ERROR', '.gitignore not found', 'Create .gitignore to exclude .env files'))
        return issues

    with open(gitignore_file, 'r') as f:
        content = f.read()

    # Check if .env is ignored
    if '.env' not in content:
        issues.append(('ERROR', '.env not in .gitignore', 'Add .env to .gitignore'))

    return issues


def check_file_permissions() -> List[Tuple[str, str, str]]:
    """Check file permissions for sensitive files."""
    issues = []

    # Check .env file permissions (should be readable only by owner)
    env_file = Path('.env')
    if env_file.exists():
        stat_info = env_file.stat()
        mode = oct(stat_info.st_mode)[-3:]
        if mode != '600':
            issues.append(('WARNING', f'.env permissions are {mode}', 'Set to 600 (chmod 600 .env)'))

    return issues


def check_dependencies() -> List[Tuple[str, str, str]]:
    """Check for known vulnerable dependencies."""
    issues = []

    # Check if requirements.txt exists
    req_file = Path('requirements.txt')
    if not req_file.exists():
        issues.append(('INFO', 'requirements.txt not found', 'Ensure dependencies are documented'))
        return issues

    # Suggest running security checks
    issues.append(('INFO', 'Dependencies check', 'Run: pip install safety && safety check'))

    return issues


def check_security_headers() -> List[Tuple[str, str, str]]:
    """Check if security headers are implemented."""
    issues = []

    # Check main.py for security headers
    main_file = Path('main.py')
    if main_file.exists():
        with open(main_file, 'r') as f:
            content = f.read()

        if 'X-Content-Type-Options' not in content:
            issues.append(('WARNING', 'Security headers may not be configured', 'Check main.py for security headers'))
    else:
        issues.append(('INFO', 'main.py not found', 'Skipping security headers check'))

    return issues


def check_api_keys() -> List[Tuple[str, str, str]]:
    """Check for hardcoded API keys in code."""
    issues = []

    # Patterns that might indicate hardcoded secrets
    dangerous_patterns = [
        'sk-',  # OpenAI/Stripe secret keys
        'pk_live_',  # Stripe publishable keys (live)
        'sk_live_',  # Stripe secret keys (live)
        'whsec_',  # Stripe webhook secrets
    ]

    # Check Python files
    for py_file in Path('.').rglob('*.py'):
        # Skip this security check script
        if py_file.name == 'security_check.py':
            continue

        # Skip test files and migrations
        if 'test' in str(py_file) or 'alembic' in str(py_file):
            continue

        with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for pattern in dangerous_patterns:
                if pattern in content:
                    # Check if it's in a comment or docstring
                    if f'"{pattern}' not in content and f"'{pattern}" not in content:
                        continue
                    issues.append(('ERROR', f'Possible hardcoded key in {py_file}', 'Remove hardcoded secrets'))
                    break

    return issues


def print_report(all_issues: List[Tuple[str, str, str]]):
    """Print formatted security report."""
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}PrepWise Security Configuration Check{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")

    errors = [i for i in all_issues if i[0] == 'ERROR']
    warnings = [i for i in all_issues if i[0] == 'WARNING']
    info = [i for i in all_issues if i[0] == 'INFO']

    if errors:
        print(f"{RED}ERRORS ({len(errors)}):{RESET}")
        for severity, issue, fix in errors:
            print(f"  {RED}✗{RESET} {issue}")
            print(f"    → {fix}\n")

    if warnings:
        print(f"{YELLOW}WARNINGS ({len(warnings)}):{RESET}")
        for severity, issue, fix in warnings:
            print(f"  {YELLOW}!{RESET} {issue}")
            print(f"    → {fix}\n")

    if info:
        print(f"{BLUE}INFO ({len(info)}):{RESET}")
        for severity, issue, fix in info:
            print(f"  {BLUE}ℹ{RESET} {issue}")
            print(f"    → {fix}\n")

    if not all_issues:
        print(f"{GREEN}✓ No security issues found!{RESET}\n")

    # Summary
    print(f"{BLUE}{'='*80}{RESET}")
    print(f"Total Issues: {len(all_issues)} ({len(errors)} errors, {len(warnings)} warnings, {len(info)} info)")
    print(f"{BLUE}{'='*80}{RESET}\n")

    # Recommendations
    print(f"{BLUE}Additional Security Recommendations:{RESET}\n")
    print("1. Run dependency vulnerability scan: pip install safety && safety check")
    print("2. Enable 2FA for all deployment platforms (Vercel, Render, etc.)")
    print("3. Set up monitoring and alerts for your application")
    print("4. Review SECURITY.md for complete security checklist")
    print("5. Rotate API keys every 90 days")
    print("6. Enable API key restrictions (IP whitelist, domain restrictions)")
    print("7. Set up automated backups for production database")
    print("8. Configure SSL/TLS certificate for production")
    print("9. Review logs regularly for suspicious activity")
    print("10. Perform security audit before production deployment\n")

    return len(errors) > 0


def main():
    """Run all security checks."""
    print(f"{BLUE}Running security configuration checks...{RESET}\n")

    all_issues = []
    all_issues.extend(check_env_file())
    all_issues.extend(check_gitignore())
    all_issues.extend(check_file_permissions())
    all_issues.extend(check_dependencies())
    all_issues.extend(check_security_headers())
    all_issues.extend(check_api_keys())

    has_errors = print_report(all_issues)

    if has_errors:
        print(f"{RED}⚠ Security issues found! Please address before deploying to production.{RESET}\n")
        sys.exit(1)
    else:
        print(f"{GREEN}✓ Basic security checks passed!{RESET}")
        print(f"{YELLOW}Note: This is a basic check. Perform thorough security audit before production.{RESET}\n")
        sys.exit(0)


if __name__ == '__main__':
    main()
