# AWS Manager ☁️

**Last Updated:** October 27, 2025

A Python-based AWS service management library providing simplified interfaces for AWS Lambda, S3, EC2, and DynamoDB operations.

[Repository](https://github.com/Bytes0211/aws-manager)

## ✨ Features

- **Lambda Management** ⚡: Invoke, update, and list Lambda functions
- **S3 Operations** 🪣: Bucket creation, file uploads, versioning, and batch operations
- **EC2 Management** 🖥️: Instance creation, starting, stopping, and termination
- **DynamoDB Operations** 🗄️: Table management and full CRUD operations (AWS & Local)
- **Local DynamoDB Support** 💻: Connect to localhost DynamoDB for development/testing
- **Table Migration** 🚀: Migrate tables from local DynamoDB to AWS with schema and data
- **Lambda Deployment** 📦: Complete deployment pipeline with dependency packaging
- **Comprehensive Testing** ✅: Full unit test suite with moto for AWS service mocking

## Key Components

### aws.py

Contains the `Aws` class which provides centralized AWS client management for Lambda, S3, EC2, and DynamoDB services. Features lazy initialization of clients and abstracts complex Boto3 operations into simple, intuitive methods.

**Key Features:**
- Lazy client initialization for optimal resource usage
- Support for both AWS and local DynamoDB endpoints
- Comprehensive error handling with informative messages
- Automatic pagination for DynamoDB scan operations
- Batch operations for efficient bulk data handling

***Code Snippet - DynamoDB Table Creation***

```py
def create_dynamodb_table(self, table_name: str, key_schema: list, attribute_definitions: list, 
                          provisioned_throughput: dict = None, billing_mode: str = 'PAY_PER_REQUEST',
                          global_secondary_indexes: list = None, local_secondary_indexes: list = None,
                          tags: list = None) -> tuple:
    """Create DynamoDB table with specified configuration."""
    try:
        params = {
            'TableName': table_name,
            'KeySchema': key_schema,
            'AttributeDefinitions': attribute_definitions,
            'BillingMode': billing_mode
        }
        
        # Only add ProvisionedThroughput if billing mode is PROVISIONED
        if billing_mode == 'PROVISIONED':
            if provisioned_throughput:
                params['ProvisionedThroughput'] = provisioned_throughput
            else:
                params['ProvisionedThroughput'] = {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
        
        if global_secondary_indexes:
            params['GlobalSecondaryIndexes'] = global_secondary_indexes
        if local_secondary_indexes:
            params['LocalSecondaryIndexes'] = local_secondary_indexes
        if tags:
            params['Tags'] = tags
        
        table = self.dynamodb_resource.create_table(**params)
        table.wait_until_exists()
        print(f"✅ DynamoDB table '{table_name}' created successfully")
        return 200, table
    except ClientError as err:
        print(f"❌ Error creating DynamoDB table: {err.response['Error']['Code']} - {err.response['Error']['Message']}")
        raise
```

### aws_manager.py

Contains the `AWSManager` class with static methods for easy access to AWS operations. Manages environment variables and provides a clean interface for all AWS services.

**Key Features:**
- Static methods for simplified API
- Automatic credential management from environment
- Consistent return types across all methods
- Support for both AWS and local DynamoDB operations

***Code Snippet - DynamoDB Operations***

```py
@staticmethod
def put_item_dynamodb(table_name: str, item: dict) -> tuple:
    """Insert or update item in DynamoDB table."""
    aws = Aws()
    return aws.put_item_dynamodb(table_name, item)

@staticmethod
def get_item_dynamodb(table_name: str, key: dict) -> dict:
    """Retrieve item from DynamoDB table by key."""
    aws = Aws()
    return aws.get_item_dynamodb(table_name, key)

@staticmethod
def copy_table_to_aws(source_table_name: str, destination_table_name: str = None) -> tuple:
    """Copy a table from local DynamoDB to AWS DynamoDB."""
    aws = Aws(use_local_dynamodb=False)
    return aws.copy_table_to_aws(source_table_name, destination_table_name)
```

### test_dynamodb.py

Comprehensive unit test suite covering all DynamoDB operations using pytest and moto for AWS service mocking.

**Test Coverage:**
- ✅ Table creation with various billing modes and schemas
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ Batch operations and pagination
- ✅ Table migration from local to AWS
- ✅ Edge cases and error handling

***Code Snippet - Example Test***

```py
@mock_aws
def test_put_and_get_item(self, aws_credentials, dynamodb_table_config):
    """Test that after put_item_dynamodb, get_item_dynamodb retrieves the correct item."""
    # Create table
    AWSManager.create_dynamodb_table(
        table_name=dynamodb_table_config['table_name'],
        key_schema=dynamodb_table_config['key_schema'],
        attribute_definitions=dynamodb_table_config['attribute_definitions'],
        billing_mode='PAY_PER_REQUEST'
    )
    
    # Put item
    test_item = {
        'id': 'test-id-123',
        'name': 'Test Item',
        'value': 42,
        'active': True
    }
    
    status_code, response = AWSManager.put_item_dynamodb(
        table_name=dynamodb_table_config['table_name'],
        item=test_item
    )
    
    assert status_code == 200
    
    # Get item and verify
    retrieved_item = AWSManager.get_item_dynamodb(
        table_name=dynamodb_table_config['table_name'],
        key={'id': 'test-id-123'}
    )
    
    assert retrieved_item == test_item
```

## DynamoDB Development Workflow

### Local Development

The library provides comprehensive support for local DynamoDB development:

1. **Setup Local DynamoDB**: Run DynamoDB locally using Docker or direct download
2. **Create Test Data**: Use `dynamodb_local_setup.py` to populate test tables
3. **Scan and Query**: Use `dynamodb_scan.py` to inspect local data
4. **Migrate to AWS**: Use `dynamodb_migrate.py` or `copy_table_to_aws()` to deploy

**Example Workflow:**

```python
from aws_manager import AWSManager

# 1. Work with local DynamoDB during development
employees = AWSManager.scan_dynamodb_local('employee')
print(f"Found {len(employees)} employees locally")

# 2. Test queries locally
from boto3.dynamodb.conditions import Key
engineers = AWSManager.query_dynamodb_local(
    table_name='employee',
    key_condition_expression=Key('department').eq('Engineering')
)

# 3. When ready, migrate to AWS
status, message = AWSManager.copy_table_to_aws('employee', 'employee-prod')
print(message)  # ✅ TABLE employee-prod CREATED AND 6 ITEMS MIGRATED

# 4. Verify on AWS
aws_employees = AWSManager.scan_dynamodb('employee-prod')
print(f"Migrated {len(aws_employees)} employees to AWS")
```

### Helper Scripts

**dynamodb_local_setup.py**: Creates sample employee table with test data  
**dynamodb_scan.py**: Scans and displays local DynamoDB tables  
**dynamodb_migrate.py**: CLI tool for migrating tables from local to AWS

```bash
# Create test data locally
python dynamodb_local_setup.py

# View local data
python dynamodb_scan.py

# Migrate to AWS
python dynamodb_migrate.py employee employee-prod
```

## Testing Infrastructure

The project includes a comprehensive unit test suite with **16 test cases** covering all DynamoDB operations:

- **Test Framework**: pytest with moto for AWS mocking
- **Zero AWS Costs**: All tests run locally with mocked services
- **Coverage**: CRUD operations, migrations, edge cases, and error handling
- **Fast Execution**: No network latency or API calls

**Running Tests:**

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
pytest test_dynamodb.py -v

# Run with coverage report
pytest test_dynamodb.py --cov=aws_manager --cov=resources.aws --cov-report=html
```

## Architecture Highlights

### Lazy Client Initialization

The `Aws` class uses the lazy initialization pattern to create AWS service clients only when needed, optimizing resource usage:

```python
@property
def dynamodb_client(self):
    if self._dynamodb_client is None:
        self._dynamodb_client = util.get_dynamodb_client(local=self._use_local_dynamodb)
    return self._dynamodb_client
```

### Dual Environment Support

Seamlessly switch between AWS and local DynamoDB by passing a single parameter:

```python
# Connect to AWS
aws_client = Aws(use_local_dynamodb=False)

# Connect to local DynamoDB (localhost:8000)
local_client = Aws(use_local_dynamodb=True)
```

### Automatic Pagination

DynamoDB scan operations automatically handle pagination for large datasets:

```python
def scan_dynamodb(self, table_name: str, ...) -> list:
    response = table.scan(**params)
    items = response.get('Items', [])
    
    # Handle pagination for large tables
    while 'LastEvaluatedKey' in response:
        params['ExclusiveStartKey'] = response['LastEvaluatedKey']
        response = table.scan(**params)
        items.extend(response.get('Items', []))
    
    return items
```

## Project Structure

```
aws-manager/
├── aws_manager.py                    # Main AWSManager class
├── resources/
│   ├── aws.py                       # Core AWS service wrapper
│   ├── lambdadeployer.py            # Lambda deployment utilities
│   └── util.py                      # Client factories and utilities
├── test_dynamodb.py                 # Comprehensive test suite (16 tests)
├── dynamodb_scan.py                 # Local DynamoDB inspection tool
├── dynamodb_migrate.py              # Table migration CLI tool
├── dynamodb_local_setup.py          # Test data generator
├── requirements.txt                 # Production dependencies
├── requirements-test.txt            # Test dependencies (pytest, moto)
├── README.md                        # Complete API documentation
├── DYNAMODB_WORKFLOW.md             # DynamoDB workflow guide
├── QUICKSTART_DYNAMODB.md           # Quick start guide
├── TEST_README.md                   # Testing documentation
└── aws_lambda_deployment_guide.md   # Lambda deployment guide
```

## Summary

AWS Manager is a comprehensive Python library that simplifies AWS service interactions through a clean, object-oriented interface. The library consists of two main components: the `Aws` class for direct service operations and the `AWSManager` class for higher-level management with static helper methods.

**Key Capabilities:**
- **Multi-Service Support**: Lambda, S3, EC2, and DynamoDB operations
- **Local Development**: Full DynamoDB local support for cost-free development
- **Migration Tools**: Seamlessly migrate tables from local to AWS
- **Comprehensive Testing**: 16 unit tests with moto for AWS service mocking
- **Production Ready**: Robust error handling, pagination, and batch operations
- **Developer Friendly**: Clean API, extensive documentation, and helper scripts

The library is particularly useful for development and testing workflows, providing streamlined methods for common AWS tasks while handling authentication, pagination, and error management automatically. The dual-environment support allows developers to work entirely with local DynamoDB during development, then migrate to AWS with a single command when ready for production.

## Repository

[View on GitHub](https://github.com/Bytes0211/aws-manager)

---

[← Back to Cloud Computing](cloud-compute.md)
