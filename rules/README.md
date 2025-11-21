# CrowdStrike Custom IOM Rules

This folder contains YAML configuration files for CrowdStrike custom Indicator of Misconfiguration (IOM) rules.

## Available Rules

### simple-test-rule.yaml
- **Purpose**: Basic test rule for API validation
- **Resource Type**: AWS::EC2::Instance
- **Description**: Simple rule that checks if EC2 instances are in running state
- **Complexity**: Basic (good for testing and learning)
- **Usage**: 
  ```bash
  pipenv run python ../rule-manager.py create --config simple-test-rule.yaml
  ```

### example-ec2-security-rule.yaml
- **Purpose**: Comprehensive EC2 security validation
- **Resource Type**: AWS::EC2::Instance
- **Description**: Advanced rule with multiple security checks including:
  - Required tags validation
  - Approved instance types
  - Security group configuration
  - Monitoring requirements
- **Complexity**: Advanced (production-ready example)
- **Usage**: 
  ```bash
  pipenv run python ../rule-manager.py create --config example-ec2-security-rule.yaml
  ```

## Rule Structure

Each YAML file contains:

```yaml
metadata:
  version: "1.0"
  author: "Security Team"
  created: "2025-11-21"

rule:
  name: "Rule-Name"
  description: "What this rule validates"
  resource_type: "AWS::EC2::Instance"
  platform: "AWS"
  provider: "AWS"
  severity: 1  # 0=critical, 1=high, 2=medium, 3=informational
  
  logic: |
    package crowdstrike
    
    default result = "fail"
    
    result = "pass" if {
        # Your validation conditions
    }
    
    violation contains {"msg": msg} if {
        # Your violation conditions
        msg := "Description of violation"
    }

testing:
  sample_resource_ids:
    - "resource-id-1"
    - "resource-id-2"
```

## Creating New Rules

1. Copy an existing rule file as a template
2. Modify the rule name, description, and logic
3. Update the resource type and platform as needed
4. Test with validation command:
   ```bash
   pipenv run python ../rule-manager.py validate --config your-new-rule.yaml
   ```
5. Create the rule:
   ```bash
   pipenv run python ../rule-manager.py create --config your-new-rule.yaml
   ```

## Supported Platforms

- **AWS**: Amazon Web Services
- **Azure**: Microsoft Azure
- **GCP**: Google Cloud Platform
- **OCI**: Oracle Cloud Infrastructure

## Common Resource Types

### AWS
- `AWS::EC2::Instance`
- `AWS::S3::Bucket`
- `AWS::RDS::DBInstance`
- `AWS::IAM::Role`
- `AWS::Lambda::Function`

### Azure
- `Azure::Compute::VirtualMachine`
- `Azure::Storage::StorageAccount`
- `Azure::SQL::Server`

### GCP
- `GCP::Compute::Instance`
- `GCP::Storage::Bucket`
- `GCP::SQL::DatabaseInstance`

## Best Practices

1. **Start Simple**: Begin with basic rules like `simple-test-rule.yaml`
2. **Use Descriptive Names**: Make rule names clear and specific
3. **Include Violation Messages**: Provide helpful error descriptions
4. **Test Thoroughly**: Always validate before creating rules
5. **Document Logic**: Add comments in complex Rego logic
6. **Version Control**: Track changes to rule configurations