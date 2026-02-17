#!/usr/bin/env python3
"""
Script to create GitHub issues from issues.json
Usage: GITHUB_TOKEN=<your-token> python create_issues.py
"""

import json
import os
import subprocess
from pathlib import Path

def load_issues():
    """Load issues from issues.json file"""
    with open('issues.json', 'r') as f:
        return json.load(f)

def create_issue(title, body, labels):
    """Create a single issue using git commands"""
    # Escape special characters for shell
    title_safe = title.replace('"', '\\"')
    body_safe = body.replace('"', '\\"').replace('\n', '\\n')
    labels_str = ','.join(labels) if labels else ''
    
    cmd = ['gh', 'issue', 'create', '--title', title, '--body', body]
    if labels:
        cmd.extend(['--label', labels_str])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✓ Created: {title}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed: {title}")
        print(f"  Error: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Error: 'gh' command not found. Please install GitHub CLI.")
        return False

def main():
    # Check for GitHub token
    if not os.getenv('GITHUB_TOKEN') and not os.getenv('GH_TOKEN'):
        print("Error: GitHub token not found!")
        print("\nPlease set your GitHub token:")
        print("  export GITHUB_TOKEN=<your-personal-access-token>")
        print("\nThen run this script again:")
        print("  python create_issues.py")
        return 1
    
    # Load issues
    try:
        issues = load_issues()
    except FileNotFoundError:
        print("Error: issues.json not found in current directory")
        return 1
    
    print(f"\nCreating {len(issues)} issues...\n")
    
    # Create each issue
    successful = 0
    for issue in issues:
        if create_issue(issue['title'], issue['body'], issue.get('labels', [])):
            successful += 1
    
    print(f"\n✓ Successfully created {successful}/{len(issues)} issues")
    return 0 if successful == len(issues) else 1

if __name__ == '__main__':
    exit(main())
