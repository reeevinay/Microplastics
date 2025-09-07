#!/usr/bin/env python3
"""
Deployment script for Microplastic Analysis System
"""

import os
import subprocess
import sys

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
    """Main deployment function"""
    print("=" * 60)
    print("Microplastic Analysis System - Deployment Setup")
    print("=" * 60)
    
    # Check if git is initialized
    if not os.path.exists('.git'):
        print("Initializing Git repository...")
        if not run_command("git init", "Git initialization"):
            print("Failed to initialize git repository")
            sys.exit(1)
    
    # Add all files to git
    print("\nAdding files to git...")
    if not run_command("git add .", "Adding files to git"):
        print("Failed to add files to git")
        sys.exit(1)
    
    # Create initial commit
    print("\nCreating initial commit...")
    if not run_command('git commit -m "Initial commit: Microplastic Analysis System"', "Creating initial commit"):
        print("Failed to create initial commit")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("DEPLOYMENT SETUP COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Create a new repository on GitHub")
    print("2. Add the remote origin:")
    print("   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git")
    print("3. Push to GitHub:")
    print("   git push -u origin main")
    print("\nFor team members to use:")
    print("1. Clone the repository:")
    print("   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git")
    print("2. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("3. Run the application:")
    print("   python app.py")

if __name__ == "__main__":
    main()
