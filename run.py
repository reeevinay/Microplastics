#!/usr/bin/env python3
"""
Microplastic Analysis System - Startup Script
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import tensorflow
        import cv2
        import numpy
        import pandas
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', 'results', 'models', 'static/css', 'static/js', 'static/images', 'templates']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"✓ Created directory: {directory}")
        else:
            print(f"✓ Directory exists: {directory}")

def main():
    """Main startup function"""
    print("=" * 50)
    print("Microplastic Analysis System")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create directories
    print("\nChecking directories...")
    create_directories()
    
    # Start the application
    print("\nStarting the application...")
    print("Access the web interface at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\nShutting down the server...")
    except Exception as e:
        print(f"\nError starting the application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
