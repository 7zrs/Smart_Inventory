#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess
from django.core.management import execute_from_command_line
from django.utils.autoreload import run_with_reloader

def start_streamlit():
    """Start the Streamlit app in a separate subprocess."""
    streamlit_script = "Streamlit_app.py"  
    try:
        print("Starting Streamlit server...")
        subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", streamlit_script],
            env={**os.environ, "STREAMLIT_SERVER_HEADLESS": "true"}  # Suppress welcome message
        )
    except Exception as e:
        print(f"Failed to start Streamlit: {e}")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Smart_Inventory.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    # Start Streamlit only if running the development server and not in the reloader process
    if len(sys.argv) > 1 and sys.argv[1] == "runserver":
        if os.environ.get("RUN_MAIN") == "true":  # Check if this is the main process
            start_streamlit()
    main()