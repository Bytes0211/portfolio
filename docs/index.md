# Steven Cotton

**Data Engineer | Cloud Architect | Infrastructure as Code Specialist**

> Home of passionate, thoughtful energy expressed through code
> Projects are being updated frequently. Now that my employment has changed, I am moving from code commit to github.

## 🚀 Featured Projects

Most of these projects originally resided in AWS CodeCommit. I decided to migrate to GitHub and so I did some cleanup along the way. It's been a lot of "Now how does that work?", "What the heck is that?", and "That's stupid!", but it's been kinda fun experience. 

### AutoCorp Cloud Data Lake Pipeline ☁️

An end-to-end **AWS Data Lake Pipeline** implementing modern data lakehouse architecture with CDC replication, serverless ETL, open table formats, and **Infrastructure as Code** (Terraform).

- **Tech Stack**: AWS (DMS, DataSync, Glue, S3, Athena), Apache Hudi, Terraform, PostgreSQL, PySpark, Python
- **Features**: 3-layer data lakehouse (Raw → Curated), CDC replication, serverless ETL, <15min data latency, 95% IaC automation
- **Highlights**: Complete Terraform IaC (6 modules), Apache Hudi ACID transactions, PySpark data quality, 3,103+ lines of documentation
- **Skills**: Cloud Data Engineering, Infrastructure as Code, AWS Data Services, PySpark ETL, Open Table Formats, Technical Documentation
- [View Project](autocorp-database.md)

### AWS Data Lake Pipeline 🔄

An event-driven **AWS Data Lake Pipeline** built with Infrastructure as Code principles, demonstrating production-ready architecture for data ingestion, transformation, and consumption.

- **Tech Stack**: Terraform, AWS Lambda, S3, EventBridge, Pandas
- **Features**: 3-layer data lake architecture, event-driven processing, automated testing
- **Highlights**: Complete IaC with Terraform, serverless ETL, S3 event triggers
- **Skills**: Data Engineering, Cloud Architecture, Python, Event-Driven Design
- [View Project](basic-pipeline.md)

### Heart Disease Prediction 🫀

A comprehensive machine learning project demonstrating a complete ML pipeline for predicting heart disease using k-Nearest Neighbors classification.

- **Tech Stack**: Python, pandas, scikit-learn, seaborn, matplotlib
- **Features**: Data cleaning, EDA, feature engineering, hyperparameter tuning, comprehensive evaluation
- **Model**: k-NN with GridSearchCV optimization (k=1-30, weights, distance metrics)
- **Evaluation**: Confusion matrix, ROC curves, AUC, cross-validation
- [View Project](heart-disease.ipynb)

### AWS Manager ☁️

A comprehensive Python library for managing AWS services (Lambda, S3, EC2, DynamoDB) with local development support and comprehensive testing.

- **Tech Stack**: Python, Boto3, pytest, moto
- **Features**: Local DynamoDB, Table Migration, 16+ Unit Tests
- [View Project](aws-management.md)

### AWS File Validator 📄

A serverless Java application that validates file formats (CSV/JSON) using AWS Lambda and uploads validated files to S3.

- **Tech Stack**: Java 11, AWS Lambda, S3, Maven
- **Features**: CSV/JSON Validation, Extensible Architecture, Local Testing
- [View Project](aws-file-validator.md)

### Scotton AWS Utils ⚙️

A comprehensive Python package for AWS service operations with unified interface for S3, Lambda, EC2, IAM, and DynamoDB.

- **Tech Stack**: Python, Boto3, pip package
- **Features**: Multi-Service Support, Advanced DynamoDB, Transactions, Local Testing
- [View Project](scotton-aws-utils.md)

### AWS Product Management App 🏭️

A Complete Infrastructure as Code using Terraform to deploy a full-stack product management application on AWS.

- **Tech Stack**: Terraform, Spring Boot, Python Lambda, DynamoDB
- **Features**: VPC Networking, Automated Deployment, Full-Stack Architecture
- [View Project](terraform-aws-product-app.md)

## 📚 Documentation Hub

### 🔄 Data Engineering

End-to-end data pipeline implementations with modern cloud-native technologies

- **Data Lakehouse Architecture**: Multi-layer data platforms with raw, processed, and curated zones
- **CDC Replication**: Real-time data capture with AWS DMS and streaming ingestion
- **Serverless ETL**: PySpark and Lambda-based data transformation at scale
- **Open Table Formats**: Apache Hudi for ACID transactions on data lakes
- **Event-Driven Architecture**: S3 triggers, EventBridge orchestration
- **PostgreSQL Database Design**: Source system design with normalized schemas
- **SQL Query Optimization**: Complex joins, aggregations, and analytics queries

### ☁️ [Cloud Computing](cloud-compute.md)

AWS and Terraform projects with practical implementations and educational resources

- AWS Service Management
- Infrastructure as Code
- Deployment Automation

### 📊 [Data Science](ds.md)

Data analysis guides, machine learning experiments, and statistical computing

- Data Analysis
- Machine Learning
- Visualization

### ☕ [Java](java.md)

Java projects showcasing serverless architectures, AWS integration, and enterprise patterns

- AWS Lambda Functions
- File Validation Systems
- Cloud Integration

### 👤 [About](about.md)

Learn more about my background, skills, and interests

## 🛠️ Tech Stack

**Languages**: Python, Java, SQL, Bash, HCL (Terraform), PySpark  
**Cloud & Infrastructure**: AWS (DMS, DataSync, Glue, Athena, Lambda, S3, EventBridge, EC2, DynamoDB), Terraform (IaC with 95% automation)  
**Databases**: PostgreSQL, DynamoDB  
**Data Engineering**: Apache Hudi, PySpark, Pandas, Event-Driven Architecture, ETL Pipelines, CDC Replication  
**Infrastructure as Code**: Terraform modules, multi-environment deployment, remote state management  
**Tools**: Git, Docker, pytest, AWS CLI, psycopg2, mkdocs

## 📝 Latest Updates

### AutoCorp Cloud Data Lake Pipeline (Dec 4, 2025)

**Phase 2 - Glue ETL with Apache Hudi Nearly Complete** (85% Phase 2 progress, 43% overall):
- **7 Production PySpark ETL Jobs Deployed**: 535 lines of PySpark code with Hudi integration
- **All ETL Scripts Uploaded**: 7 scripts deployed to S3 via Terraform automation
- **2 Glue Crawlers Operational**: Automated schema discovery for raw zones
- **First Hudi Table Validated**: auto_parts (400 records → 3.5 MB, 57 Parquet files)
- **AWS Glue 4.0**: 7 serverless ETL jobs with job bookmarking and CloudWatch logging
- **Developer's Journal**: 911-line detailed technical log documenting Phase 2 implementation
- **35 AWS Resources Deployed**: Complete infrastructure via Terraform (S3, IAM, Glue, Secrets)
- **Comprehensive Documentation**: 4,670+ lines across 13 files
- **IaC Automation**: 95% coverage with Terraform (6 modules, 25 files)
- **Project Timeline**: Ahead of schedule for Dec 13 completion (43% complete, 8.5 of 20 days)
- **Remaining Tasks**: Glue workflows/triggers, end-to-end pipeline testing

### AWS Data Lake Pipeline (Nov 18, 2025)

- Complete event-driven data pipeline with Terraform IaC
- Three-layer architecture: Ingestion, Storage, Processing
- Serverless ETL with Lambda, S3, and EventBridge
- Automated deployment and testing scripts
- Production-ready security and monitoring

### Heart Disease Prediction (Nov 08, 2025)

- Complete ML pipeline with k-NN classification
- Comprehensive data cleaning with median imputation
- EDA with correlation analysis and feature visualization
- Hyperparameter tuning using GridSearchCV
- Multi-metric evaluation (accuracy, precision, recall, F1, AUC, cross-validation)

### DynamoDB Inventory System (Oct 29, 2025)

- Initiated project for managing inventory using DynamoDB

### hypothesis-testing (Oct 23, 2025)

- Created SYNC_SUMMARY.md documenting synchronization process
- Updated README.md with improved project documentation
- Added create_test.py for automated test generation

---

***"Building tools that make developers' lives easier, one line of code at a time."***
