#!/usr/bin/env python3
"""
Add all packages as git submodules.
"""

import json
import subprocess
import sys

def add_submodule(name, url):
    """Add a git submodule."""
    path = f"pyhc_packages/{name}"
    try:
        result = subprocess.run(
            ['git', 'submodule', 'add', url, path],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return True, None
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

def main():
    with open('package_url_mapping.json') as f:
        mapping = json.load(f)

    # Filter out duplicates (keep only the ones we actually want)
    # These are the lowercase/different-name versions we don't want
    skip_names = {'NEXRADutils', 'WMM2020', 'astrometry_azel', 'pytplot'}

    packages = [(name, url) for name, url in mapping.items() if name not in skip_names]

    print(f"Adding {len(packages)} packages as git submodules...\n")

    success_count = 0
    failed = []

    for i, (name, url) in enumerate(packages, 1):
        print(f"[{i}/{len(packages)}] Adding {name}...", end=' ')
        success, error = add_submodule(name, url)

        if success:
            print("✓")
            success_count += 1
        else:
            print(f"✗")
            failed.append((name, url, error))

    print(f"\n{'='*60}")
    print(f"Successfully added: {success_count}/{len(packages)}")

    if failed:
        print(f"\nFailed ({len(failed)}):")
        for name, url, error in failed:
            print(f"\n  {name}:")
            print(f"    URL: {url}")
            print(f"    Error: {error[:200]}")
        return 1

    print("\n✅ All submodules added successfully!")
    return 0

if __name__ == '__main__':
    exit(main())
