# Poetry Environment Guide

## Overview
This project now uses Poetry for dependency management and virtual environment isolation.

## Installed Dependencies

### Core Dependencies:
- **requests** (2.32.5) - HTTP library for web scraping
- **beautifulsoup4** (4.14.3) - HTML parsing
- **pandas** (2.3.3) - Data manipulation and analysis
- **matplotlib** (3.10.7) - Data visualization
- **ipython** (8.37.0) - Interactive Python shell

### Development Dependencies:
- **pytest** (7.4.4) - Testing framework
- **black** (23.12.1) - Code formatter
- **flake8** (6.1.0) - Code linter

## Common Commands

### Activate the virtual environment:
```bash
poetry shell
```

### Run the web scraper:
```bash
poetry run python webscraping.py
```

### Install dependencies (if cloning fresh):
```bash
poetry install
```

### Add a new dependency:
```bash
poetry add <package-name>
```

### Add a development dependency:
```bash
poetry add --group dev <package-name>
```

### Update dependencies:
```bash
poetry update
```

### Show installed packages:
```bash
poetry show
```

### Format code with Black:
```bash
poetry run black .
```

### Lint code with Flake8:
```bash
poetry run flake8 .
```

### Run tests (when you add them):
```bash
poetry run pytest
```

## Project Structure

```
webscraping-with-python/
├── config.py           # Configuration and URL building
├── scraper.py          # Web scraping logic
├── data_cleaner.py     # Data cleaning functions
├── visualizer.py       # Data visualization
├── webscraping.py      # Main entry point
├── pyproject.toml      # Poetry configuration
└── poetry.lock         # Locked dependency versions
```

## Benefits of Poetry

✅ **Isolated Environment**: Dependencies don't interfere with system Python  
✅ **Reproducible Builds**: poetry.lock ensures consistent versions  
✅ **Easy Dependency Management**: Simple commands to add/remove packages  
✅ **Development Tools**: Separate dev dependencies for testing and formatting  

## Notes

- Poetry has been installed at: `/home/dem/.local/bin/poetry`
- Virtual environment location: `~/.cache/pypoetry/virtualenvs/`
- Python version: >=3.8.1,<4.0
