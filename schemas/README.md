# CrowdStrike Schema Manager

A standalone tool for managing CrowdStrike resource schemas. This tool fetches schemas from CrowdStrike APIs and provides comprehensive testing and documentation capabilities for AWS, Azure, and GCP resource types.

## Overview

The Schema Manager is a complete solution for:
- Testing resource type support across cloud providers
- Generating and validating schemas
- Creating comprehensive documentation
- Managing schema files and reports

## Quick Start

### Prerequisites

1. **Environment Setup**: Create a `.env` file in the project root with your CrowdStrike API credentials:
   ```bash
   FALCON_CLIENT_ID=your_client_id
   FALCON_CLIENT_SECRET=your_client_secret
   FALCON_CLOUD=us-1  # or your appropriate cloud region
   ```

2. **Dependencies**: Install required Python packages:
   ```bash
   pip install falconpy python-dotenv
   ```

### Basic Usage

Run the schema manager from the schemas directory:

```bash
cd schemas
python get_schemas.py --help
```

## Commands

### 1. Test Resource Type Support

Test which resource types are supported by CrowdStrike for each cloud provider:

```bash
# Test AWS resource types (413 types)
python get_schemas.py test-support --provider aws

# Test Azure resource types (1,374 types, Microsoft only)
python get_schemas.py test-support --provider azure

# Test GCP resource types (562 types)
python get_schemas.py test-support --provider gcp

# Adjust concurrency (default: 10 concurrent requests)
python get_schemas.py test-support --provider aws --batch-size 5
```

**Results:**
- **AWS**: 130/413 supported (31.5%)
- **Azure**: 51/1,374 supported (3.7%)
- **GCP**: 64/562 supported (11.4%)

### 2. Get Individual Schema

Retrieve schema for a specific resource type:

```bash
# Get AWS EC2 Instance schema
python get_schemas.py get-schema --provider aws --resource-type "AWS::EC2::Instance"

# Get Azure Virtual Machine schema
python get_schemas.py get-schema --provider azure --resource-type "Microsoft.Compute/virtualMachines"

# Get GCP Compute Instance schema
python get_schemas.py get-schema --provider gcp --resource-type "compute.googleapis.com/Instance"
```

### 3. Validate Schemas

Validate existing schema files for correctness:

```bash
# Validate all schemas in current directory
python get_schemas.py validate-schemas

# Validate schemas in specific directory
python get_schemas.py validate-schemas --schemas-dir /path/to/schemas
```

### 4. Generate Documentation

Create documentation from schema files:

```bash
# Generate markdown documentation
python get_schemas.py generate-docs --format markdown

# Generate JSON documentation
python get_schemas.py generate-docs --format json

# Specify output directory
python get_schemas.py generate-docs --output-dir docs --format markdown
```

### 5. List Available Schemas

List all available schema files:

```bash
# List all schemas
python get_schemas.py list-schemas

# Filter by provider
python get_schemas.py list-schemas --provider aws
python get_schemas.py list-schemas --provider azure
python get_schemas.py list-schemas --provider gcp
```

### 6. Compare Schema Versions

Compare schemas between different versions or directories:

```bash
python get_schemas.py compare-schemas --old-dir old_schemas --new-dir new_schemas
```

### 7. Cache Management

Manage schema cache:

```bash
# Show cache status
python get_schemas.py cache status

# Clear cache
python get_schemas.py cache clear

# Update cache (placeholder for future implementation)
python get_schemas.py cache update
```

## File Structure

```
schemas/
├── get_schemas.py                     # Main schema management tool
├── README.md                          # This documentation
├── json/                              # All schema JSON files
│   ├── schema-aws-*.json             # AWS schemas (130 files)
│   ├── schema-azure-*.json           # Azure schemas (51 files)
│   └── schema-gcp-*.json             # GCP schemas (64 files)
├── docs/                             # Generated documentation
├── all-resource-types-*.txt          # Authoritative resource type lists
├── resource-type-support-*.json      # Test reports
├── resource-type-support-*.md        # Markdown documentation
└── validation-report.json           # Schema validation results
```

## Resource Type Lists

The tool uses authoritative resource type lists:

- **`all-resource-types-aws.txt`**: 413 AWS Config resource types
- **`all-resource-types-azure.txt`**: 1,374 Azure resource types (Microsoft only)
- **`all-resource-types-gcp.txt`**: 562 GCP resource types

## Advanced Usage

### Concurrent Testing

Adjust the batch size for concurrent API requests based on your API limits:

```bash
# Conservative (slower but safer)
python get_schemas.py test-support --provider aws --batch-size 5

# Aggressive (faster but may hit rate limits)
python get_schemas.py test-support --provider aws --batch-size 20
```

### Error Handling

The tool provides enhanced error reporting:
- **❌ NOT SUPPORTED**: Standard "resource not found" errors
- **🚨 UNEXPECTED ERROR**: Non-standard HTTP errors (highlighted for investigation)
- **🚨 EXCEPTION**: Unexpected exceptions during testing

### Output Directories

All commands support custom output directories:

```bash
# Save results to custom directory
python get_schemas.py test-support --provider aws --output-dir /custom/path

# Generate docs to specific location
python get_schemas.py generate-docs --output-dir /docs/path
```

## Integration with Rule Manager

The schemas generated by this tool can be used with the main rule manager:

```bash
# From project root, use schemas for rule development
cd ..
python rule-manager.py schema --config your-rule.yaml
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Ensure your `.env` file is in the project root with correct credentials
2. **Rate Limiting**: Reduce `--batch-size` if you encounter rate limiting
3. **File Not Found**: Ensure resource type files exist in the schemas directory
4. **Permission Errors**: Check file permissions for output directories

### Debug Mode

For detailed error information, the tool provides comprehensive error reporting and stack traces.

## Support

For issues or questions:
1. Check the error messages - they provide specific guidance
2. Verify your CrowdStrike API credentials and permissions
3. Ensure all required files are present in the schemas directory

---

*Generated by CrowdStrike Custom IOM Rules Toolkit*