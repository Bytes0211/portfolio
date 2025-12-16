# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a technical portfolio showcasing data engineering, cloud computing, machine learning, and statistical analysis projects. The portfolio is built using MkDocs Material and contains interactive Jupyter notebooks, project documentation, and technical writeups.

## Core Architecture

### Documentation System
- **MkDocs Material** with custom theme configuration (Material theme with Indigo color scheme)
- **mkdocs-jupyter plugin** for rendering notebooks directly in documentation
- Static site generation with navigation structure defined in `mkdocs.yml`
- Light/dark mode support with custom CSS (`docs/stylesheets/extra.css`)
- MathJax integration for mathematical notation

### Content Organization
```
docs/
├── index.md                    # Portfolio homepage with featured projects
├── about.md                    # Professional background and skills
├── notebooks/                  # Jupyter notebooks organized by project prefix
│   ├── dist-*.ipynb           # Statistical distributions (12 notebooks)
│   ├── ht-*.ipynb             # Hypothesis testing (5 notebooks)
│   └── test_datum.py          # Unit tests for distribution utilities
├── autocorp-database.md        # AutoCorp data lake pipeline project
├── basic-pipeline.md           # AWS data lake pipeline
├── heart-disease.ipynb         # ML classification project
└── [other project docs]        # Additional cloud/data engineering projects
```

### Notebook Naming Convention
All notebooks follow: `<prefix>-<number>-<description>.ipynb`
- `dist-01` through `dist-12`: Statistical distributions
- `ht-01` through `ht-05`: Hypothesis testing
- Two-digit numbering ensures proper sorting and organization

### Supporting Resources
- `resources/`: Python utilities for data processing, visualization, and testing
  - `datum.py`: Data processing utilities
  - `test.py`: Statistical testing framework
  - `glyph.py` / `plot.py`: Visualization utilities
  - Sample datasets (CSV files)

## Common Development Commands

### Local Development
```bash
# Serve documentation locally (auto-reload on changes)
mkdocs serve
# View at http://127.0.0.1:8000

# Build static site
mkdocs build
# Output in site/ directory
```

### Virtual Environment Setup
```bash
# Create and setup virtual environment
make setup
# This prompts for venv name (default: .venv) and installs requirements.txt

# Activate and update dependencies
make activate
```

### Jupyter Notebooks
```bash
# Launch Jupyter (after activating venv)
jupyter notebook
# Opens browser to notebooks interface

# Launch JupyterLab (alternative)
jupyter lab
```

### Cleanup
```bash
# Remove build artifacts and cache
make clean
# Removes: build/, dist/, __pycache__, .eggs/
```

## Key Python Dependencies

### Documentation & Notebooks
- **mkdocs** (1.6.1), **mkdocs-material** (9.6.22): Documentation framework
- **mkdocs-jupyter** (0.25.1): Jupyter notebook integration
- **jupyter** (1.1.1), **jupyterlab** (4.4.9): Interactive development
- **nbconvert**: Notebook conversion utilities

### Data Science Stack
- **pandas** (2.3.3), **numpy** (2.3.3): Data manipulation
- **scipy** (1.16.2), **statsmodels** (0.14.5): Statistical analysis
- **scikit-learn** (1.7.2): Machine learning
- **matplotlib** (3.10.7), **seaborn** (0.13.2): Visualization
- **plotly** (6.3.1), **bokeh** (3.8.0): Interactive visualizations

### Specialized Tools
- **streamlit** (1.50.0), **dash** (3.2.0): Interactive dashboards
- **pyarrow** (21.0.0): Parquet file handling
- **psycopg2-binary**: PostgreSQL connections

## Portfolio Projects Context

### AutoCorp Cloud Data Lake Pipeline
**Location**: `docs/autocorp-database.md`
**Scale**: 1.19M unique orders, 7.27M total rows
**Tech**: AWS (DMS, DataSync, Glue, S3, Athena), Apache Hudi, Terraform, PySpark
**Architecture**: 3-layer data lakehouse (Raw → Processed → Curated)
**IaC**: Terraform with 95% automation (6 modules, 25 files)
**Key Features**: CDC replication, serverless ETL, ACID transactions with Hudi, <15min data latency

### Statistical Analysis Notebooks
**Distribution fundamentals** (12 notebooks): Probability theory, discrete/continuous distributions, sampling, transformations, T-distribution
**Hypothesis testing** (5 notebooks): P-values, one/two-tail tests (means & proportions), chi-squared, regression testing
**Framework**: Custom testing utilities in `resources/` for reusable test configurations

### Machine Learning Projects
**Heart Disease Prediction**: k-NN classification with GridSearchCV, comprehensive EDA, feature engineering, multi-metric evaluation

## Working with Notebooks

### Adding New Notebooks
1. Choose appropriate prefix (`dist`, `ht`, or create new for different project type)
2. Use next sequential number with leading zero (e.g., `dist-13`, `ht-06`)
3. Place in `docs/notebooks/` directory
4. Update `mkdocs.yml` navigation structure to include new notebook
5. Follow self-contained pattern: include imports, explanations, and outputs

### Testing Statistical Utilities
```python
# Example usage of custom testing framework
import sys
sys.path.insert(0, '..')
from resources import test, datum

test_params = {
    'cl': 0.95,              # Confidence level
    'type': 'prop',          # Test type
    'tail': 'lower',         # Test direction
    'n1': 100,
    'p1': 0.30,
    'null_hypo': 'H₀ description',
    'alt_hypo': 'H₁ description',
    'visual': True
}

test_obj = test.Test()
test_obj.make_hypothesis_test(info=test_params)
```

## Documentation Updates

### Adding New Projects
1. Create project documentation in `docs/`
2. Add entry to `docs/index.md` under appropriate section
3. Update `mkdocs.yml` navigation structure
4. Include technical stack, features, and project-specific details
5. Use consistent formatting with existing project docs

### MkDocs Configuration
**Theme features enabled**:
- Navigation tabs, footer, top navigation
- Code annotation and copy buttons
- Search with highlighting and suggestions
- TOC integration
- Content tabs with linking
- Mermaid diagram support
- Dark/light mode toggle

**Markdown extensions**:
- PyMdown extensions for enhanced formatting
- Admonitions for callout boxes
- Superfences for code blocks and Mermaid
- Math support via MathJax

## Important Notes

- The current virtual environment is `.portfolioVenv` (not the Makefile default `.venv`)
- Site output directory `site/` contains built static files (excluded from version control)
- MathJax CDN included for rendering mathematical equations in notebooks
- Material design icons via FontAwesome for social links
- Personal info and links configured in `mkdocs.yml` under `extra.social`

## Project Maintenance

- Portfolio is actively maintained with frequent updates (see `docs/index.md` for latest updates)
- Documentation totals 4,670+ lines across project files
- Focus on comprehensive technical documentation with code examples
- Real-world project emphasis: production-scale data volumes, infrastructure automation, end-to-end implementations
