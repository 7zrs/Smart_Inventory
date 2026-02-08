#!/usr/bin/env python
"""Test environment configuration."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv


def test_environment():
    print("="*80)
    print("ENVIRONMENT CONFIGURATION TEST")
    print("="*80)
    print()

    # Check .env exists
    if not Path('.env').exists():
        print("❌ FAIL: .env file not found")
        print("\nCreate .env from .env.example")
        return False

    load_dotenv()

    # Check SECRET_KEY
    secret_key = os.getenv('SECRET_KEY')
    if not secret_key:
        print("❌ FAIL: SECRET_KEY not set")
        return False
    if len(secret_key) < 50:
        print("⚠ WARNING: SECRET_KEY too short (should be 50+ characters)")
    print(f"✓ SECRET_KEY set ({len(secret_key)} chars)")

    # Check GOOGLE_API_KEY
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ FAIL: GOOGLE_API_KEY not set")
        return False
    if api_key.startswith('"') or api_key.startswith("'"):
        print("❌ FAIL: GOOGLE_API_KEY has quotes around it")
        print("   Remove quotes from .env: GOOGLE_API_KEY=your_key_here")
        return False
    if api_key == "YOUR_NEW_GEMINI_API_KEY_HERE" or api_key == "your-gemini-api-key-here":
        print("❌ FAIL: GOOGLE_API_KEY is still using placeholder value")
        print("   Get a real API key from: https://makersuite.google.com/app/apikey")
        return False
    if not api_key.startswith('AIza'):
        print("⚠ WARNING: API key format unexpected (should start with 'AIza')")
    print(f"✓ GOOGLE_API_KEY set ({api_key[:10]}...)")

    # Check DEBUG setting
    debug = os.getenv('DEBUG', 'True')
    print(f"✓ DEBUG={debug}")

    # Check ALLOWED_HOSTS
    allowed_hosts = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1')
    print(f"✓ ALLOWED_HOSTS={allowed_hosts}")

    print("\n" + "="*80)
    print("✓ ALL TESTS PASSED")
    print("="*80)
    print("\nYou can now start the application with:")
    print("  Windows: .\\run_project.bat")
    print("  Manual:  python manage.py runserver")
    return True


if __name__ == '__main__':
    sys.exit(0 if test_environment() else 1)
