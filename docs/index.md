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

### StreamForge Real-Time Streaming Platform ⚡

A real-time data streaming and processing platform demonstrating modern stream processing architecture with Apache Kafka, Apache Flink, and dual deployment models (local + AWS production).

- **Tech Stack**: Apache Kafka, Apache Flink (Java 11), MongoDB, Docker Compose, Maven, AWS (DynamoDB, Amplify), Terraform
- **Features**: Event-driven streaming, custom Flink sinks, containerized infrastructure, dual deployment strategy (local/AWS)
- **Highlights**: Complete Docker orchestration (5 services), custom MongoDB sink with lifecycle management, Maven build with Shade plugin, comprehensive unit tests
- **Skills**: Stream Processing, Event-Driven Architecture, Apache Kafka, Apache Flink, Java, Docker, Container Orchestration, Real-Time Data Processing
- [View Project](streamforge.md)

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

- **Real-Time Stream Processing**: Apache Kafka and Apache Flink for event-driven data pipelines
- **Data Lakehouse Architecture**: Multi-layer data platforms with raw, processed, and curated zones
- **CDC Replication**: Real-time data capture with AWS DMS and streaming ingestion
- **Serverless ETL**: PySpark and Lambda-based data transformation at scale
- **Open Table Formats**: Apache Hudi for ACID transactions on data lakes
- **Event-Driven Architecture**: S3 triggers, EventBridge orchestration, Kafka messaging
- **Container Orchestration**: Docker Compose multi-service environments
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
**Cloud & Infrastructure**: AWS (DMS, DataSync, Glue, Athena, Lambda, S3, EventBridge, EC2, DynamoDB, Amplify), Terraform (IaC with 95% automation)  
**Databases**: PostgreSQL, DynamoDB, MongoDB  
**Data Engineering**: Apache Kafka, Apache Flink, Apache Hudi, PySpark, Pandas, Event-Driven Architecture, Stream Processing, ETL Pipelines, CDC Replication  
**Infrastructure as Code**: Terraform modules, Docker Compose, multi-environment deployment, remote state management  
**Build Tools**: Maven, pytest, pip  
**Tools**: Git, Docker, pytest, AWS CLI, psycopg2, mkdocs

## 📝 Latest Updates

### StreamForge Real-Time Streaming Platform (Dec 18, 2025)

**Phase 1 Complete** (40% overall progress):
- ✅ **Complete Docker Infrastructure**: Kafka, Flink (JobManager + TaskManager), MongoDB, Zookeeper orchestration
- ✅ **Apache Flink Stream Processing**: StreamProcessor.java with Kafka source and custom MongoDB sink
- ✅ **Custom MongoDB Sink**: RichSinkFunction with connection lifecycle management
- ✅ **Maven Build System**: Fat JAR packaging with Shade plugin, provided scopes for Flink dependencies
- ✅ **Unit Testing**: Comprehensive tests for StreamProcessor, MongoDBSink, and schema validation
- 🎯 **Phase 2 In Progress**: Windowed aggregations, stateful operations, MongoDB schema design
- **Tech Stack**: Apache Kafka 3.5.1, Apache Flink 1.18.0, MongoDB 7.0, Java 11, Docker Compose
- **Next Phase**: Advanced stream processing (windowing, keyed state), AWS deployment with Terraform

### AutoCorp Cloud Data Lake Pipeline (Dec 7, 2025)

**Phase 2 Complete - Ready for Phase 3** (50% overall progress):
- ✅ **Phase 2 Complete (100%)**: All AWS Glue ETL with Apache Hudi operational
- ✅ **7 Hudi Tables Tested**: auto_parts, customers, service, service_parts + 3 sales tables ready
- ✅ **35+ Data Quality Rules**: Comprehensive validation framework implemented
- ✅ **End-to-End Testing**: <15 minute data latency validated
- ✅ **2 Glue Crawlers Operational**: Automated schema discovery working
- 📝 **Phase 2.5 Planned**: 1M sales orders to be generated (300K PostgreSQL + 700K CSV)
- 🎯 **Next Phase**: DMS CDC Replication & DataSync (Dec 9-13)
- **Infrastructure**: 35 AWS resources, 95% IaC automation
- **Documentation**: 4,670+ lines across 13 files
- **Timeline**: On track for Dec 20 completion (50% complete, 10 of 20 days)

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
