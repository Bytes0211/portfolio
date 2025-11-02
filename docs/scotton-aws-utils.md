# Scotton AWS Utils ⚙️

A comprehensive Python package for AWS service operations, providing a unified interface for S3, Lambda, EC2, IAM, and DynamoDB operations with simplified error handling and best practices built-in.

[Repository](https://github.com/Bytes0211/scotton-aws-utils)

## ✨ Features

- **S3 Operations** 🪣: Bucket management, file uploads/downloads, versioning
- **Lambda Functions** ⚡: Invoke, update code, manage configurations
- **EC2 Management** 🖥️: Create, start, stop, and manage EC2 instances
- **IAM Operations** 🔐: Role validation and management
- **DynamoDB Operations** 🗄️: Full CRUD operations, queries, scans, batch operations
- **Advanced DynamoDB** 🚀: Key/Attr condition builders, streams, GSI/LSI support
- **Unified Error Handling** ✅: Consistent error handling across all services
- **Local DynamoDB Support** 💻: Easy testing with DynamoDB Local
- **Atomic Transactions** 🔒: ACID-compliant multi-item operations
- **Package Distribution** 📦: Pip-installable Python package

## Key Components

### aws.py

Contains the `Aws` class which provides centralized AWS client management for all AWS services. Features lazy initialization of clients and abstracts complex Boto3 operations into simple, intuitive methods.

**Key Features:**
- Lazy client initialization for optimal resource usage
- Support for both AWS and local DynamoDB endpoints
- Comprehensive error handling with informative messages
- Automatic pagination for DynamoDB scan operations
- Advanced DynamoDB features (transactions, batch operations)

***Code Snippet - DynamoDB Query with Conditions***

```python
from scotton_aws_utils import Aws
from boto3.dynamodb.conditions import Key, Attr

aws = Aws()

# Query with complex conditions
orders = aws.query_dynamodb(
    table_name='Orders',
    key_condition_expression=Key('customer_id').eq('CUST-123') & 
                            Key('order_date').begins_with('2025'),
    filter_expression=Attr('total').gt(100),
    scan_index_forward=False,  # Most recent first
    limit=50
)
```

### util.py

Provides utility functions for creating AWS clients and managing environment variables. Centralizes configuration management and client factory methods.

**Key Features:**
- Client factory functions for all AWS services
- Environment variable management
- Custom endpoint support for local testing
- Region configuration

***Code Snippet - Client Factory Functions***

```python
from scotton_aws_utils import util

# Get AWS clients with automatic region detection
s3_client = util.get_s3_client()
lambda_client = util.get_lambda_client()
dynamodb_client = util.get_dynamodb_client()
dynamodb_resource = util.get_dynamodb_resource()

# With custom region/endpoint for local testing
dynamodb_client = util.get_dynamodb_client(
    region_name='us-west-2',
    endpoint_url='http://localhost:8000'
)

# Environment configuration
app_name = util.get_appName()
env = util.get_env()
```

### lambdadeployer.py

Contains deployment utilities for AWS Lambda functions, including dependency packaging and code updates.

**Key Features:**
- Automated dependency packaging
- Lambda function deployment
- Configuration management
- Environment variable updates

***Code Snippet - Lambda Deployment***

```python
from scotton_aws_utils import Aws

aws = Aws()

# Update Lambda function code
with open('function.zip', 'rb') as f:
    deployment_package = f.read()

status, response = aws.update_function_code(
    function_name='my-function',
    deployment_package=deployment_package
)

# Update environment variables
env_vars = {
    'DATABASE_URL': 'dynamodb-table-name',
    'LOG_LEVEL': 'INFO'
}

status, response = aws.update_function_configuration(
    function_name='my-function',
    env_vars=env_vars
)
```

## Advanced DynamoDB Features

### Conditional Updates

The package provides robust support for conditional updates, ensuring data integrity:

```python
from scotton_aws_utils import Aws

aws = Aws()

# Update only if condition is met (e.g., stock management)
aws.update_item_dynamodb(
    table_name='Inventory',
    key={'id': 'item-123'},
    update_expression='SET stock = stock - :qty',
    expression_attribute_values={':qty': 5, ':min': 0},
    condition_expression='stock >= :min'
)
```

### Atomic Transactions

Execute multiple operations atomically - all succeed or all fail:

***Code Snippet - Transaction Example***

```python
# Transfer between accounts with atomic guarantee
transaction = [
    {
        'Update': {
            'TableName': 'Accounts',
            'Key': {'account_id': {'S': 'acct-123'}},
            'UpdateExpression': 'SET balance = balance - :amount',
            'ExpressionAttributeValues': {':amount': {'N': '100'}}
        }
    },
    {
        'Update': {
            'TableName': 'Accounts',
            'Key': {'account_id': {'S': 'acct-456'}},
            'UpdateExpression': 'SET balance = balance + :amount',
            'ExpressionAttributeValues': {':amount': {'N': '100'}}
        }
    },
    {
        'Put': {
            'TableName': 'Transactions',
            'Item': {
                'id': {'S': 'txn-789'},
                'from': {'S': 'acct-123'},
                'to': {'S': 'acct-456'},
                'amount': {'N': '100'}
            }
        }
    }
]

status, response = aws.transact_write_dynamodb(transaction)
```

### Batch Operations

Efficiently process multiple items in a single request:

```python
from scotton_aws_utils import Aws

aws = Aws()

# Batch get multiple items (up to 100)
keys = [{'id': 'item-1'}, {'id': 'item-2'}, {'id': 'item-3'}]
items = aws.batch_get_dynamodb('Products', keys)

# Batch write multiple items (up to 25)
items = [
    {'id': 'item-1', 'name': 'Product 1', 'price': 29.99},
    {'id': 'item-2', 'name': 'Product 2', 'price': 39.99}
]
unprocessed = aws.batch_write_dynamodb('Products', items)
```

## Local Development Workflow

### Setting Up Local DynamoDB

The package seamlessly supports local DynamoDB development:

1. **Run DynamoDB Locally**: Use Docker or download DynamoDB Local
2. **Connect to Local Instance**: Simply pass `use_local_dynamodb=True`
3. **Develop and Test**: Work with local data during development
4. **Migrate to AWS**: Copy tables to production when ready

**Example Workflow:**

```python
from scotton_aws_utils import Aws
from boto3.dynamodb.conditions import Key

# 1. Work with local DynamoDB during development
local_aws = Aws(use_local_dynamodb=True)

# Create test table locally
local_aws.create_dynamodb_table(
    table_name='products',
    key_schema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
    attribute_definitions=[{'AttributeName': 'id', 'AttributeType': 'S'}]
)

# Add test data
local_aws.put_item_dynamodb('products', {'id': 'prod-1', 'name': 'Test Product'})

# 2. Test queries locally
items = local_aws.scan_dynamodb('products')
print(f"Found {len(items)} products locally")

# 3. When ready, migrate to AWS
prod_aws = Aws(use_local_dynamodb=False)
status, message = prod_aws.copy_table_to_aws('products', 'products-prod')
print(message)  # ✅ TABLE products-prod CREATED AND DATA MIGRATED
```

## Installation

### From Source (Development)

```bash
# Clone or navigate to the package directory
cd ~/dev/projects/scotton-aws-utils

# Install in editable mode
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

### From Git Repository

```bash
pip install git+https://github.com/Bytes0211/scotton-aws-utils.git
```

### Package Import

```python
from scotton_aws_utils import Aws
from scotton_aws_utils import util

# Initialize AWS client
aws = Aws()

# S3 Operations
aws.list_buckets()
aws.add_file_to_bucket('my-bucket', 'file.txt', 'uploaded-file.txt')

# Lambda Operations
aws.list_functions()
response = aws.invoke_function('my-function', {'key': 'value'})

# EC2 Operations
aws.list_ec2s()
status, instance_ids = aws.create_ec2(image_id='ami-12345678')
```

## Configuration

The package uses environment variables for configuration. Create a `.env` file:

```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# Application-specific
env=development
appName=my-app
```

## API Reference

### Main Classes

#### `Aws`

Main class for AWS operations with lazy-initialized clients.

**Constructor:**
- `Aws(use_local_dynamodb=False)`: Initialize with optional local DynamoDB support

**S3 Methods:**
- `create_bucket(bucket_prefix)`: Create S3 bucket
- `list_buckets()`: List all buckets
- `add_file_to_bucket(bucket_name, file_name, object_name, url=None)`: Upload file
- `delete_files_from_bucket(bucket_name, file_list)`: Delete multiple files
- `enable_bucket_versioning(bucket_name)`: Enable versioning

**Lambda Methods:**
- `list_functions()`: List Lambda functions
- `invoke_function(function_name, function_params, get_log=False)`: Invoke function
- `update_function_code(function_name, deployment_package)`: Update code
- `update_function_configuration(function_name, env_vars)`: Update configuration

**DynamoDB Methods:**
- `create_dynamodb_table(...)`: Create table with GSI/LSI/streams support
- `put_item_dynamodb(table_name, item)`: Insert/update item
- `get_item_dynamodb(table_name, key)`: Get item by key
- `update_item_dynamodb(table_name, key, update_expression, ...)`: Update with conditions
- `delete_item_dynamodb(table_name, key)`: Delete item
- `query_dynamodb(table_name, key_condition_expression, ...)`: Query with Key/Attr
- `scan_dynamodb(table_name, filter_expression, ...)`: Scan with filters
- `batch_get_dynamodb(table_name, keys)`: Batch get up to 100 items
- `batch_write_dynamodb(table_name, items)`: Batch write up to 25 items
- `transact_write_dynamodb(transact_items)`: Atomic transactions
- `list_dynamodb_tables()`: List all tables
- `delete_dynamodb_table(table_name)`: Delete table
- `get_table_schema(table_name)`: Get table schema
- `copy_table_to_aws(source_table_name, destination_table_name)`: Migrate table

**EC2 Methods:**
- `create_ec2(image_id, ...)`: Create EC2 instance
- `list_ec2s()`: List all instances
- `start_ec2(instance_ids)`: Start instances
- `stop_ec2(instance_ids)`: Stop instances
- `remove_ec2s(instance_ids)`: Terminate instances

**IAM Methods:**
- `list_iam_roles()`: List IAM roles
- `validate_iam_role(role)`: Validate role exists

## Project Structure

```
scotton-aws-utils/
├── scotton_aws_utils/
│   ├── __init__.py                 # Package initialization and exports
│   ├── aws.py                      # Core AWS service wrapper
│   ├── util.py                     # Client factories and utilities
│   └── lambdadeployer.py           # Lambda deployment utilities
├── pyproject.toml                  # Package configuration and dependencies
├── MANIFEST.in                     # Package manifest for distribution
├── README.md                       # Complete API documentation
├── LICENSE                         # MIT License
├── PACKAGE_CREATION_GUIDE.md       # Package creation documentation
├── MIGRATION_REPORT.md             # Migration guide from local files
└── FINAL_SUMMARY.md                # Project summary and usage
```

## Architecture Highlights

### Lazy Client Initialization

The `Aws` class uses lazy initialization to create AWS service clients only when needed:

```python
@property
def dynamodb_client(self):
    if self._dynamodb_client is None:
        self._dynamodb_client = util.get_dynamodb_client(
            local=self._use_local_dynamodb
        )
    return self._dynamodb_client
```

### Dual Environment Support

Seamlessly switch between AWS and local DynamoDB:

```python
# Connect to AWS
aws_client = Aws(use_local_dynamodb=False)

# Connect to local DynamoDB (localhost:8000)
local_client = Aws(use_local_dynamodb=True)
```

### Automatic Pagination

DynamoDB scan and query operations automatically handle pagination:

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

## Summary

Scotton AWS Utils is a comprehensive Python package that simplifies AWS service interactions through a clean, object-oriented interface. The package provides a unified `Aws` class with support for multiple AWS services and advanced features.

**Key Capabilities:**
- **Multi-Service Support**: S3, Lambda, EC2, IAM, and DynamoDB operations
- **Advanced DynamoDB**: Transactions, batch operations, conditional updates, Key/Attr conditions
- **Local Development**: Full DynamoDB local support for cost-free development
- **Package Distribution**: Pip-installable with proper versioning and dependencies
- **Production Ready**: Robust error handling, pagination, and best practices
- **Developer Friendly**: Clean API, extensive documentation, and easy migration

The package is particularly useful for development workflows requiring multiple AWS services, providing streamlined methods for common tasks while handling authentication, pagination, and error management automatically. The dual-environment support allows developers to work entirely with local DynamoDB during development, then switch to AWS with a single parameter change.

## Migration Guide

### From Local aws.py/util.py

If you're migrating from local `aws.py` and `util.py` files:

**Before:**
```python
from resources.aws import Aws
import resources.util as util
```

**After:**
```python
from scotton_aws_utils import Aws
from scotton_aws_utils import util
```

All method signatures remain the same, making migration seamless.

## Repository

[View on GitHub](https://github.com/Bytes0211/scotton-aws-utils)

---

[← Back to Cloud Computing](cloud-compute.md)
