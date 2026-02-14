"""
Setup helper for Smart Inventory.
Called by setup.bat after Python and dependencies are installed.
Handles: .env creation, SECRET_KEY, API key prompt, migrations, superuser.
"""
import os
import sys
import subprocess
import shutil
import secrets
import string


def generate_secret_key(length=50):
    """Generate a Django-compatible SECRET_KEY."""
    chars = string.ascii_letters + string.digits + string.punctuation
    # Exclude characters that break .env parsing: #, ', ", \, =, space
    safe_chars = [c for c in chars if c not in ('#', "'", '"', '\\', '=', ' ')]
    return ''.join(secrets.choice(safe_chars) for _ in range(length))


def create_env_file():
    """Create .env file if it doesn't exist."""
    if os.path.exists('.env'):
        print('[4/7] Setting up environment file...')
        print('  > .env already exists - keeping it')
        return

    print('[4/7] Creating .env file...')

    # Try to copy from .env.example first
    if os.path.exists('.env.example'):
        shutil.copy2('.env.example', '.env')
        print('  > Copied from .env.example')
    else:
        # Generate from scratch
        with open('.env', 'w') as f:
            f.write('SECRET_KEY=your-secret-key-here\n')
            f.write('DEBUG=True\n')
            f.write('ALLOWED_HOSTS=localhost,127.0.0.1\n')
            f.write('GOOGLE_API_KEY=your-gemini-api-key-here\n')
        print('  > Created new .env file')

    # Generate and write SECRET_KEY
    secret_key = generate_secret_key()
    replace_env_value('SECRET_KEY', secret_key)
    print('  > Generated SECRET_KEY')


def replace_env_value(key, value):
    """Replace or add a key=value pair in the .env file."""
    lines = []
    found = False
    with open('.env', 'r') as f:
        for line in f:
            if line.strip().startswith(key + '=') or line.strip().startswith(key + ' ='):
                lines.append(f'{key}={value}\n')
                found = True
            else:
                lines.append(line)
    if not found:
        lines.append(f'{key}={value}\n')
    with open('.env', 'w') as f:
        f.writelines(lines)


def get_current_api_key():
    """Read the current GOOGLE_API_KEY from .env."""
    if not os.path.exists('.env'):
        return None
    with open('.env', 'r') as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith('GOOGLE_API_KEY='):
                return stripped.split('=', 1)[1].strip()
    return None


def prompt_api_key():
    """Prompt user for Gemini API key if not already set."""
    print('[5/7] Checking Google Gemini API key...')

    current_key = get_current_api_key()
    placeholder_values = (None, '', 'your-gemini-api-key-here', 'YOUR_NEW_GEMINI_API_KEY_HERE')

    if current_key not in placeholder_values:
        print('  > API key already configured')
        return

    print()
    print('  ========================================')
    print('  Google Gemini API Key Required')
    print('  ========================================')
    print()
    print('  The AI Assistant requires a Google Gemini API key.')
    print('  Get your FREE API key from:')
    print('    https://makersuite.google.com/app/apikey')
    print()
    print('  You can:')
    print('    1. Enter your API key now')
    print('    2. Press Enter to skip (AI features will NOT work)')
    print()

    try:
        api_key = input('  Paste your API key here: ').strip()
    except EOFError:
        api_key = ''

    if api_key:
        replace_env_value('GOOGLE_API_KEY', api_key)
        print('  > API key saved to .env')
    else:
        print()
        print('  > Skipped - AI Assistant will NOT work until you add it.')
        print('  > Edit .env and set GOOGLE_API_KEY=your-key-here')


def run_migrations(python_cmd):
    """Run Django database migrations."""
    print('[6/7] Running database migrations...')
    result = subprocess.run([python_cmd, 'manage.py', 'migrate', '--run-syncdb'])
    if result.returncode != 0:
        print()
        print('  ERROR: Migration failed.')
        print('  Try deleting db.sqlite3 and running setup again.')
        sys.exit(1)
    print('  > Migrations complete')


def create_superuser(python_cmd):
    """Ask if user wants to create a superuser."""
    print('[7/7] Admin account setup...')
    print()
    try:
        answer = input('  Create admin account now? (Y/N): ').strip().upper()
    except EOFError:
        answer = 'N'

    if answer == 'Y':
        subprocess.run([python_cmd, 'manage.py', 'createsuperuser'])
    else:
        print('  Skipped - run later: python manage.py createsuperuser')
    print()


def print_success():
    """Print the success message."""
    print()
    print('========================================')
    print('  Setup Complete!')
    print('========================================')
    print()
    print('Next steps:')
    print('  1. Run: run_project.bat')
    print('  2. Visit: http://127.0.0.1:8000')
    print()

    # Warn if API key is still placeholder
    current_key = get_current_api_key()
    if current_key in (None, '', 'your-gemini-api-key-here', 'YOUR_NEW_GEMINI_API_KEY_HERE'):
        print('Remember to add your API key to .env:')
        print('  GOOGLE_API_KEY=your-key-here')
        print()

    print('========================================')


def main():
    # Determine the Python command (passed as argument or auto-detect)
    if len(sys.argv) > 1:
        python_cmd = sys.argv[1]
    else:
        python_cmd = sys.executable

    create_env_file()
    print()
    prompt_api_key()
    print()
    run_migrations(python_cmd)
    print()
    create_superuser(python_cmd)
    print_success()


if __name__ == '__main__':
    main()
