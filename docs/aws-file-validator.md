# AWS File Validator Lambda

**Last Updated:** October 27, 2025

A Java project that validates file formats (CSV/JSON) using AWS Lambda and uploads validated files to S3.

## Overview

The AWS File Validator iis a serverless application built with Java that provides automated validation for CSV and JSON files. It leverages AWS Lambda for scalable, event-driven processing and integrates with S3 for secure storage of validated files.

## Features

- **File Format Validation**: Validates CSV and JSON file formats
- **AWS Lambda Integration**: Serverless processing of file validation
- **S3 Upload**: Automatically uploads validated files to S3 bucket
- **Structured Validation**: 
  - CSV: Checks headers, row consistency, and format
  - JSON: Validates JSON structure and reports element counts
- **Local Testing**: Test Lambda functions locally before deployment

## Tech Stack

- **Java 11+**
- **AWS Lambda** - Serverless compute
- **AWS S3** - Object storage
- **Maven** - Build automation
- **AWS SDK for Java v2** - AWS service integration
- **Jackson** - JSON processing
- **Apache Commons CSV** - CSV parsing

## Project Structure

```java path=null start=null
aws-file-validator/
├── src/main/java/com/awsproject/
│   ├── lambda/
│   │   └── FileValidatorHandler.java    # Lambda function handler
│   ├── service/
│   │   └── S3Service.java               # S3 upload service
│   ├── validator/
│   │   ├── FileValidator.java           # Validator interface
│   │   ├── CsvValidator.java            # CSV validation logic
│   │   └── JsonValidator.java           # JSON validation logic
│   ├── model/
│   │   └── ValidationResult.java        # Validation result model
│   └── LocalTester.java                 # Local testing utility
├── sample-files/
│   ├── sample.csv                       # Sample CSV file
│   └── sample.json                      # Sample JSON file
├── pom.xml                              # Maven configuration
├── deploy.sh                            # Lambda deployment script
└── test-lambda.sh                       # Lambda testing script
```

## Key Capabilities

### CSV Validation
- Ensures file is not empty
- Verifies at least one data record exists (excluding header)
- Validates all rows have consistent column count
- Checks proper CSV format using Apache Commons CSV

### JSON Validation
- Ensures file is not empty
- Validates JSON structure using Jackson parser
- Supports both JSON objects and arrays
- Reports element counts

## Usage

### Lambda Input Format
```json path=null start=null
{
  "fileName": "data.csv",
  "content": "header1,header2\nvalue1,value2",
  "fileType": "CSV",
  "bucketName": "your-bucket-name"
}
```

### Lambda Output Format
**Success Response:**
```json path=null start=null
{
  "statusCode": 200,
  "valid": true,
  "message": "File validated and uploaded successfully",
  "validationDetails": "Valid CSV with 3 records and 4 columns",
  "s3Key": "validated/csv/1234567890_data.csv",
  "s3Uri": "s3://your-bucket-name/validated/csv/1234567890_data.csv"
}
```

## Deployment

The project includes automated deployment scripts:

```bash path=null start=null
# Build and deploy to AWS Lambda
./deploy.sh

# Test the deployed function
./test-lambda.sh your-bucket-name
```

## Local Development

Test locally before deploying:

```bash path=null start=null
# Build the project
mvn clean package

# Test with sample CSV
mvn exec:java -Dexec.mainClass="com.awsproject.LocalTester" \
  -Dexec.args="your-bucket-name sample-files/sample.csv CSV"

# Test with sample JSON
mvn exec:java -Dexec.mainClass="com.awsproject.LocalTester" \
  -Dexec.args="your-bucket-name sample-files/sample.json JSON"
```

## Architecture Highlights

- **Extensible Design**: Easy to add new file format validators
- **Serverless**: No server management, automatic scaling
- **Secure**: Uses IAM roles and AWS credentials
- **Organized Storage**: Files uploaded with structured naming pattern

## Learning Outcomes

This project demonstrates:
- AWS Lambda function development in Java
- Integration with AWS S3 for file storage
- Implementation of validation patterns using interfaces
- Serverless application deployment
- Local testing strategies for cloud functions
- Maven build configuration for AWS Lambda

## Repository

[View on GitHub](https://github.com/Bytes0211/aws-file-validator)

---

[← Back to Java Projects](java.md)
