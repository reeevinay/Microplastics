#!/usr/bin/env python3
"""
Setup script for Microplastic Analysis System
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("=" * 60)
    print("Microplastic Analysis System - Setup")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        sys.exit(1)
    else:
        print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    print("\nInstalling dependencies...")
    if not run_command("pip install -r requirements.txt", "Installing Python packages"):
        print("Failed to install dependencies. Please check your Python environment.")
        sys.exit(1)
    
    # Create necessary directories
    print("\nCreating directories...")
    directories = [
        'uploads', 'results', 'models', 
        'static/css', 'static/js', 'static/images', 'templates'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"✓ Created: {directory}")
        else:
            print(f"✓ Exists: {directory}")
    
    # Test the system
    print("\nTesting the system...")
    if run_command("python demo.py", "Running demo test"):
        print("\n" + "="*60)
        print("SETUP COMPLETE!")
        print("="*60)
        print("\nTo start the application:")
        print("  python app.py")
        print("\nOr use the startup script:")
        print("  python run.py")
        print("\nThen open your browser to:")
        print("  http://localhost:5000")
        print("\nFor help, see README.md")
    else:
        print("\nSetup completed with warnings. The system may still work.")
        print("Try running: python app.py")

if __name__ == "__main__":
    main()
