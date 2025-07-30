#!/usr/bin/env python3
"""
GitHub deployment automation script for Python to C# Translator
"""

import os
import subprocess
import sys
from pathlib import Path

def ensure_git_available():
    """Ensure Git is available in PATH, add common installation paths if needed."""
    # First check if git is already available
    result = subprocess.run(["git", "--version"], capture_output=True, text=True)
    if result.returncode == 0:
        return True
    
    # Common Git installation paths on Windows
    git_paths = [
        r"C:\Program Files\Git\bin",
        r"C:\Program Files (x86)\Git\bin",
        r"C:\Users\%USERNAME%\AppData\Local\Programs\Git\bin"
    ]
    
    for git_path in git_paths:
        expanded_path = os.path.expandvars(git_path)
        git_exe = os.path.join(expanded_path, "git.exe")
        if os.path.exists(git_exe):
            # Add to PATH for this session
            current_path = os.environ.get("PATH", "")
            if expanded_path not in current_path:
                os.environ["PATH"] = current_path + os.pathsep + expanded_path
                print(f"✅ Added Git to PATH: {expanded_path}")
            return True
    
    print("❌ Git not found. Please install Git from https://git-scm.com/download/win")
    return False

def run_command(cmd, check=True):
    """Run a shell command and return the result."""
    print(f"🔄 Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if check and result.returncode != 0:
        print(f"❌ Error running command: {cmd}")
        print(f"Error: {result.stderr}")
        return False
    
    if result.stdout:
        print(f"✅ Output: {result.stdout.strip()}")
    
    return True

def check_git_installed():
    """Check if git is installed."""
    return run_command("git --version", check=False)

def check_project_files():
    """Check if all required project files exist."""
    required_files = [
        "py_to_cs_agent.py",
        "test_input.py", 
        "README_GITHUB.md",
        "LICENSE",
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        ".gitignore"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required project files found")
    return True

def initialize_git_repo(commit_message=None):
    """Initialize git repository and add files."""
    if Path(".git").exists():
        print("📁 Git repository already exists")
        return True
    
    if commit_message is None:
        commit_message = """Initial release: Python to C# translator v1.0.0

- AST-based translation with visitor pattern
- Support for classes, functions, control flow
- LINQ integration for comprehensions
- Exception handling and type mapping
- CLI interface with file I/O
- Comprehensive documentation"""
    
    commands = [
        "git init",
        "git add .",
        f'git commit -m "{commit_message}"'
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            return False
    
    return True

def setup_github_remote(username=None, repo_name=None):
    """Set up GitHub remote repository."""
    if username is None:
        username = input("🔧 Enter your GitHub username: ").strip()
        if not username:
            print("❌ GitHub username is required")
            return False
    
    if repo_name is None:
        repo_name = "python-to-csharp-translator"
    
    remote_url = f"https://github.com/{username}/{repo_name}.git"
    
    # Check if remote origin already exists and handle accordingly
    print("🔄 Checking for existing Git remote...")
    result = subprocess.run(["git", "remote", "get-url", "origin"], 
                          capture_output=True, text=True, cwd=".")
    
    if result.returncode == 0:
        # Remote exists, update it
        print("📝 Updating existing remote origin...")
        if not run_command(f"git remote set-url origin {remote_url}"):
            return False
    else:
        # Remote doesn't exist, add it
        print("➕ Adding new remote origin...")
        if not run_command(f"git remote add origin {remote_url}"):
            return False
    
    # Set main branch
    if not run_command("git branch -M main"):
        return False
    
    print(f"✅ GitHub remote configured: {remote_url}")
    return True

def push_to_github():
    """Push code to GitHub."""
    print("🚀 Pushing to GitHub...")
    
    # First check if there are any commits
    result = subprocess.run(["git", "log", "--oneline"], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ No commits found. Creating initial commit...")
        
        # Ensure we have files to commit
        if not run_command("git add ."):
            return False
        
        # Check if there are files staged
        result_status = subprocess.run(["git", "status", "--porcelain", "--cached"], 
                                     capture_output=True, text=True)
        if not result_status.stdout.strip():
            print("❌ No files to commit. Make sure project files exist.")
            return False
        
        # Create initial commit
        if not run_command('git commit -m "Initial commit: Python to C# translator"'):
            return False
    
    # Ensure we're on main branch
    if not run_command("git branch -M main"):
        return False
    
    # Now push
    return run_command("git push -u origin main")

def update_readme_urls(username, repo_name="python-to-csharp-translator"):
    """Update GitHub URLs in README with actual username."""
    readme_path = Path("README_GITHUB.md")
    
    if not readme_path.exists():
        print("❌ README_GITHUB.md not found")
        return False
    
    # Read and update content
    content = readme_path.read_text(encoding='utf-8')
    updated_content = content.replace('yourusername', username)
    updated_content = updated_content.replace('python-to-csharp-translator', repo_name)
    
    # Write to README.md
    readme_final = Path("README.md")
    readme_final.write_text(updated_content, encoding='utf-8')
    
    # Remove old file and commit changes
    commands = [
        "git add README.md",
        "git rm README_GITHUB.md",
        f'git commit -m "docs: update GitHub URLs for user {username}"',
        "git push"
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            return False
    
    print("✅ README updated with correct GitHub URLs")
    return True

def print_next_steps(username, repo_name="python-to-csharp-translator"):
    """Print manual steps user needs to complete."""
    repo_url = f"https://github.com/{username}/{repo_name}"
    
    print("\n" + "="*60)
    print("🎉 DEPLOYMENT SUCCESSFUL!")
    print("="*60)
    print(f"\n📍 Your repository: {repo_url}")
    print("\n📋 NEXT STEPS:")
    print("\n1. 🌐 Visit your repository on GitHub")
    print("2. ⚙️  Click the gear icon next to 'About'")
    print("3. 📝 Add description: '🔄 Automatic Python to C# code translator using AST parsing'")
    print("4. 🏷️  Add topics: python, csharp, translator, ast, code-conversion, cli-tool")
    print("5. 🎁 Create a release (v1.0.0) with the changelog")
    print("6. 📚 Enable GitHub Pages if desired")
    print("7. 💬 Enable Discussions for community Q&A")
    print("\n🎯 OPTIONAL:")
    print("- Star your own repository")
    print("- Share on social media")
    print("- Submit to awesome lists")
    print("- Write a blog post")
    print(f"\n🔗 Direct link: {repo_url}")
    print("\n" + "="*60)

def main():
    """Main deployment function."""
    print("🚀 Python to C# Translator - GitHub Deployment Script")
    print("="*55)
    
    # Get user preferences
    print("\n📋 DEPLOYMENT CONFIGURATION")
    print("-" * 30)
    
    # Ask for GitHub username
    while True:
        username = input("🔧 Enter your GitHub username: ").strip()
        if username:
            break
        print("❌ GitHub username is required!")
    
    # Ask for repository name with default
    default_repo = "python-to-csharp-translator"
    repo_input = input(f"📁 Repository name (default: {default_repo}): ").strip()
    repo_name = repo_input if repo_input else default_repo
    
    # Ask if they want to create the GitHub repo now
    print(f"\n🌐 Repository URL will be: https://github.com/{username}/{repo_name}")
    create_repo = input("❓ Have you created this repository on GitHub yet? (y/n): ").strip().lower()
    
    if create_repo not in ['y', 'yes']:
        print(f"\n📝 Please create the repository first:")
        print(f"   1. Go to https://github.com/new")
        print(f"   2. Repository name: {repo_name}")
        print(f"   3. Make it public")
        print(f"   4. Don't initialize with README, .gitignore, or license")
        print(f"   5. Click 'Create repository'")
        
        input("\n⏳ Press Enter after creating the repository...")
    
    # Ask about commit message customization
    default_commit = """Initial release: Python to C# translator v1.0.0

- AST-based translation with visitor pattern
- Support for classes, functions, control flow
- LINQ integration for comprehensions
- Exception handling and type mapping
- CLI interface with file I/O
- Comprehensive documentation"""
    
    print(f"\n📝 Default commit message:")
    print(f"   {default_commit.split()[0]} {default_commit.split()[1]} {' '.join(default_commit.split()[2:6])}")
    custom_commit = input("📝 Use custom commit message? (y/n): ").strip().lower()
    
    if custom_commit in ['y', 'yes']:
        print("✏️  Enter your commit message (press Enter twice to finish):")
        commit_lines = []
        while True:
            line = input()
            if line == "" and commit_lines:
                break
            commit_lines.append(line)
        commit_message = "\n".join(commit_lines)
    else:
        commit_message = default_commit
    
    # Ask about automatic README updates
    auto_readme = input("\n🔄 Automatically update README URLs with your username? (y/n): ").strip().lower()
    update_readme = auto_readme in ['y', 'yes']
    
    # Show configuration summary
    print(f"\n📊 DEPLOYMENT SUMMARY")
    print("-" * 25)
    print(f"👤 GitHub Username: {username}")
    print(f"📁 Repository Name: {repo_name}")
    print(f"🔄 Update README: {'Yes' if update_readme else 'No'}")
    print(f"📝 Custom Commit: {'Yes' if custom_commit in ['y', 'yes'] else 'No'}")
    
    confirm = input(f"\n✅ Proceed with deployment? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("❌ Deployment cancelled by user")
        sys.exit(0)
    
    print(f"\n🚀 Starting deployment...")
    
    # Check prerequisites
    if not ensure_git_available():
        print("❌ Git is not available. Please install Git first.")
        sys.exit(1)
    
    if not check_project_files():
        print("❌ Missing required project files. Please ensure all files are present.")
        sys.exit(1)
    
    # Initialize repository
    if not initialize_git_repo(commit_message):
        print("❌ Failed to initialize Git repository")
        sys.exit(1)
    
    # Set up GitHub remote
    if not setup_github_remote(username, repo_name):
        print("❌ Failed to set up GitHub remote")
        sys.exit(1)
    
    # Push to GitHub
    if not push_to_github():
        print("❌ Failed to push to GitHub")
        print("💡 Possible issues:")
        print(f"   - Repository doesn't exist: https://github.com/{username}/{repo_name}")
        print(f"   - Check your GitHub credentials")
        print(f"   - Repository might not be empty")
        sys.exit(1)
    
    # Update README with correct URLs
    if update_readme:
        if not update_readme_urls(username, repo_name):
            print("⚠️  Failed to update README URLs (non-critical)")
    
    # Show next steps
    print_next_steps(username, repo_name)

if __name__ == "__main__":
    main()
