
import os
import sys
import subprocess

GIT_PATH = r"C:\Program Files\Git\bin\git.exe"
REPO_URL = "https://github.com/vikasredd057-create/swiftride.git"

def run_git_cmd(argst):
    full_cmd = [GIT_PATH] + argst
    print(f"Running: {' '.join(full_cmd)}")
    try:
        result = subprocess.run(
            full_cmd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}")
        print(f"Output: {e.output}")
        print(f"Stderr: {e.stderr}")
        return False

def main():
    print("Initializing Git Push Process...")
    
    if not os.path.exists(GIT_PATH):
        print(f"Error: Git executable not found at {GIT_PATH}")
        return

    # 1. Initialize if needed
    if not os.path.exists(".git"):
        print("Initializing repository...")
        run_git_cmd(["init"])
    
    # 2. Check remote
    remote_check = subprocess.run([GIT_PATH, "remote", "-v"], capture_output=True, text=True)
    if REPO_URL not in remote_check.stdout:
        print("Configuring remote...")
        # Remove existing if any (simplest way to ensure correct URL)
        if "origin" in remote_check.stdout:
            run_git_cmd(["remote", "remove", "origin"])
        run_git_cmd(["remote", "add", "origin", REPO_URL])
    else:
        print("Remote already configured.")

    # 3. Add files
    print("Adding files...")
    run_git_cmd(["add", "."])
    
    # 4. Commit
    print("Committing changes...")
    # We might fail if nothing to commit, which is fine
    run_git_cmd(["commit", "-m", "Feature: Multi-port Gateway System for User and Driver Dashboards"])
    
    # 5. Push
    print("Pushing to remote...")
    success = run_git_cmd(["push", "-u", "origin", "main"])
    
    if not success:
        print("\nStandard push failed. Remote might be ahead.")
        print("Attempting to pull --rebase...")
        pull_success = run_git_cmd(["pull", "origin", "main", "--rebase"])
        
        if pull_success:
            print("Rebase successful. Pushing again...")
            run_git_cmd(["push", "-u", "origin", "main"])
        else:
            print("Rebase failed. This might be a fresh repo/conflict.")
            # Optional: Force push if you are sure. 
            # For this user context "push code to repository" usually implies "update remote to match local".
            # I won't force push automatically unless I know it's safe, but I will try to handle the 'non-fast-forward' specifically.
            print("Trying push with force-with-lease...")
            run_git_cmd(["push", "-u", "origin", "main", "--force-with-lease"])

if __name__ == "__main__":
    main()
