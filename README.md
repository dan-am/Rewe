# Rewe Project

An analytical Python project following best practices for data science and analysis.

## Project Structure

```
.
├── README.md              # Project documentation
├── .gitignore            # Git ignore file (data folders excluded)
├── .env.example          # Example environment variables
├── requirements.txt      # Python dependencies
├── setup.py             # Package setup file
├── setup.cfg            # Configuration for tools
├── pyproject.toml       # Modern Python project configuration
│
├── data/                # Data directory (not committed to git)
│   ├── raw/            # Original, immutable data
│   ├── processed/      # Cleaned, transformed data
│   ├── interim/        # Intermediate transformation data
│   └── external/       # External reference data
│
├── notebooks/           # Jupyter notebooks for exploration
│   └── README.md       # Notebook organization guidelines
│
├── src/                # Source code for the project
│   └── rewe/          # Main package
│       ├── __init__.py
│       ├── data.py           # Data loading/saving functions
│       ├── utils.py          # Utility functions
│       └── visualization.py  # Plotting functions
│
├── tests/              # Unit tests
│   ├── __init__.py
│   ├── test_data.py
│   └── test_utils.py
│
└── docs/               # Project documentation

```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip or conda for package management

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Rewe
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install the package in development mode:
```bash
pip install -e .
```

5. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your specific values
```

### Running Tests

```bash
pytest
```

For coverage report:
```bash
pytest --cov=src --cov-report=html
```

### Code Quality

Format code with black:
```bash
black src/ tests/
```

Sort imports:
```bash
isort src/ tests/
```

Lint with flake8:
```bash
flake8 src/ tests/
```

Type checking with mypy:
```bash
mypy src/
```

## Data Management

### Data Folder Structure

- **`data/raw/`**: Original, immutable data. Never modify files here.
- **`data/processed/`**: Cleaned and transformed data ready for analysis.
- **`data/interim/`**: Intermediate data during multi-step transformations.
- **`data/external/`**: External reference data, lookup tables, etc.

### Important Notes

- **Data files are NOT committed to git** - they are excluded via `.gitignore`
- Only `.gitkeep` files and `README.md` files in data folders are tracked
- Document your data sources and processing steps
- Keep raw data immutable - all transformations should be reproducible

## Using Notebooks

Jupyter notebooks are stored in the `notebooks/` directory. Best practices:

1. Use numbered prefixes for sequential analysis (e.g., `01_exploration.ipynb`)
2. Include descriptive names
3. Add markdown cells to document your analysis
4. Move reusable code to the `src/` directory
5. Clear outputs before committing (optional)

To start Jupyter:
```bash
jupyter notebook
```

## Development Workflow

1. Place raw data in `data/raw/`
2. Create notebooks in `notebooks/` for exploration
3. Move reusable code to `src/rewe/`
4. Write tests in `tests/`
5. Save processed data to `data/processed/`

## Contributing

1. Create a new branch for your feature
2. Write tests for new functionality
3. Ensure all tests pass
4. Format code with black and isort
5. Submit a pull request

## License

MIT

## Authors

Your Name

## Acknowledgments

- Project structure inspired by [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/)
