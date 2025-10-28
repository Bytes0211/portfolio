# Hypothesis Testing 📊

A comprehensive collection of Jupyter notebooks exploring statistical hypothesis testing concepts, methods, and practical applications using Python.

## Overview

This series of notebooks provides hands-on demonstrations of hypothesis testing techniques commonly used in data science and statistical analysis. Each notebook includes theoretical explanations, visual illustrations, and practical examples with real-world datasets.

## 📓 Notebooks

### [1. Introduction to P-Value](notebooks/01-intro-to-pvalue.ipynb)

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

### [2. One-Tail and Two-Tail Tests for Difference in Means](notebooks/02-one-two-tail-test-diff-mean.ipynb)

**Objective**: Understanding directional vs. non-directional hypothesis tests

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

### [3. Chi-Squared Test](notebooks/03-chi-squared.ipynb)

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

### [4. Hypothesis Testing in Regression](notebooks/04-regression-hypothesis.ipynb)

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

## Learning Path

**Recommended Order**:
1. Start with **Introduction to P-Value** to build foundational understanding
2. Move to **One-Tail and Two-Tail Tests** to learn about directional testing
3. Explore **Chi-Squared Test** for categorical data analysis
4. Complete with **Regression Hypothesis Testing** for advanced applications

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
| Chi-squared | Categorical relationships | #3 |
| F-test | Regression significance | #4 |
| t-test (regression) | Coefficient significance | #4 |

## Practical Applications

These notebooks demonstrate hypothesis testing in contexts such as:

- **Population Studies**: Testing differences between fish populations (cod and salmon)
- **A/B Testing**: Comparing two groups to determine statistical differences
- **Survey Analysis**: Analyzing categorical data relationships
- **Predictive Modeling**: Validating regression model assumptions

## Visual Learning

Each notebook includes:
- 📊 Distribution plots showing p-value regions
- 📈 Visual representations of test statistics
- 🎯 Graphical interpretations of critical regions
- 📉 Regression diagnostic plots

## Prerequisites

**Required Knowledge**:
- Basic statistics (mean, variance, standard deviation)
- Understanding of probability distributions
- Familiarity with Python and Jupyter notebooks

**Setup**:
```bash
# Install required packages
pip install numpy pandas matplotlib seaborn scipy statsmodels jupyter
```

## Usage

### Running Locally

```bash
# Clone or download the notebooks
cd hypothesis-testing

# Launch Jupyter
jupyter notebook

# Open any notebook to begin exploring
```

### Interactive Exploration

Each notebook is designed to be:
- **Self-contained**: Can be run independently
- **Interactive**: Modify parameters to see different outcomes
- **Educational**: Includes explanations and interpretations

## Code Examples

### Example: Basic P-Value Calculation

```python
import numpy as np
from scipy import stats

# Sample data
sample_mean = 52
population_mean = 50
std_dev = 10
n = 30

# Calculate z-score
z_score = (sample_mean - population_mean) / (std_dev / np.sqrt(n))

# Calculate p-value (two-tailed)
p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

print(f"Z-score: {z_score:.4f}")
print(f"P-value: {p_value:.4f}")
```

### Example: Chi-Squared Test

```python
import pandas as pd
from scipy.stats import chi2_contingency

# Contingency table
data = pd.DataFrame({
    'Group A': [30, 20],
    'Group B': [25, 25]
})

# Perform chi-squared test
chi2, p_value, dof, expected = chi2_contingency(data)

print(f"Chi-squared statistic: {chi2:.4f}")
print(f"P-value: {p_value:.4f}")
print(f"Degrees of freedom: {dof}")
```

## Learning Outcomes

After completing these notebooks, you will be able to:

- ✅ Understand and interpret p-values
- ✅ Choose appropriate hypothesis tests for different scenarios
- ✅ Perform one-tailed and two-tailed tests
- ✅ Analyze categorical data with chi-squared tests
- ✅ Interpret regression output and test coefficient significance
- ✅ Make data-driven decisions using statistical evidence
- ✅ Communicate statistical findings effectively

## Additional Resources

- **Statistical Theory**: Background on probability distributions and sampling
- **Python for Data Science**: pandas, NumPy, and visualization libraries
- **Real-World Applications**: Case studies in various domains

## Repository

[View on GitHub](https://github.com/Bytes0211/hypothesis-testing)

---

[← Back to Data Science](ds.md)
