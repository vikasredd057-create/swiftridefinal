#!/usr/bin/env python3
"""
Script to push SwiftRide project to GitHub
"""

import os
import sys
from pathlib import Path

# Set Git executable BEFORE importing git
os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = r'C:\Program Files\Git\bin\git.exe'

import git
from git import Repo
from git.exc import InvalidGitRepositoryError, GitCommandError

# Configuration
REPO_URL = "https://github.com/vikasredd057-create/fsd_swiftride.git"
LOCAL_REPO_PATH = Path(__file__).parent
BRANCH_NAME = "main"

def initialize_repo():
    """Initialize Git repository if not already initialized"""
    try:
        repo = Repo(LOCAL_REPO_PATH)
        print("✓ Git repository already initialized")
        return repo
    except InvalidGitRepositoryError:
        print("Initializing new Git repository...")
        repo = Repo.init(LOCAL_REPO_PATH)
        print("✓ Git repository initialized")
        return repo

def setup_remote(repo):
    """Setup or update remote origin"""
    try:
        remote = repo.remote("origin")
        print(f"✓ Remote 'origin' already configured: {remote.url}")
        # Update URL if different
        if remote.url != REPO_URL:
            remote.set_url(REPO_URL)
            print(f"✓ Updated remote URL to: {REPO_URL}")
    except (ValueError, IndexError):
        # Remote doesn't exist, create it
        print(f"Adding remote origin: {REPO_URL}")
        remote = repo.create_remote("origin", REPO_URL)
        print(f"✓ Remote 'origin' configured: {REPO_URL}")
    
    return repo.remote("origin")

def stage_all_files(repo):
    """Stage all files for commit"""
    print("\nStaging files...")
    try:
        repo.git.add(A=True)
        print("✓ All files staged")
    except GitCommandError as e:
        print(f"✗ Error staging files: {e}")
        raise

def create_commit(repo):
    """Create initial commit if needed"""
    print("\nChecking commit history...")
    
    try:
        # Check if there are any commits
        commits = list(repo.iter_commits())
        if commits:
            print(f"✓ Repository has {len(commits)} existing commits")
            return False
        else:
            print("No commits found, creating initial commit...")
            repo.index.commit("Initial commit: SwiftRide project setup")
            print("✓ Initial commit created")
            return True
    except (GitCommandError, ValueError):
        print("Creating initial commit...")
        repo.index.commit("Initial commit: SwiftRide project setup")
        print("✓ Initial commit created")
        return True

def push_to_github(repo):
    """Push commits to GitHub"""
    print(f"\nPushing to GitHub (branch: {BRANCH_NAME})...")
    
    try:
        remote = repo.remote("origin")
        # Try to push, forcing if needed
        push_info = remote.push(BRANCH_NAME, force=True)
        
        for push_result in push_info:
            if push_result.flags & push_result.ERROR:
                print(f"✗ Push error: {push_result.summary}")
                return False
            else:
                print(f"✓ {push_result.summary}")
        
        print("✓ Successfully pushed to GitHub!")
        return True
        
    except GitCommandError as e:
        print(f"✗ Git error during push: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def main():
    """Main execution function"""
    print("=" * 60)
    print("SwiftRide GitHub Push Script")
    print("=" * 60)
    print(f"Repository URL: {REPO_URL}")
    print(f"Local Path: {LOCAL_REPO_PATH}")
    print("=" * 60)
    
    try:
        # Step 1: Initialize repo
        repo = initialize_repo()
        
        # Step 2: Setup remote
        setup_remote(repo)
        
        # Step 3: Stage files
        stage_all_files(repo)
        
        # Step 4: Create commit
        create_commit(repo)
        
        # Step 5: Push to GitHub
        success = push_to_github(repo)
        
        print("\n" + "=" * 60)
        if success:
            print("✓ PUSH SUCCESSFUL!")
            print(f"Your code is now at: {REPO_URL}")
            print("=" * 60)
            return 0
        else:
            print("✗ PUSH FAILED!")
            print("Please check your GitHub credentials and repository URL.")
            print("=" * 60)
            return 1
            
    except Exception as e:
        print(f"\n✗ Critical error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
