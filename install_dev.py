#!/usr/bin/env python3
"""
Development installation script for Dexter Toolkit
"""

import subprocess
import sys
import os

def install_dev():
    """Install Dexter Toolkit in development mode"""
    print("Installing Dexter Toolkit in development mode...")
    
    # Install in editable mode
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-e", "."
    ])
    
    # Install development dependencies
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-e", ".[dev]"
    ])
    
    print("✅ Dexter Toolkit installed successfully!")
    print("\nYou can now import dexter:")
    print(">>> import dexter")
    print(">>> from dexter import pick_classifier, Problem, SimManager")

if __name__ == "__main__":
    install_dev()
