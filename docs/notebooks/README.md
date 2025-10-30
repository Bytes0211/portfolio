# Notebook Naming Convention

This directory contains Jupyter notebooks organized by project using a standardized naming convention.

## Naming Pattern

All notebooks follow this pattern:

```
<project-prefix>-<number>-<descriptive-name>.ipynb
```

### Components

- **project-prefix**: A short abbreviation identifying the project (lowercase)
- **number**: Two-digit sequence number (01, 02, etc.)
- **descriptive-name**: Hyphen-separated description of the notebook content

## Current Project Prefixes

### `dist` - Statistical Distributions
Notebooks covering statistical distributions, probability theory, and related calculations.

**Count**: 12 notebooks

Examples:
- `dist-01-distribution-fundamentals.ipynb`
- `dist-05-binomial-distributions.ipynb`
- `dist-12-student-t-distribution.ipynb`

### `ht` - Hypothesis Testing
Notebooks focused on hypothesis testing methods, p-values, and statistical inference.

**Count**: 5 notebooks

Examples:
- `ht-01-intro-to-pvalue.ipynb`
- `ht-02-one-two-tail-test-diff-mean.ipynb`
- `ht-04-chi-squared.ipynb`

## Benefits of This Convention

1. **Organization**: Easy to identify which project a notebook belongs to
2. **Sorting**: Notebooks automatically sort by project and sequence
3. **Scalability**: Easy to add new projects without conflicts
4. **Clarity**: Clear and descriptive names improve discoverability
5. **Navigation**: Facilitates building hierarchical navigation structures

## Adding New Projects

When adding a new project:

1. Choose a short, memorable prefix (2-4 characters recommended)
2. Use lowercase letters only
3. Update this README with the new prefix and description
4. Follow the same numbering pattern (01, 02, etc.)
5. Update the portfolio's `mkdocs.yml` navigation structure

## Example Projects for Future

Potential future prefixes:
- `ml` - Machine Learning
- `nlp` - Natural Language Processing
- `ts` - Time Series Analysis
- `da` - Data Analysis
- `viz` - Data Visualization
- `spark` - Apache Spark
- `sql` - SQL Queries and Analysis

## Directory Structure

```
notebooks/
├── README.md                                    # This file
├── test_datum.py                               # Unit tests for distributions
├── dist-01-distribution-fundamentals.ipynb    # Distribution notebooks
├── dist-02-basic-prob-and-exp-val.ipynb
├── ...
├── dist-12-student-t-distribution.ipynb
├── ht-01-intro-to-pvalue.ipynb                # Hypothesis testing notebooks
├── ht-02-one-two-tail-test-diff-mean.ipynb
├── ...
└── ht-05-regression-hypothesis.ipynb
```

## Legacy Files

Some older notebooks in the parent `docs/` directory may not follow this convention. They remain for backward compatibility but new notebooks should follow the standard pattern and be placed in this directory.

## Notes

- Notebooks are version-controlled and should include clear documentation
- Each notebook should be self-contained with necessary imports and explanations
- Consider adding a brief description at the top of each notebook
- Use descriptive cell outputs to enhance readability

## Maintenance

Last updated: 2025-10-30

Maintained by: S Cotton
