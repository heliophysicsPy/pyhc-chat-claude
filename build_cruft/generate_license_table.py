#!/usr/bin/env python3
"""
Generate a formatted license table for PyHC packages
"""

import json
from collections import Counter

# Manual corrections for packages that couldn't be auto-detected
MANUAL_CORRECTIONS = {
    'aiapy': 'BSD-2-Clause',
    'asilib': 'BSD-3-Clause',
    'ccsdspy': 'BSD-3-Clause',
    'client-python': 'MIT',  # HAPI Client
    'fiasco': 'BSD-3-Clause',
    'fisspy': 'BSD-2-Clause',
    'hermes_core': 'Apache-2.0',
    'irispy-lmsal': 'BSD-2-Clause',
    'kaipy': 'BSD-3-Clause',
    'ndcube': 'BSD-2-Clause',
    'ocbpy': 'BSD-3-Clause',
    'pysat': 'BSD-3-Clause',
    'sunkit-image': 'BSD-2-Clause',
    'sunkit-instruments': 'BSD-2-Clause',
    'sunpy': 'BSD-2-Clause',
    'sunraster': 'BSD-2-Clause',
    'themisasi': 'MIT',
    'Kamodo': 'NASA Open Source Agreement',
    'PyGS': 'BSD-3-Clause',
    'SAVIC': 'MIT',
    'TomograPy': 'MIT',
    'astrometry_geomap': 'MIT',
    'dbprocessing': 'BSD-3-Clause',
    'mcalf': 'BSD-2-Clause',
    'pyhc-docker-environment': 'MIT',
    'pymap3d': 'BSD-2-Clause',
    'pysatCDF': 'BSD-3-Clause',
    'sami2py': 'BSD-3-Clause',
    'scanning-doppler-interferometer': 'MIT',
    'solo-epd-loader': 'BSD-3-Clause',
    'standards': 'N/A',
    'enlilviz': 'MIT',
    'regularizepsf': 'MIT',
    'spacepy': 'PSF',  # Python Software Foundation License
}

# Map package directory names to display names
PACKAGE_NAME_MAP = {
    'client-python': 'HAPI Client',
    'heliophysicsPy.github.io': 'PyHC Website',
    'pyhc-docker-environment': 'PyHC Docker Environment',
    'pyhc-docs': 'PyHC Docs',
    'standards': 'PyHC Standards',
    'ACE_magnetometer': 'ACEmag',
    'AEindex': 'Auroral Electrojet Index',
    'CDFpp': 'PyCDFpp',
    'LOFAR-Sun-tools': 'lofarSun',
    'NCAR-GLOW': 'GLOW',
    'NEXRAD': 'NEXRADutils',
    'GeoDataPython': 'geodata',
    'GOESplot': 'GOESutils',
    'VirES-Python-Client': 'viresclient',
    'astrometry_geomap': 'AstrometryAzEl',
    'dascasi': 'DASCutils',
    'digital-meridian-spectrometer': 'Digital Meridian Spectrometer',
    'gima-magnetometer': 'GIMAmag',
    'georinex': 'GEOrinex',
    'geospacelab': 'GeospaceLAB',
    'hermes_core': 'HERMES-Core',
    'irfu-python': 'PyRFU',
    'madrigalWeb': 'MadrigalWeb',
    'mgs-radio': 'MGSutils',
    'pyaurorax': 'PyAuroraX',
    'pyzenodo3': 'PyZenodo',
    'reesaurora': 'ReesAurora',
    'scanning-doppler-interferometer': 'Scanning Doppler Interferometer',
    'sciencedates': 'ScienceDates',
    'themisasi': 'THEMISasi',
    'space_packet_parser': 'space-packet-parser',
    'wmm2020': 'WMM2020',
}

def normalize_license_name(license_str):
    """Normalize license names to standard format"""
    if not license_str or license_str == 'Unknown':
        return license_str

    # Normalize common variations
    license_map = {
        'BSD 3-Clause': 'BSD-3-Clause',
        'BSD-3-Clause License': 'BSD-3-Clause',
        'BSD 3-Clause License': 'BSD-3-Clause',
        'BSD-3': 'BSD-3-Clause',
        'BSD-2': 'BSD-2-Clause',
        'BSD': 'BSD (unspecified)',
        'MIT License': 'MIT',
        'Apache License 2.0': 'Apache-2.0',
        'Apache 2.0': 'Apache-2.0',
        'GPL-2': 'GPL-2.0',
        'GPL-3': 'GPL-3.0',
    }

    return license_map.get(license_str, license_str)

def main():
    # Load the extracted license info
    with open('license_info.json', 'r') as f:
        licenses = json.load(f)

    # Apply manual corrections
    for pkg, lic in MANUAL_CORRECTIONS.items():
        if pkg in licenses:
            licenses[pkg] = lic

    # Normalize all license names
    normalized = {}
    for pkg, lic in licenses.items():
        normalized[pkg] = normalize_license_name(lic)

    # Get display names
    display_names = {}
    for pkg in normalized.keys():
        display_names[pkg] = PACKAGE_NAME_MAP.get(pkg, pkg)

    # Sort by display name
    sorted_packages = sorted(normalized.items(), key=lambda x: display_names[x[0]].lower())

    # Generate markdown table
    print("# PyHC Package Licenses\n")
    print("| Package | License |")
    print("|---------|---------|")

    for pkg, lic in sorted_packages:
        display_name = display_names[pkg]
        print(f"| {display_name} | {lic} |")

    # Generate summary statistics
    print("\n## License Summary\n")

    # Count licenses
    license_counts = Counter(normalized.values())

    print("| License | Count |")
    print("|---------|-------|")
    for lic, count in sorted(license_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"| {lic} | {count} |")

    print(f"\n**Total Packages:** {len(normalized)}")

if __name__ == '__main__':
    main()
