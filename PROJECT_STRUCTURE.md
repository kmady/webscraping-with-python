# Project Structure

This document describes the organization of the webscraping-with-python project.

## Directory Layout

```
webscraping-with-python/
├── src/                    # Source code files
│   ├── __init__.py        # Package initialization
│   ├── config.py          # Configuration settings
│   ├── scraper.py         # Web scraping logic
│   ├── data_cleaner.py    # Data cleaning utilities
│   ├── visualizer.py      # Data visualization tools
│   └── webscraping.py     # Main scraping script
│
├── data/                   # Data files (CSV outputs)
│   ├── laptops_rating.csv
│   └── laptops_rating2019.csv
│
├── notebooks/              # Jupyter notebooks
│   └── LaptopsData.ipynb  # Tutorial notebook for beginners
│
├── docs/                   # Documentation files
│   └── POETRY_GUIDE.md    # Poetry package manager guide
│
├── .gitignore             # Git ignore patterns
├── pyproject.toml         # Poetry project configuration
├── poetry.lock            # Poetry dependency lock file
├── README.md              # Project overview
└── PROJECT_STRUCTURE.md   # This file
```

## Directory Descriptions

### `src/`
Contains all Python source code for the web scraping project:
- **config.py**: Configuration settings and constants
- **scraper.py**: Core web scraping functionality using BeautifulSoup4
- **data_cleaner.py**: Data cleaning and preprocessing utilities
- **visualizer.py**: Data visualization and plotting functions
- **webscraping.py**: Main entry point for running the scraper

### `data/`
Stores scraped data and CSV outputs:
- Raw and processed laptop data from Best Buy
- Historical data snapshots

### `notebooks/`
Contains Jupyter notebooks for tutorials and data exploration:
- Interactive examples for beginners
- Data analysis and visualization demos

### `docs/`
Project documentation and guides:
- Setup instructions
- Package manager guides
- API documentation

## Usage

To run the web scraper from the new structure:

```bash
# From project root
python src/webscraping.py
```

Or if using as a module:

```bash
python -m src.webscraping
```

## Note

CSV data files are currently tracked in git. If you want to exclude them from version control, uncomment the CSV pattern in `.gitignore`.
