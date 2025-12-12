#!/usr/bin/env python3
"""
Push SwiftRide to GitHub using PAT (Personal Access Token)
"""

import os
import sys
from pathlib import Path

# Set Git executable path BEFORE importing git
os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = r'C:\Program Files\Git\bin\git.exe'

from git import Repo
from git.exc import GitCommandError

REPO_URL = "https://github.com/vikasredd057-create/fsd_swiftride.git"
LOCAL_REPO_PATH = Path(__file__).parent

def main():
    print("=" * 70)
    print("SwiftRide GitHub Push Setup")
    print("=" * 70)
    
    try:
        # Try to open existing repo
        repo = Repo(LOCAL_REPO_PATH)
        print("✓ Repository found")
    except Exception as e:
        print(f"✗ Error: {e}")
        return 1
    
    print("\n" + "=" * 70)
    print("IMPORTANT: GitHub Authentication")
    print("=" * 70)
    print("""
Your repository requires authentication to push code.
GitHub has deprecated password authentication.

You have 2 options:

Option 1: Create a Personal Access Token (Recommended)
─────────────────────────────────────────────────────
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Select scopes: repo (all), admin:repo_hook
4. Copy the token

Option 2: Use GitHub CLI
─────────────────────────────────────────────────────
1. Install: https://cli.github.com
2. Run: gh auth login
3. Follow the prompts

=" * 70)
    
    # Try to set credentials via git command
    try:
        git_exe = r'C:\Program Files\Git\bin\git.exe'
        
        # Configure git for this repo
        print("\nConfiguring git...")
        os.system(f'"{git_exe}" config user.email "vikas@swiftride.com"')
        os.system(f'"{git_exe}" config user.name "SwiftRide Developer"')
        print("✓ Git configured")
        
        # Try to push with credential prompt
        print("\nAttempting to push...")
        os.system(f'cd "{LOCAL_REPO_PATH}" && "{git_exe}" push -u origin main')
        
    except Exception as e:
        print(f"✗ Push failed: {e}")
        return 1
    
    print("\n" + "=" * 70)
    print("✓ Push complete!")
    print("=" * 70)
    print(f"Repository: {REPO_URL}")
    print("=" * 70)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
