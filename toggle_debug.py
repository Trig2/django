#!/usr/bin/env python
"""
Script to toggle between development and production settings.
This temporarily renames the local_settings.py file to make Django use
either development (DEBUG=True) or production (DEBUG=False) settings.
"""
import os
import sys
import shutil
from pathlib import Path

# Define paths
BASE_DIR = Path(__file__).resolve().parent
LOCAL_SETTINGS = BASE_DIR / "ecommerce" / "ecommerce" / "local_settings.py"
LOCAL_SETTINGS_BACKUP = BASE_DIR / "ecommerce" / "ecommerce" / "local_settings.py.bak"

def enable_production():
    """Temporarily disable local_settings.py to use production settings"""
    if LOCAL_SETTINGS.exists():
        print("Enabling production mode (DEBUG=False)")
        # Rename local_settings.py to local_settings.py.bak
        shutil.move(LOCAL_SETTINGS, LOCAL_SETTINGS_BACKUP)
        print("Local settings temporarily disabled. Django will use production settings.")
        print("Run 'python toggle_debug.py dev' to restore development settings.")
    else:
        print("Already in production mode (DEBUG=False)")

def enable_development():
    """Re-enable local_settings.py to use development settings"""
    if LOCAL_SETTINGS_BACKUP.exists():
        print("Enabling development mode (DEBUG=True)")
        # Restore local_settings.py from backup
        shutil.move(LOCAL_SETTINGS_BACKUP, LOCAL_SETTINGS)
        print("Local settings restored. Django will use development settings.")
    else:
        print("No backup found. Creating new local_settings.py with DEBUG=True")
        with open(LOCAL_SETTINGS, 'w') as f:
            f.write("""\"\"\"
Local development settings for ecommerce project.
These settings override the production settings in settings.py
when running locally.
\"\"\"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow all hosts in development
ALLOWED_HOSTS = ['*']

# Email backend for development (prints to console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
""")
        print("Development settings created.")

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) < 2 or sys.argv[1] not in ['prod', 'dev']:
        print("Usage: python toggle_debug.py [prod|dev]")
        print("  - 'prod': Enable production settings (DEBUG=False)")
        print("  - 'dev': Enable development settings (DEBUG=True)")
        return

    mode = sys.argv[1]
    if mode == 'prod':
        enable_production()
    else:
        enable_development()

if __name__ == "__main__":
    main()
