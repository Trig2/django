#!/usr/bin/env python
"""
Script to prepare the application for production deployment.
This collects static files and performs other production setup tasks.
"""
import os
import subprocess
import sys
from pathlib import Path

# Define paths
BASE_DIR = Path(__file__).resolve().parent
STATIC_ROOT = BASE_DIR / "ecommerce" / "staticfiles"

def collect_static_files():
    """Collect static files into STATIC_ROOT directory"""
    print("Collecting static files...")
    try:
        result = subprocess.run(
            ["python", "ecommerce/manage.py", "collectstatic", "--noinput"],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print("Static files collected successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error collecting static files: {e}")
        print(e.stderr)
        return False
    return True

def main():
    """Main function to run production setup tasks"""
    print("Setting up production environment...")
    
    # Make sure we're using production settings
    subprocess.run(["python", "toggle_debug.py", "prod"])
    
    # Collect static files
    if not collect_static_files():
        print("Failed to set up production environment.")
        return False
    
    print("\nProduction setup complete!")
    print("\nIMPORTANT: Your application is now in production mode (DEBUG=False).")
    print("To return to development mode, run:")
    print("  python toggle_debug.py dev")
    
    return True

if __name__ == "__main__":
    main()
