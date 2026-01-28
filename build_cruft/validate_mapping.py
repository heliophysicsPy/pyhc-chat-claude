#!/usr/bin/env python3
"""
Validate package_url_mapping.json against actual git remote URLs in pyhc_packages/
"""

import json
import subprocess
from pathlib import Path

def get_git_remote_url(repo_path):
    """Get the git remote URL for a repository."""
    try:
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except Exception as e:
        return None

def normalize_url(url):
    """Normalize URL for comparison (remove .git, trailing slash, etc)."""
    if not url:
        return None
    url = url.rstrip('/')
    if url.endswith('.git'):
        url = url[:-4]
    return url

def main():
    # Load the mapping
    with open('package_url_mapping.json') as f:
        mapping = json.load(f)

    pyhc_packages_dir = Path('pyhc_packages')

    print("Validating package URLs...\n")

    mismatches = []
    matches = 0
    not_git_repos = []
    not_in_mapping = []

    # Check each directory in pyhc_packages
    for dir_path in sorted(pyhc_packages_dir.iterdir()):
        if not dir_path.is_dir():
            continue

        dir_name = dir_path.name

        # Skip .claude directory
        if dir_name.startswith('.'):
            continue

        # Get git remote URL
        git_url = get_git_remote_url(dir_path)

        if git_url is None:
            not_git_repos.append(dir_name)
            continue

        # Check if in mapping
        if dir_name not in mapping:
            not_in_mapping.append((dir_name, git_url))
            continue

        # Compare URLs
        normalized_git_url = normalize_url(git_url)
        normalized_mapped_url = normalize_url(mapping[dir_name])

        if normalized_git_url != normalized_mapped_url:
            mismatches.append({
                'name': dir_name,
                'git_url': git_url,
                'mapped_url': mapping[dir_name]
            })
        else:
            matches += 1

    # Print results
    print(f"✓ Matches: {matches}")

    if not_git_repos:
        print(f"\n⚠️  Not git repositories ({len(not_git_repos)}):")
        for name in not_git_repos:
            print(f"  - {name}")

    if not_in_mapping:
        print(f"\n⚠️  In pyhc_packages/ but not in mapping ({len(not_in_mapping)}):")
        for name, url in not_in_mapping:
            print(f"  - {name}: {url}")

    if mismatches:
        print(f"\n❌ URL Mismatches ({len(mismatches)}):")
        for item in mismatches:
            print(f"\n  {item['name']}:")
            print(f"    Git:    {item['git_url']}")
            print(f"    Mapped: {item['mapped_url']}")
        return 1

    # Check for mappings without directories
    mapped_dirs = set(mapping.keys())
    actual_dirs = set([d.name for d in pyhc_packages_dir.iterdir() if d.is_dir() and not d.name.startswith('.')])

    missing_dirs = mapped_dirs - actual_dirs
    if missing_dirs:
        print(f"\n⚠️  In mapping but not in pyhc_packages/ ({len(missing_dirs)}):")
        for name in sorted(missing_dirs):
            print(f"  - {name}: {mapping[name]}")

    if matches > 0 and not mismatches:
        print(f"\n✅ All {matches} repositories validated successfully!")
        return 0

    return 1

if __name__ == '__main__':
    exit(main())
