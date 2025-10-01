# PyHC-Chat-Claude

A specialized Claude Code environment for answering questions about the Python in Heliophysics Community (PyHC) and its 96+ Python packages.

## Overview

This repository provides a ready-to-use Claude Code setup that can answer questions about:
- The PyHC organization and community
- Any of the 96+ PyHC Python packages
- Package implementation details, usage, and code structure
- Cross-package comparisons and recommendations

The key insight: Claude Code is excellent at navigating code repositories to answer questions. This repo houses all PyHC package repos as git submodules, allowing Claude to autonomously search through them to answer your questions.

## Quick Start

### Prerequisites
- [Claude Code](https://claude.ai/code) installed
- Git 2.13+ (for submodule support)

### Clone the Repository

**Important:** You must clone with the `--recursive` flag to download all PyHC packages:

```bash
git clone --recursive https://github.com/heliophysicsPy/pyhc-chat-claude.git
cd pyhc-chat-claude
```

**Or**, if you already cloned without `--recursive`:

```bash
git clone https://github.com/heliophysicsPy/pyhc-chat-claude.git
cd pyhc-chat-claude
git submodule update --init --recursive
```

This will download all 96 PyHC package repositories (~several GB).

### Start Chatting

```bash
claude
```

Then ask questions like:
- "How does SunPy handle FITS file coordinate transformations?"
- "Which PyHC packages support CDF file reading?"
- "Show me how pysat handles time series data"
- "What's the difference between aacgmv2 and apexpy?"

## Repository Structure

```
pyhc-chat-claude/
├── pyhc_packages/          # All 96 PyHC packages as git submodules
│   ├── heliophysicsPy.github.io/  # PyHC website (contains metadata)
│   └── ...                 # 95 more packages
├── CLAUDE.md               # Instructions for Claude Code
└── .github/workflows/      # Automated package updates
    └── update-submodules.yml
```

## Keeping Packages Updated

This repository automatically updates all PyHC packages nightly via GitHub Actions. The workflow:
1. Runs daily at midnight UTC
2. Updates all submodules to their latest commits
3. Commits and pushes if any packages changed

You can also manually trigger updates from the Actions tab on GitHub.

To update locally:

```bash
git pull
git submodule update --remote --merge
```

## Included Packages

96 PyHC packages including:

**Core Packages:**
- sunpy, spacepy, pysat, PlasmaPy, pyspedas, Kamodo

**Standards & Documentation:**
- heliophysicsPy.github.io (PyHC website)
- standards, pyhc-docs

**And 89+ specialized packages** for solar physics, magnetosphere science, ionosphere/thermosphere research, data access, visualization, and more.

See `pyhc_packages/heliophysicsPy.github.io/_data/` for complete package metadata.

## How It Works

1. **Git Submodules**: Each PyHC package is a git submodule pointing to its official repository
2. **Full Git History**: Claude Code can access the complete development history of each package
3. **Automated Updates**: GitHub Actions keeps all packages synchronized with their upstream repos
4. **CLAUDE.md**: Specialized instructions that guide Claude on how to search packages, cite sources, and acknowledge limitations when answering PyHC questions

## Contributing

This is an experiment in AI-assisted PyHC support. Contributions welcome:
- Add missing PyHC packages
- Improve CLAUDE.md instructions
- Report issues with Claude's answers
- Share interesting use cases

## Notes

- First clone will take several minutes and ~several GB of disk space
- Claude Code requires an active subscription
- This is a community tool, not an official PyHC project
- For authoritative answers, always consult official package documentation

## License

This repository structure is provided as-is. Individual packages retain their original licenses.
