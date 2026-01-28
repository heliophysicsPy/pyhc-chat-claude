#!/usr/bin/env python3
"""
Extract package URLs from PyHC YAML files and create a mapping.
"""

import yaml
import json
from pathlib import Path

def extract_repo_name(url):
    """Extract repository name from GitHub/GitLab URL."""
    # Handle special case: URLs with /tree/branch or /tree/main
    if '/tree/' in url:
        url = url.split('/tree/')[0]

    # Remove trailing slash
    url = url.rstrip('/')

    # Remove .git suffix if present
    if url.endswith('.git'):
        url = url[:-4]

    # Get the last part of the URL path
    return url.split('/')[-1]

def main():
    yaml_files = [
        'pyhc_packages/heliophysicsPy.github.io/_data/projects_core.yml',
        'pyhc_packages/heliophysicsPy.github.io/_data/projects.yml',
        'pyhc_packages/heliophysicsPy.github.io/_data/projects_unevaluated.yml'
    ]

    # Add the four generic PyHC repos
    mapping = {
        'heliophysicsPy.github.io': 'https://github.com/heliophysicsPy/heliophysicsPy.github.io',
        'standards': 'https://github.com/heliophysicsPy/standards',
        'pyhc-docker-environment': 'https://github.com/heliophysicsPy/pyhc-docker-environment',
        'pyhc-docs': 'https://github.com/heliophysicsPy/pyhc-docs'
    }

    for yaml_file in yaml_files:
        with open(yaml_file, 'r') as f:
            projects = yaml.safe_load(f)

        for project in projects:
            if 'code' in project:
                url = project['code']
                # Extract the repo name from the URL
                repo_name = extract_repo_name(url)
                if repo_name in mapping and mapping[repo_name] != url:
                    print(f"⚠️  Duplicate: {repo_name} maps to both {mapping[repo_name]} and {url}")
                mapping[repo_name] = url

    # Manual corrections for repos where directory name differs from URL-extracted name
    # or where YAML data is incorrect (these override YAML data)
    manual_mappings = {
        'NEXRAD': 'https://github.com/space-physics/NEXRAD',
        'astrometry_geomap': 'https://github.com/space-physics/astrometry_geomap',
        'PyTplot': 'https://github.com/MAVENSDC/PyTplot',  # Correct case
        'wmm2020': 'https://github.com/space-physics/wmm2020',
        'EUVpy': 'https://github.com/DanBrandt/EUVpy',  # Remove /tree/main
        'ccsdspy': 'https://github.com/CCSDSPy/ccsdspy',  # Correct case
        'madrigalWeb': 'https://github.com/MITHaystack/madrigalWeb',  # Correct repo, not PyPI
        'pysatCDF': 'https://github.com/pysat/pysatCDF'  # Correct org
    }
    mapping.update(manual_mappings)

    # Write mapping to JSON file
    with open('package_url_mapping.json', 'w') as f:
        json.dump(mapping, f, indent=2)

    print(f"Found {len(mapping)} packages")
    print("\nPackages:")
    for repo_name, url in sorted(mapping.items()):
        print(f"  {repo_name}: {url}")

    # Check for directories that don't have URLs
    existing_dirs = set([d.name for d in Path('pyhc_packages').iterdir() if d.is_dir()])
    mapped_dirs = set(mapping.keys())

    missing_urls = existing_dirs - mapped_dirs
    if missing_urls:
        print(f"\n⚠️  Warning: {len(missing_urls)} directories without URLs:")
        for d in sorted(missing_urls):
            print(f"  - {d}")

    extra_urls = mapped_dirs - existing_dirs
    if extra_urls:
        print(f"\n⚠️  Warning: {len(extra_urls)} URLs without directories:")
        for d in sorted(extra_urls):
            print(f"  - {d}")

if __name__ == '__main__':
    main()
