# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a technical portfolio showcasing data engineering, cloud computing, machine learning, and statistical analysis projects. The portfolio is built using MkDocs Material and contains interactive Jupyter notebooks, project documentation, and technical writeups.

**Live Deployment**: GitHub Pages via GitHub Actions CI/CD workflow (`.github/workflows/ci.yml`)
**Documentation System**: MkDocs Material with mkdocs-jupyter integration
**Project Status**: Actively maintained with frequent updates (last update: Dec 29, 2025)

## Core Architecture

### Documentation System
- **MkDocs Material** (v9.6.22) with custom theme configuration (Material theme with Indigo color scheme)
- **mkdocs-jupyter plugin** (v0.25.1) for rendering notebooks directly in documentation
- **GitHub Actions CI/CD**: Automated deployment to GitHub Pages on push to main/master
- Static site generation with navigation structure defined in `mkdocs.yml`
- Light/dark mode toggle with custom CSS (`docs/stylesheets/extra.css`)
- MathJax integration for mathematical notation
- Custom fonts: Merriweather Sans (text), Red Hat Mono (code)

### Content Organization
```
docs/
├── index.md                          # Portfolio homepage with featured projects
├── about.md                          # Professional background and skills
├── notebooks/                        # Jupyter notebooks (17 total)
│   ├── dist-*.ipynb                 # Statistical distributions (12 notebooks)
│   ├── ht-*.ipynb                   # Hypothesis testing (5 notebooks)
│   ├── test_datum.py                # Unit tests for distribution utilities
│   ├── CORRECTIONS_LOG.md           # Notebook corrections tracking
│   └── README.md                    # Hypothesis testing guide
├── Data Engineering Projects:
│   ├── autocorp-database.md         # AutoCorp data lake pipeline (Phase 4 complete, Phase 5 in progress)
│   ├── streamforge.md               # StreamForge real-time streaming (Phase 1 complete)
│   └── basic-pipeline.md            # AWS data lake pipeline
├── Cloud Computing Projects:
│   ├── aws-management.md            # AWS Manager library
│   ├── aws-file-validator.md        # Java Lambda file validator
│   ├── scotton-aws-utils.md         # AWS utils package
│   ├── terraform-aws-product-app.md # Terraform IaC full-stack app
│   └── dynamodb-inventory-system.md # DynamoDB with GSI, transactions
├── Machine Learning:
│   └── heart-disease.ipynb          # k-NN classification project
├── Statistical Analysis:
│   ├── distributions.md             # Distributions overview
│   ├── hypothesis-testing.md        # Hypothesis testing overview
│   └── distributions_fundementals.ipynb  # Legacy notebook
├── stylesheets/
│   └── extra.css                    # Custom CSS styling
└── assets/
    ├── favicon.png                  # Site logo
    └── favicon.ico                  # Browser icon
```

### Notebook Naming Convention
All notebooks follow: `<prefix>-<number>-<description>.ipynb`
- `dist-01` through `dist-12`: Statistical distributions (12 notebooks)
- `ht-01` through `ht-05`: Hypothesis testing (5 notebooks)
- Two-digit numbering ensures proper sorting and organization
- Total: 17 notebooks in `docs/notebooks/` directory

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

# Deploy to GitHub Pages (manual)
mkdocs gh-deploy --force
# Note: Automated via GitHub Actions on push to main/master
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
- **nbconvert** (7.16.6): Notebook conversion utilities
- **notebook** (7.4.7): Jupyter notebook interface

### Data Science Stack
- **pandas** (2.3.3), **numpy** (2.3.3): Data manipulation
- **scipy** (1.16.2), **statsmodels** (0.14.5): Statistical analysis
- **scikit-learn** (1.7.2): Machine learning
- **matplotlib** (3.10.7), **seaborn** (0.13.2): Visualization
- **plotly** (6.3.1), **bokeh** (3.8.0): Interactive visualizations

### Specialized Tools
- **streamlit** (1.50.0), **dash** (3.2.0): Interactive dashboards
- **pyarrow** (21.0.0): Parquet file handling
- **psycopg2-binary** (2.9.11): PostgreSQL connections
- **pymongo** (4.15.3): MongoDB client for StreamForge project
- **SQLAlchemy** (2.0.44): SQL toolkit and ORM

### Web & Markup
- **Jinja2** (3.1.6): Template engine
- **Markdown** (3.9): Markdown processing
- **beautifulsoup4** (4.14.2): HTML/XML parsing
- **lxml** (6.0.2): XML processing

## Portfolio Projects Context

### AutoCorp Cloud Data Lake Pipeline
**Location**: `docs/autocorp-database.md`
**Status**: Phase 4 Complete ✅ | Phase 5 AI Chatbox In Progress (20%)
**Last Updated**: December 29, 2025
**Scale**: 1.6M operational records (PostgreSQL), 1.19M total unique orders, 7.27M total rows
**Tech**: AWS (DMS, DataSync, Glue, S3, Athena, Bedrock Nova Pro), Apache Hudi, Terraform, PostgreSQL, PySpark, Python, Next.js
**Architecture**: 3-layer data lakehouse (Raw → Processed → Curated) + AI Layer (RAG with Bedrock)
**IaC**: Terraform with 95% automation (8 modules: S3, IAM, Secrets, Glue, Athena, Monitoring, DMS, Bedrock)
**Infrastructure**: 50+ AWS resources deployed
**ETL Jobs**: 10 total (7 operational + 3 analytics denormalized tables)
**Documentation**: 6,500+ lines across 20+ files
**Key Features**: 
- CDC replication with <5min lag
- Serverless ETL with PySpark
- ACID transactions with Apache Hudi
- <15min end-to-end data latency
- CloudWatch monitoring (dashboard with 8 widgets, 3 alarms)
- Athena analytics (workgroup with 5 named queries)
- Phase 5: Bedrock Knowledge Base with 1,584 documents (RAG for AI chatbox)
**Phase 5 Timeline**: 10 days (Days 1-2 complete: Bedrock infrastructure)

### StreamForge Real-Time Streaming Platform
**Location**: `docs/streamforge.md`
**Status**: Phase 1 Complete (40% overall)
**Last Updated**: December 18, 2025
**Duration**: 2 weeks (Dec 4 - Dec 18, 2025)
**Tech**: Apache Kafka 3.5.1, Apache Flink 1.18.0 (Java 11), MongoDB 7.0, Docker Compose, Maven
**Architecture**: Event-driven streaming with dual deployment models (local Docker + AWS planned)
**Key Components**:
- Complete Docker infrastructure (5 services: Kafka, Zookeeper, Flink JobManager/TaskManager, MongoDB)
- Apache Flink stream processing with custom MongoDB sink
- StreamProcessor.java with Kafka integration and consumer group management
- MongoDBSink.java with RichSinkFunction and connection lifecycle management
- Maven build with Shade plugin for fat JAR packaging
- Comprehensive unit tests (StreamProcessor, MongoDBSink, schema validation)
**Phase 2 In Progress**: Windowed aggregations, stateful operations, MongoDB schema design
**Next Phase**: Advanced stream processing (windowing, keyed state), AWS deployment with Terraform

### Statistical Analysis Notebooks
**Distribution fundamentals** (12 notebooks): Probability theory, discrete/continuous distributions, sampling, transformations, T-distribution
**Hypothesis testing** (5 notebooks): P-values, one/two-tail tests (means & proportions), chi-squared, regression testing
**Framework**: Custom testing utilities in `resources/` (datum.py, test.py, glyph.py, plot.py) for reusable test configurations
**Sample Datasets**: cod_population.csv, salmon_population.csv

### Machine Learning Projects
**Heart Disease Prediction** (`docs/heart-disease.ipynb`):
- k-NN classification with GridSearchCV optimization (k=1-30, weights, distance metrics)
- Comprehensive data cleaning with median imputation
- EDA with correlation analysis and feature visualization
- Hyperparameter tuning using GridSearchCV
- Multi-metric evaluation (accuracy, precision, recall, F1, AUC, cross-validation)
**Last Updated**: November 8, 2025

### Cloud Computing Projects
**AWS Management** (`docs/aws-management.md`):
- Python library for Lambda, S3, EC2, DynamoDB operations
- Local development support and comprehensive testing (16+ unit tests)
- pytest with moto for AWS service mocking

**AWS File Validator** (`docs/aws-file-validator.md`):
- Serverless Java 11 application for CSV/JSON validation
- AWS Lambda with S3 integration
- Maven build system, extensible architecture

**Scotton AWS Utils** (`docs/scotton-aws-utils.md`):
- Comprehensive Python package for AWS service operations
- Unified interface for S3, Lambda, EC2, IAM, DynamoDB
- Advanced DynamoDB features (transactions, batch operations, GSI/LSI support)
- Pip-installable package

**Terraform AWS Product App** (`docs/terraform-aws-product-app.md`):
- Complete Infrastructure as Code using Terraform
- Full-stack serverless product management application
- VPC networking with public/private subnets
- Spring Boot (Java 17), Python Lambda, DynamoDB
- Automated deployment with one-command provisioning

**DynamoDB Inventory System** (`docs/dynamodb-inventory-system.md`):
- Advanced DynamoDB project with single table design
- Global Secondary Indexes (GSI), transactions, batch operations
- Composite keys, conditional writes, query optimization
- 20+ comprehensive unit tests
- Enterprise-level NoSQL patterns

**AWS Data Lake Pipeline** (`docs/basic-pipeline.md`):
- Event-driven AWS pipeline with Terraform IaC
- 3-layer data lake architecture
- Serverless ETL with Lambda, S3, EventBridge
- Automated testing and deployment
**Last Updated**: November 18, 2025

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

## GitHub Actions CI/CD

**Workflow File**: `.github/workflows/ci.yml`
**Trigger**: Push to `main` or `master` branch
**Actions**:
1. Checkout repository
2. Configure Git credentials (github-actions bot)
3. Setup Python 3.x
4. Cache dependencies (keyed by week number)
5. Install mkdocs-material and mkdocs-jupyter
6. Deploy to GitHub Pages (`mkdocs gh-deploy --force`)

**Deployment**: Automated static site deployment to GitHub Pages on every push

## Important Notes

- The current virtual environment is `.portfolioVenv` (not the Makefile default `.venv`)
- Site output directory `site/` contains built static files (excluded from version control)
- MathJax CDN included for rendering mathematical equations in notebooks
- Material design icons via FontAwesome for social links
- Personal info and links configured in `mkdocs.yml` under `extra.social`
- Privacy policy link points to GitHub's privacy statement
- Copyright range: 2018 - 2025 Steven Cotton
- Repository includes update tracking files (AUTOCORP_DEC29_UPDATE.md, HEART_DISEASE_UPDATE.md, etc.)

## Project Maintenance

- Portfolio is actively maintained with frequent updates (see `docs/index.md` for latest updates)
- Latest major updates:
  - **StreamForge** (Dec 18, 2025): Phase 1 complete - Docker infrastructure, Flink processing, MongoDB sink
  - **AutoCorp** (Dec 29, 2025): Phase 4 complete, Phase 5 (AI Chatbox) 20% complete - Bedrock infrastructure ready
  - **AWS Data Lake Pipeline** (Nov 18, 2025): Complete event-driven pipeline with Terraform IaC
  - **Heart Disease Prediction** (Nov 08, 2025): Complete ML pipeline with k-NN classification
- Documentation totals 6,500+ lines for AutoCorp alone across 20+ files
- Focus on comprehensive technical documentation with code examples
- Real-world project emphasis: production-scale data volumes, infrastructure automation, end-to-end implementations
- Project tracking via dedicated update files in root directory

## Navigation Structure

**mkdocs.yml** defines the site navigation with the following major sections:
1. **Home**: Portfolio overview with featured projects (`index.md`)
2. **About**: Professional background and skills (`about.md`)
3. **Data Engineering**: AutoCorp, StreamForge, AWS Data Lake Pipeline (3 projects)
4. **Data Science**: 
   - Statistical Distributions (overview + 12 notebooks organized by topic)
   - Hypothesis Testing (overview + 5 notebooks)
5. **Machine Learning**: Heart Disease Prediction (1 notebook)
6. **Cloud Computing**: AWS services, Terraform, DynamoDB projects (5 projects)

**Featured Projects Order** (as shown on homepage):
1. AutoCorp Cloud Data Lake Pipeline (primary showcase)
2. StreamForge Real-Time Streaming Platform
3. AWS Data Lake Pipeline
4. Heart Disease Prediction
5. AWS Manager
6. AWS File Validator
7. Scotton AWS Utils
8. AWS Product Management App
