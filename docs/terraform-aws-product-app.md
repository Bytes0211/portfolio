# AWS Product Management Application - Terraform Infrastructure 🏗️

**Last Updated:** October 27, 2025

A complete Infrastructure as Code (IaC) project using Terraform to deploy a full-stack serverless product management application on AWS, demonstrating modern cloud architecture patterns.

## ✨ Features

- **Infrastructure as Code** 📝: Complete AWS infrastructure defined in Terraform
- **Full-Stack Application** 🌐: Spring Boot web app with serverless backend
- **VPC Networking** 🔒: Secure network architecture with public/private subnets
- **Serverless Processing** ⚡: Lambda function for business logic
- **NoSQL Storage** 🗄️: DynamoDB for persistent data storage
- **Automated Deployment** 🚀: One-command infrastructure provisioning
- **Comprehensive Testing** ✅: Unit tests for both Spring Boot and Lambda

## Architecture

### Component Interaction Flow

```
User → Nginx (Port 80) → Spring Boot (Port 8080) → AWS Lambda → DynamoDB
                                                          ↓
                                                    CloudWatch Logs
```

### Infrastructure Components

#### Networking Layer
- **VPC** with DNS support enabled
- **Public Subnet** (10.0.1.0/24) with Internet Gateway
- **Private Subnet** (10.0.2.0/24) with NAT Gateway
- **Route Tables** configured for public and private subnets
- **Security Groups** for EC2 and Lambda functions

#### Compute & Application Layer
- **EC2 Instance** (t2.micro, Ubuntu 22.04) in the public subnet
  - Elastic IP attached for consistent access
  - Nginx web server as reverse proxy
  - Java 17 and Maven installed
  - Spring Boot application running on port 8080
  - IAM role with Lambda invoke permissions

#### Serverless & Storage Layer
- **Lambda Function** (Python 3.11) in the private subnet
  - Processes product data and saves to DynamoDB
  - VPC-enabled with proper security group
  - IAM role with DynamoDB write permissions
- **DynamoDB Table** for storing product information
  - Pay-per-request billing mode
  - Composite key: productId (hash) + date (range)

## Technology Stack

**Infrastructure**: Terraform  
**Backend**: Spring Boot (Java 17), AWS Lambda (Python 3.11)  
**Storage**: DynamoDB  
**Compute**: EC2, Lambda  
**Networking**: VPC, Security Groups, NAT Gateway  
**Web Server**: Nginx  
**Build Tools**: Maven, Terraform  

## Application Features

The Spring Boot web application provides a form to enter:
- Product Name
- Product ID
- Sales Price
- Date
- Salesperson

When submitted, the application invokes the Lambda function which saves the data to DynamoDB.

## Key Components

### Terraform Configuration Files

***vpc.tf - Network Infrastructure***

```hcl
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "product-app-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidr
  availability_zone       = data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = true

  tags = {
    Name = "product-app-public-subnet"
  }
}

resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidr
  availability_zone = data.aws_availability_zones.available.names[1]

  tags = {
    Name = "product-app-private-subnet"
  }
}
```

***lambda.tf - Lambda Function Configuration***

```hcl
resource "aws_lambda_function" "product_processor" {
  filename      = "lambda/function.zip"
  function_name = "product-app-product-processor"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.lambda_handler"
  runtime       = "python3.11"
  timeout       = 30

  vpc_config {
    subnet_ids         = [aws_subnet.private.id]
    security_group_ids = [aws_security_group.lambda_sg.id]
  }

  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.products.name
    }
  }

  tags = {
    Name = "product-app-processor"
  }
}
```

***dynamodb.tf - DynamoDB Table***

```hcl
resource "aws_dynamodb_table" "products" {
  name           = "product-app-products"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "productId"
  range_key      = "date"

  attribute {
    name = "productId"
    type = "S"
  }

  attribute {
    name = "date"
    type = "S"
  }

  tags = {
    Name = "product-app-products"
  }
}
```

### Lambda Function (Python)

***lambda/index.py - Lambda Handler***

```python
import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    """
    Process product data and save to DynamoDB.
    """
    table_name = os.environ.get('DYNAMODB_TABLE')
    if not table_name:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'DYNAMODB_TABLE environment variable not set'})
        }
    
    table = dynamodb.Table(table_name)
    
    try:
        # Parse input
        body = json.loads(event.get('body', '{}'))
        
        # Prepare item
        item = {
            'productId': body['productId'],
            'date': body['date'],
            'productName': body['productName'],
            'price': str(body['price']),
            'salesperson': body['salesperson'],
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Save to DynamoDB
        table.put_item(Item=item)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Product saved successfully',
                'productId': item['productId']
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

### Spring Boot Application (Java)

***ProductController.java - Web Controller***

```java
@Controller
public class ProductController {
    
    @Autowired
    private AWSLambda lambdaClient;
    
    @GetMapping("/")
    public String showForm(Model model) {
        model.addAttribute("product", new Product());
        return "product-form";
    }
    
    @PostMapping("/submit")
    public String submitProduct(@ModelAttribute Product product, Model model) {
        try {
            // Invoke Lambda function
            InvokeRequest invokeRequest = new InvokeRequest()
                .withFunctionName(lambdaFunctionName)
                .withPayload(convertProductToJson(product));
            
            InvokeResult result = lambdaClient.invoke(invokeRequest);
            
            // Check response
            if (result.getStatusCode() == 200) {
                model.addAttribute("message", "Product submitted successfully!");
            } else {
                model.addAttribute("error", "Failed to submit product");
            }
        } catch (Exception e) {
            model.addAttribute("error", "Error: " + e.getMessage());
        }
        
        return "product-form";
    }
}
```

## Deployment

### Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform >= 1.0
- AWS account with permissions to create VPC, EC2, Lambda, DynamoDB, and IAM resources

### Quick Start

```bash
# Initialize Terraform
terraform init

# Review the plan
terraform plan

# Deploy infrastructure
terraform apply

# Get the application URL
terraform output application_url
```

### Post-Deployment

After deployment completes (approximately 5-10 minutes for EC2 user data to finish):

1. Visit the application URL from the terraform output
2. You should see the Product Entry Form
3. Fill in the form and submit to test the integration

## Project Structure

```
terraform-aws-product-app/
├── provider.tf              # Terraform and AWS provider configuration
├── variables.tf             # Input variables
├── vpc.tf                  # VPC, subnets, IGW, NAT, route tables
├── security_groups.tf      # Security groups for EC2 and Lambda
├── dynamodb.tf             # DynamoDB table
├── iam.tf                  # IAM roles and policies
├── lambda.tf               # Lambda function configuration
├── ec2.tf                  # EC2 instance configuration
├── user_data.sh            # EC2 initialization script
├── outputs.tf              # Output values
├── lambda/
│   ├── index.py            # Lambda function code
│   └── test_index.py       # Lambda unit tests
├── spring-boot/            # Spring Boot application source
│   ├── pom.xml
│   └── src/
│       ├── main/java/com/example/product/
│       │   ├── ProductApplication.java
│       │   ├── Product.java
│       │   └── ProductController.java
│       └── test/java/      # Spring Boot tests
├── DEVELOPER_GUIDE.md      # Comprehensive development guide
├── TEST_README.md          # Testing documentation
└── QUICK_REFERENCE.md      # Quick command reference
```

## Testing

### Lambda Tests

```bash
cd lambda
python -m unittest test_index.py

# With coverage
pytest test_index.py --cov=index --cov-report=html
```

### Spring Boot Tests

```bash
cd spring-boot
mvn test

# With coverage
mvn test jacoco:report
```

## Monitoring & Debugging

### View Lambda Logs

```bash
aws logs tail /aws/lambda/product-app-product-processor --follow
```

### SSH to EC2 Instance

```bash
ssh -i key.pem ubuntu@$(terraform output -raw ec2_public_ip)
```

### Check Services on EC2

```bash
# Product app status
sudo systemctl status product-app

# Nginx status
sudo systemctl status nginx

# View application logs
sudo journalctl -u product-app -f

# View EC2 initialization logs
sudo tail -f /var/log/cloud-init-output.log
```

### Check DynamoDB Data

```bash
aws dynamodb scan --table-name product-app-products
```

## Customization

Edit `variables.tf` to customize:

| Variable | Description | Default |
|----------|-------------|---------|
| `aws_region` | AWS region | us-east-1 |
| `vpc_cidr` | VPC CIDR block | 10.0.0.0/16 |
| `public_subnet_cidr` | Public subnet CIDR | 10.0.1.0/24 |
| `private_subnet_cidr` | Private subnet CIDR | 10.0.2.0/24 |
| `instance_type` | EC2 instance type | t2.micro |
| `allowed_ssh_cidr` | CIDR blocks allowed SSH | 0.0.0.0/0 |

## Architecture Highlights

### Infrastructure as Code Benefits

- **Reproducibility**: Infrastructure can be recreated identically
- **Version Control**: Track changes to infrastructure over time
- **Documentation**: Code serves as living documentation
- **Automation**: Eliminates manual configuration errors

### Security Features

- **VPC Isolation**: Resources deployed in isolated VPC
- **Private Subnets**: Lambda functions run in private subnet
- **Security Groups**: Granular network access control
- **IAM Roles**: Least privilege access for services
- **NAT Gateway**: Secure outbound internet access for private resources

### Scalability Patterns

- **Serverless Lambda**: Automatically scales with demand
- **DynamoDB**: Serverless NoSQL with pay-per-request billing
- **Elastic IP**: Persistent public IP for EC2 instance
- **Auto-scaling Ready**: Architecture supports auto-scaling groups

## Cost Estimation

### Free Tier Eligible Resources

- EC2 t2.micro instance
- DynamoDB (25 GB storage, 25 WCU/RCU)
- Lambda (1M requests/month)

### Paid Resources

- NAT Gateway (~$0.045/hour + data transfer)
- Elastic IP (when not associated)
- Data transfer
- Additional usage beyond free tier

**Estimated Monthly Cost**: $30-50 USD (primarily NAT Gateway)

## Cleanup

To destroy all resources:

```bash
terraform destroy
```

## Learning Outcomes

This project demonstrates:

- **Terraform**: Infrastructure as Code with multiple AWS services
- **VPC Networking**: Public/private subnet architecture with NAT
- **Serverless Architecture**: Lambda integration with traditional compute
- **Spring Boot**: Java web application with AWS SDK integration
- **DynamoDB**: NoSQL database design with composite keys
- **IAM**: Role-based access control and service permissions
- **DevOps**: Automated deployment and testing workflows

## Repository

[View on GitHub](https://github.com/Bytes0211/terraform-aws-product-app)

---

[← Back to Cloud Computing](cloud-compute.md)
