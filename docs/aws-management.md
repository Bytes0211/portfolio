# AWS Manager ☁️

A Python-based AWS service management library providing simplified interfaces for AWS Lambda, S3, and EC2 operations.

[Repository](https://github.com/Bytes0211/aws-manager)

## ✨ Features

- **Lambda Management** ⚡: Invoke, update, and list Lambda functions
- **S3 Operations** 🪣: Bucket creation, file uploads, versioning, and batch operations
- **EC2 Management** 🖥️: Instance creation, starting, stopping, and termination
- **Lambda Deployment** 📦: Complete deployment pipeline with dependency packaging

## Key Components

### aws.py

Contains the Aws Class which is a centralized AWS client management for various services. Abstracts Boto3 methods for various services.

***Code Snippet - method to create ec2***

```py
    def create_ec2(self, image_id: str, instance_type: str = 't2.micro', min_count: int = 1, max_count: int = 1, key_name: str = None, security_group_ids: list = None, subnet_id: str = None, tags: list = None) -> tuple: 
        """Create EC2 instance(s) with specified configuration."""
        try:
            params = {
                'ImageId': image_id,
                'InstanceType': instance_type,
                'MinCount': min_count,
                'MaxCount': max_count
            }
            
            if key_name:
                params['KeyName'] = key_name
            if security_group_ids:
                params['SecurityGroupIds'] = security_group_ids
            if subnet_id:
                params['SubnetId'] = subnet_id
            if tags:
                params['TagSpecifications'] = [{
                    'ResourceType': 'instance',
                    'Tags': tags
                }]
            
            instances = self.ec2_resource.create_instances(**params) # type: ignore
            instance_ids = [instance.id for instance in instances]
            print(f"✅ EC2 instance(s) created successfully: {', '.join(instance_ids)}")
            return 200, instance_ids
        except ClientError as err:
            print(f"❌ Error creating EC2 instance: {err.response['Error']['Code']} - {err.response['Error']['Message']}")
            raise
```

### aws_manager.py

Contains the AWSManager class which is used to make calls to aws.py and manages arguments for Aws class and environment variabls. Static methods to used for ease of use.

***Code Snippet - invoke function***

Not really useful in production, but great for designing and testing lambdas.

```py
    @staticmethod
    def invoke_lambda(function_name: str, payload: dict = None, region_name: str = None, aws_access_key_id: str = None, aws_secret_access_key: str = None, aws_session_token: str = None) -> tuple:
        """Invoke a Lambda function with the given payload."""
        aws_manager = AWSManager(region_name, aws_access_key_id, aws_secret_access_key, aws_session_token)
        return aws_manager.aws.invoke_lambda(function_name, payload)
```

## Summary

AWS Manager is a comprehensive Python library that simplifies AWS service interactions through a clean, object-oriented interface. The library consists of two main components: the `Aws` class for direct service operations and the `AWSManager` class for higher-level management with static helper methods. It supports essential AWS services including Lambda function invocation and deployment, S3 bucket and file operations, and EC2 instance lifecycle management. The library is particularly useful for development and testing workflows, providing streamlined methods for common AWS tasks while handling authentication and error management automatically.