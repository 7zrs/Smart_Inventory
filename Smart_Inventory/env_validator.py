"""Environment variable validation."""
import os
import sys


def validate_environment():
    """Validate required environment variables."""
    # Only validate during Django commands
    if 'manage.py' not in sys.argv[0] and 'django-admin' not in sys.argv[0]:
        return

    # Skip validation during migrations and other safe commands
    safe_commands = ['migrate', 'makemigrations', 'createsuperuser', 'collectstatic']
    if any(cmd in sys.argv for cmd in safe_commands):
        return

    required_vars = {
        'SECRET_KEY': 'Django secret key',
        'GOOGLE_API_KEY': 'Google Gemini API key'
    }

    missing = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value or value.strip() == '':
            missing.append(f"{var} ({description})")

    # Check for placeholder values
    api_key = os.getenv('GOOGLE_API_KEY', '')
    if api_key in ['YOUR_NEW_GEMINI_API_KEY_HERE', 'your-gemini-api-key-here']:
        missing.append('GOOGLE_API_KEY (still has placeholder value)')

    if missing:
        print("\n" + "="*80)
        print("❌ ENVIRONMENT CONFIGURATION ERROR")
        print("="*80)
        print("\nMissing or invalid environment variables:\n")
        for var in missing:
            print(f"  • {var}")
        print("\nSetup Instructions:")
        print("  1. Edit .env file")
        print("  2. Add your actual Google Gemini API key")
        print("  3. Get key from: https://makersuite.google.com/app/apikey")
        print("\n" + "="*80 + "\n")
        sys.exit(1)

    # Validate format
    if api_key.startswith('"') or api_key.startswith("'"):
        print("\n⚠ WARNING: GOOGLE_API_KEY has quotes around it.")
        print("Remove quotes from .env: GOOGLE_API_KEY=your_key_here\n")

    print("✓ Environment validation passed")
