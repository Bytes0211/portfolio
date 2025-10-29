# Hypothesis Testing 📊

A comprehensive collection of Jupyter notebooks exploring statistical hypothesis testing concepts, methods, and practical applications using Python.

## Overview

This project provides hands-on demonstrations of hypothesis testing techniques commonly used in data science and statistical analysis. Each notebook includes theoretical explanations, visual illustrations, and practical examples with real-world datasets.

## 📓 Notebooks

### [1. Introduction to P-Value](01-intro-to-pvalue.ipynb)

**Objective**: Understanding the premise of the p-value concept

**Topics Covered**:
- Concept of p-value in statistical testing
- Normal distribution and probability
- Visual interpretation of p-values
- Relationship between p-values and statistical significance
- Practical examples with visualizations

**Key Concepts**:
- What is a p-value?
- How to interpret p-values in hypothesis testing
- Understanding significance levels (alpha)
- Type I and Type II errors

---

### [2. One-Tail and Two-Tail Tests for Difference in Means](02-one-two-tail-test-diff-mean.ipynb)

**Objective**: Understanding directional vs. non-directional hypothesis tests for means

**Topics Covered**:
- One-tailed vs. two-tailed tests
- Testing for differences in population means
- When to use each type of test
- Critical values and rejection regions
- Practical examples comparing group means

**Key Concepts**:
- Null hypothesis (H₀) vs. alternative hypothesis (H₁)
- Left-tailed, right-tailed, and two-tailed tests
- Z-tests and t-tests for mean differences
- Interpreting test statistics

---

### [3. One-Tail and Two-Tail Tests for Difference of Proportions](03_one_two_tail_test_diff_props.ipynb)

**Objective**: Testing differences between categorical response proportions

**Topics Covered**:
- Hypothesis testing for two proportions
- Two-tailed, upper-tail, and lower-tail tests for proportions
- Combined sample proportion (p-hat)
- Test statistic formula for difference of proportions
- Criteria for using normal approximation (≥5 successes and failures)

**Key Concepts**:
- Comparing population proportions (p₁ vs. p₂)
- Pooled proportion estimate
- Z-test for difference of proportions
- Critical value and p-value interpretation
- Practical example: comparing vehicle type proportions between states

---

### [4. Chi-Squared Test](04-chi-squared.ipynb)

**Objective**: Testing relationships between categorical variables

**Topics Covered**:
- Chi-squared test for independence
- Contingency tables and observed vs. expected frequencies
- Degrees of freedom in chi-squared tests
- Goodness-of-fit tests
- Applications in categorical data analysis

**Key Concepts**:
- Testing independence between categorical variables
- Chi-squared distribution
- Calculating chi-squared statistic
- Interpreting chi-squared test results

---

### [5. Hypothesis Testing in Regression](05-regression-hypothesis.ipynb)

**Objective**: Understanding hypothesis testing within regression analysis

**Topics Covered**:
- Testing significance of regression coefficients
- F-test for overall model significance
- t-tests for individual predictors
- Confidence intervals for regression parameters
- Model diagnostics and assumptions

**Key Concepts**:
- Linear regression hypothesis testing
- Testing β coefficients
- R² and adjusted R²
- P-values in regression output
- Multiple regression considerations

## Technology Stack

**Language**: Python  
**Key Libraries**:
- NumPy - Numerical computations
- Pandas - Data manipulation
- Matplotlib/Seaborn - Data visualization
- SciPy - Statistical functions
- Statsmodels - Statistical modeling
- Bokeh - Interactive visualizations

## Getting Started

### Prerequisites

- Python 3.x
- pip package manager
- Virtual environment support

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd hypothesis-testing
   ```

2. **Set up virtual environment**:
   ```bash
   make setup
   ```
   This will prompt you for a virtual environment name (default: `.venv`) and install all dependencies.

3. **Activate the environment**:
   ```bash
   make activate
   ```

4. **Launch Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```

### Makefile Commands

- `make setup` - Create virtual environment and install dependencies
- `make activate` - Activate virtual environment and install/update dependencies
- `make clean` - Remove build artifacts and cache files

## Project Structure

```
hypothesis-testing/
├── 01-intro-to-pvalue.ipynb                    # P-value fundamentals
├── 02-one-two-tail-test-diff-mean.ipynb        # Testing means
├── 03_one_two_tail_test_diff_props.ipynb       # Testing proportions
├── 04-chi-squared.ipynb                         # Chi-squared tests
├── 05-regression-hypothesis.ipynb               # Regression testing
├── create_test.py                               # Test parameter configuration
├── resources/                                   # Support modules and data
│   ├── datum.py                                 # Data processing utilities
│   ├── test.py                                  # Testing framework
│   ├── glyph.py                                 # Visualization utilities
│   ├── plot.py                                  # Plotting functions
│   ├── cod_population.csv                       # Sample dataset
│   └── salmon_population.csv                    # Sample dataset
├── requirements.txt                             # Python dependencies
├── Makefile                                     # Build automation
└── README.md                                    # This file
```

## Learning Path

**Recommended Order**:
1. Start with **Introduction to P-Value** to build foundational understanding
2. Move to **One-Tail and Two-Tail Tests (Means)** to learn about directional testing for means
3. Progress to **One-Tail and Two-Tail Tests (Proportions)** for categorical response variables
4. Explore **Chi-Squared Test** for testing independence in categorical data
5. Complete with **Regression Hypothesis Testing** for advanced applications

## Key Statistical Concepts

### Hypothesis Testing Framework

1. **Formulate Hypotheses**
   - Null hypothesis (H₀): No effect or no difference
   - Alternative hypothesis (H₁): Effect exists or difference exists

2. **Choose Significance Level**
   - Typically α = 0.05 (5% significance level)
   - Represents probability of Type I error

3. **Calculate Test Statistic**
   - Z-statistic, t-statistic, chi-squared statistic, F-statistic
   - Depends on the type of test and data

4. **Determine P-Value**
   - Probability of observing results as extreme as actual results
   - If p-value < α, reject null hypothesis

5. **Draw Conclusion**
   - Reject or fail to reject null hypothesis
   - Interpret results in context

### Common Tests Covered

| Test Type | Use Case | Notebook |
|-----------|----------|----------|
| Z-test / t-test | Compare means | #1, #2 |
| Z-test (proportions) | Compare proportions | #3 |
| Chi-squared | Categorical relationships | #4 |
| F-test | Regression significance | #5 |
| t-test (regression) | Coefficient significance | #5 |

## Practical Applications

These notebooks demonstrate hypothesis testing in contexts such as:

- **Population Studies**: Testing differences between fish populations (cod and salmon)
- **A/B Testing**: Comparing two groups to determine statistical differences
- **Proportion Comparisons**: Testing differences in categorical responses (e.g., vehicle type proportions between states)
- **Survey Analysis**: Analyzing categorical data relationships
- **Predictive Modeling**: Validating regression model assumptions

## Visual Learning

Each notebook includes:
- 📊 Distribution plots showing p-value regions
- 📈 Visual representations of test statistics
- 🎯 Graphical interpretations of critical regions
- 📉 Regression diagnostic plots
- 🎨 Interactive Bokeh visualizations

## Usage

### Running Notebooks Locally

```bash
# Activate virtual environment
source .venv/bin/activate  # or your chosen venv name

# Launch Jupyter
jupyter notebook

# Open any notebook to begin exploring
```

### Using the Test Framework

The `create_test.py` script demonstrates how to configure and run hypothesis tests programmatically:

```python
import sys
sys.path.insert(0, '..')
from resources import test, datum

# Configure test parameters
test_params = {
    'cl': 0.95,              # Confidence level
    'type': 'prop',          # Test type: 'prop', 'mean', etc.
    'tail': 'lower',         # 'lower', 'upper', or 'two'
    'n1': 100,               # Sample size
    'p1': 0.30,              # Sample proportion
    'null_hypo': 'H₀ description',
    'alt_hypo': 'H₁ description',
    'visual': True           # Generate visualizations
}

# Run the test
test_obj = test.Test()
test_obj.make_hypothesis_test(info=test_params)
```

## Learning Outcomes

After completing these notebooks, you will be able to:

- ✅ Understand and interpret p-values
- ✅ Choose appropriate hypothesis tests for different scenarios
- ✅ Perform one-tailed and two-tailed tests
- ✅ Test differences in means and proportions
- ✅ Analyze categorical data with chi-squared tests
- ✅ Interpret regression output and test coefficient significance
- ✅ Make data-driven decisions using statistical evidence
- ✅ Communicate statistical findings effectively

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available for educational purposes.

## Author

**S Cotton**

## Acknowledgments

- Statistical concepts based on standard hypothesis testing theory
- Visualizations created using Bokeh, Matplotlib, and Seaborn
- Sample datasets included for educational demonstration

---

**Note**: These notebooks are designed for educational purposes to help understand statistical hypothesis testing concepts. Always ensure you understand the assumptions and limitations of each test before applying them to real-world data.
