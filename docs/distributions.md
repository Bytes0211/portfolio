# Statistical Distributions Library

**Last Updated:** October 29, 2025

A comprehensive Python library for statistical calculations and distribution analysis, featuring extensive implementations of normal, Poisson, binomial, and t-distributions.

## Overview

This project provides a robust `Data` class containing methods to support various statistical calculations, distribution analysis, and hypothesis testing. The library is designed for educational purposes and practical statistical computing.

## Key Features

### Distribution Support
- **Normal Distributions**: PDF, CDF, and standard normal calculations
- **Poisson Distributions**: PMF, CDF, and PPF implementations
- **Binomial Distributions**: Random variable generation and probability calculations
- **T-Distributions**: Critical values and confidence intervals
- **Geometric Distributions**: Probability calculations for geometric events

### Statistical Methods
- Central tendency calculations (mean, median, mode)
- Variance and standard deviation
- Z-score transformations
- Sample statistics and proportions
- Frequency analysis

### Hypothesis Testing
- Z-tests and T-tests
- Chi-square tests
- P-value calculations
- Critical value determination
- Confidence interval calculations

### Additional Capabilities
- Linear regression analysis
- Random sampling with/without replacement
- Data transformation and normalization
- Exponential probability calculations

## Unit Tests

The project includes comprehensive unit testing with **38 test cases** covering:

1. **Central Tendency Calculations** - Count, mean, standard deviation, min/max
2. **Poisson PMF Values** - Probability mass function calculations
3. **Binomial Standard Deviation** - Binomial distribution parameters
4. **Z-Score Transformations** - Converting data points to standard deviations
5. **T-Critical Values** - Critical values for t-distributions (lower, upper, two-tailed)

View the complete test suite: [test_datum.py](notebooks/test_datum.py)

All tests pass successfully using Python's `unittest` framework.

## Jupyter Notebooks

The project includes 12 detailed Jupyter notebooks covering fundamental concepts through advanced applications:

### Fundamentals
1. [Distribution Fundamentals](notebooks/dist-01-distribution-fundamentals.ipynb) - Introduction to statistical distributions
2. [Basic Probability and Expected Value](notebooks/dist-02-basic-prob-and-exp-val.ipynb) - Core probability concepts
3. [Standard Deviation and Variance](notebooks/dist-03-std-dev-and-var.ipynb) - Measures of spread
4. [Data Point to Standard Deviation](notebooks/dist-04-data-point-to-std-dev.ipynb) - Z-score calculations

### Discrete Distributions
5. [Binomial Distributions](notebooks/dist-05-binomial-distributions.ipynb) - Binomial probability
6. [Geometric Distributions](notebooks/dist-06-geometric-distributions.ipynb) - Geometric probability
7. [Poisson Distribution](notebooks/dist-07-poisson.ipynb) - Poisson processes

### Sampling and Transformations
8. [Sample Distribution of Sample Mean](notebooks/dist-08-sample-distro-of-sample-mean.ipynb) - Central Limit Theorem
9. [Combinations of Random Variables](notebooks/dist-09-combinations-of-random-vars.ipynb) - Variable operations
10. [Transforming Random Variables](notebooks/dist-10-transforming-random-variables.ipynb) - Variable transformations

### T-Distribution
11. [T-Distribution](notebooks/dist-11-t-distribution.ipynb) - Introduction to t-distribution
12. [Student T-Distribution](notebooks/dist-12-student-t-distribution.ipynb) - Student's t-test applications

## Technologies Used

- **Python 3.x**
- **NumPy** - Numerical computations
- **Pandas** - Data manipulation
- **SciPy** - Statistical functions
- **Statsmodels** - Statistical modeling
- **Scikit-learn** - Machine learning utilities
- **IPython** - Interactive computing and visualization

## Installation

```bash
# Clone the repository
git clone <repository-url>

# Navigate to project directory
cd distributions

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage Example

```python
from datum import Data

# Create a Data instance
data = Data(N=100, mu=50, sigma=10)

# Calculate central tendencies
test_data = [1, 2, 3, 4, 5]
cnt, mu, sigma, min_val, max_val = data.get_central_tendency(test_data)

# Calculate Poisson probability
data_poisson = Data(mu=4.0)
probability = data_poisson.get_poisson_pmf_value(k=2)

# Calculate binomial standard deviation
binom_sigma = data.get_binom_sigma(n_length=100, p=0.5)

# Convert to z-score
z_score = data.convert_to_std_dev(x=60, mu=50, sigma=10)

# Get t-critical value
t_crit = data.get_t_critical_value(tail='upper', q=0.05, df=10)
```

## Running Tests

```bash
# Run all tests
python -m unittest test_datum.py -v

# Run specific test class
python -m unittest test_datum.TestGetCentralTendency -v
```

## Project Structure

```
distributions/
├── datum.py                    # Main Data class with statistical methods
├── test_datum.py              # Comprehensive unit tests
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
└── *.ipynb                    # Jupyter notebooks (12 total)
```

## Author

S Cotton

## License

Available for personal and educational use.
