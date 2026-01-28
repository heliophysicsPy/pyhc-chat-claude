#!/usr/bin/env python3
"""
Extract license information from all PyHC packages
"""

import os
import re
import json
from pathlib import Path

def find_license_in_file(filepath):
    """Extract license information from a file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

            # Common license patterns
            patterns = {
                'MIT': r'MIT License',
                'BSD-3-Clause': r'BSD[- ]3[- ]Clause|3-Clause BSD|BSD 3-Clause',
                'BSD-2-Clause': r'BSD[- ]2[- ]Clause|2-Clause BSD|BSD 2-Clause|Simplified BSD',
                'Apache-2.0': r'Apache License[,\s]+Version 2\.0|Apache-2\.0',
                'GPL-3.0': r'GNU General Public License[,\s]+version 3|GPL-3|GPLv3',
                'GPL-2.0': r'GNU General Public License[,\s]+version 2|GPL-2|GPLv2',
                'LGPL': r'GNU Lesser General Public License|LGPL',
                'ISC': r'ISC License',
                'BSD': r'BSD License',
                'Public Domain': r'Public Domain',
                'Unlicense': r'Unlicense',
                'AGPL': r'GNU Affero General Public License|AGPL',
            }

            for license_type, pattern in patterns.items():
                if re.search(pattern, content, re.IGNORECASE):
                    return license_type
    except:
        pass
    return None

def get_license_from_setup_py(package_dir):
    """Extract license from setup.py"""
    setup_path = package_dir / 'setup.py'
    if setup_path.exists():
        try:
            with open(setup_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Look for license= or License= in setup()
                match = re.search(r'[Ll]icense\s*=\s*[\'"]([^\'"]+)[\'"]', content)
                if match:
                    return match.group(1).strip()
        except:
            pass
    return None

def get_license_from_pyproject_toml(package_dir):
    """Extract license from pyproject.toml"""
    pyproject_path = package_dir / 'pyproject.toml'
    if pyproject_path.exists():
        try:
            with open(pyproject_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Look for license patterns in TOML
                match = re.search(r'license\s*=\s*[{]?\s*[\'"]?(?:text|file)?\s*[\'"]?\s*[:=]?\s*[\'"]([^\'"]+)[\'"]', content, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
                # Also check for simple license = "MIT" format
                match = re.search(r'license\s*=\s*[\'"]([^\'"]+)[\'"]', content, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
        except:
            pass
    return None

def get_license_from_license_file(package_dir):
    """Find and parse LICENSE file"""
    # Look for LICENSE files in root and licenses/ subdirectory
    license_files = ['LICENSE', 'LICENSE.txt', 'LICENSE.md', 'LICENSE.rst', 'License',
                     'COPYING', 'COPYING.txt', 'license', 'license.txt', 'LICENSE.md']

    locations = [package_dir, package_dir / 'licenses']

    for location in locations:
        if not location.exists():
            continue
        for filename in license_files:
            license_path = location / filename
            if license_path.exists():
                result = find_license_in_file(license_path)
                if result:
                    return result
    return None

def extract_license_info(package_dir):
    """Extract license information from a package directory"""
    # Try different sources in order of reliability

    # 1. Check LICENSE file first (most reliable)
    license_info = get_license_from_license_file(package_dir)
    if license_info:
        return license_info

    # 2. Check pyproject.toml
    license_info = get_license_from_pyproject_toml(package_dir)
    if license_info:
        return license_info

    # 3. Check setup.py
    license_info = get_license_from_setup_py(package_dir)
    if license_info:
        return license_info

    return "Unknown"

def main():
    packages_dir = Path('/Users/shpo9723/git/pyhc-chat-claude/pyhc_packages')

    results = {}

    # Get all subdirectories
    for item in sorted(packages_dir.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            package_name = item.name
            license_info = extract_license_info(item)
            results[package_name] = license_info
            print(f"{package_name}: {license_info}")

    # Save results
    output_file = Path('/Users/shpo9723/git/pyhc-chat-claude/license_info.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {output_file}")

if __name__ == '__main__':
    main()
