# CrowdStrike Custom IOM Rules Toolkit

Manage CrowdStrike custom Indicator of Misconfiguration (IOM) rules as code using YAML files and Rego policy language. Export, edit, validate, and deploy rules at scale with version control.

## 🚀 Quick Start

```bash
# Setup
git clone <your-repo-url>
cd crowdstrike-custom-iom-rules
pip install -r requirements.txt
cp .env.sample .env
# Edit .env with your CrowdStrike API credentials

# Test with sample rule
python rule-manager.py validate --config rules/simple-test-rule.yaml
python rule-manager.py create --config rules/simple-test-rule.yaml
```

## 🔄 Rules as Code Workflow

### 1. Export Custom Rules
```bash
# Download all your custom rules (excludes CrowdStrike-managed rules)
python rule-manager.py export-all \
  --filter 'rule_origin:!"Default"' \
  --output-dir my-rules \
  --limit 5000
```

### 2. Validate Rules
```bash
# Validate all rules in directory
python rule-manager.py validate-all --rules-dir my-rules --continue-on-error

# Validate single rule
python rule-manager.py validate --config my-rules/my-rule.yaml
```

### 3. Deploy Rules
```bash
# Deploy all rules (creates new, updates existing)
python rule-manager.py deploy-all \
  --rules-dir my-rules \
  --continue-on-error
```

## 📋 What You Can Do

| Operation | Command | Description |
|-----------|---------|-------------|
| **Export** | `export-all --filter 'rule_origin:!"Default"'` | Download custom rules as YAML |
| **Validate** | `validate-all --rules-dir my-rules` | Check all YAML files for errors |
| **Deploy** | `deploy-all --rules-dir my-rules` | Upload/update all rules |
| **Test** | `test --config my-rule.yaml` | Test rule against real resources |
| **Schema** | `schema --config my-rule.yaml` | Get input schema for resource type |
| **Resources** | `get-resource-ids --provider aws --resource-type "EC2::Instance"` | Get real resource IDs for testing |
| **Filter** | `export-all --filter 'rule_provider:"AWS"'` | Export by platform/severity |

## 🔧 Sample Commands

### Bulk Operations
```bash
# Export only AWS custom rules
python rule-manager.py export-all \
  --filter 'rule_origin:!"Default"+rule_provider:"AWS"' \
  --output-dir aws-rules

# Export high-severity rules only
python rule-manager.py export-all \
  --filter 'rule_origin:!"Default"+rule_severity:1' \
  --output-dir critical-rules

# Validate and deploy with error handling
python rule-manager.py validate-all --rules-dir my-rules --continue-on-error
python rule-manager.py deploy-all --rules-dir my-rules --continue-on-error
```

### Individual Operations
```bash
# Single rule workflow
python rule-manager.py validate --config my-rules/ec2-security.yaml
python rule-manager.py test --config my-rules/ec2-security.yaml
python rule-manager.py create --config my-rules/ec2-security.yaml

# Get test resources
python rule-manager.py get-resource-ids --provider aws --resource-type "EC2::Instance"

# Get input schema for resource type
python rule-manager.py schema --config my-rules/ec2-security.yaml
```

### Management Operations
```bash
# List custom rules only
python rule-manager.py list --filter 'rule_origin:!"Default"' --limit 50

# Update rule properties
python rule-manager.py update --rule-id UUID --severity 2 --description "Updated rule"

# Delete rules
python rule-manager.py delete --rule-ids UUID1 UUID2 --confirm
```

## 📝 Rule Format

**Required Fields Only** (sent to CrowdStrike API):
```yaml
rule:
  # Required basic information
  name: "EC2-Security-Check"
  description: "Ensures EC2 instances meet security requirements"
  resource_type: "AWS::EC2::Instance"
  platform: "AWS"
  provider: "AWS"
  
  # Required classification (defaults shown)
  domain: "CSPM"      # Always CSPM for custom rules
  subdomain: "IOM"    # Always IOM for custom rules
  severity: 1         # 0=critical, 1=high, 2=medium, 3=informational
  
  # Required Rego logic
  logic: |
    package crowdstrike
    default result = "fail"
    
    result = "pass" if {
        input.resource.state == "running"
        input.resource.tags.Environment
    }
    
    violation contains {"msg": msg} if {
        not input.resource.state == "running"
        msg := "EC2 instance must be running"
    }
  
  # Optional but recommended
  alert_info: "Brief description of what this rule checks"
  remediation: "Steps to fix violations"

# Optional sections (not sent to API, used by rule-manager.py)
testing:
  sample_resource_ids:
    - "i-1234567890abcdef0"

metadata:
  version: "1.0"
  author: "security-team"
```

## 🔒 Setup

### API Credentials
Required scopes: `cloud-security-policies:read`, `cloud-security-policies:write`, `cloud-security-assets:read`

```bash
# .env file
FALCON_CLIENT_ID=your-client-id
FALCON_CLIENT_SECRET=your-client-secret
FALCON_BASE_URL=https://api.crowdstrike.com
```

### Supported Platforms
- **AWS**: EC2, S3, RDS, IAM, Lambda
- **Azure**: VMs, Storage, SQL
- **GCP**: Compute, Storage, SQL
- **OCI**: Compute, Storage

## 🔧 Schema and Resource Discovery

### Get Input Schema for Resource Types

Get the exact field structure that CrowdStrike provides for any resource type:

```bash
# Get schema for resource type specified in YAML config
python rule-manager.py schema --config my-rules/ec2-security.yaml
```

**Output files:**
- `schema-ec2-instance.json` - Individual resource schema with exact field structure

### Using Schema Files for Rule Development

The generated schema files contain the **exact field structure** that CrowdStrike provides:

**Available in Rego rules:**
```rego
# Access any field from the schema
resource.configuration.properties.enableNonSslPort
resource.configuration.properties.minimumTlsVersion
resource.configuration.properties.sku.name
resource.configuration.tags.Environment
```

**Sample Claude Prompt for Rule Development:**
```
I need help writing a CrowdStrike custom IOM rule using Rego for [RESOURCE_TYPE].

Resource Schema: [paste schema from schema-*.json]

Security Requirements: [your requirements]

Please provide complete YAML configuration with Rego logic.
```

## 🔧 Troubleshooting

**Export includes CrowdStrike rules**: Use `--filter 'rule_origin:!"Default"'`
**Validation fails**: Check Rego logic starts with `package crowdstrike`
**No test resources**: Use `get-resource-ids` to find valid resource IDs
**Authentication fails**: Verify API credentials and scopes in `.env`
**Schema retrieval fails**: Ensure the resource type is supported by CrowdStrike
**Rule creation fails**: Verify all required fields are present in YAML configuration
**Bulk operations fail**: Use `--continue-on-error` flag to process remaining rules

## 📚 Resources

- **Examples**: [`rules/`](rules/) directory
- **CrowdStrike API**: [Documentation](https://falcon.crowdstrike.com/documentation)
- **Rego Language**: [OPA Docs](https://www.openpolicyagent.org/docs/latest/policy-language/)

## 📁 Project Structure

```
crowdstrike-custom-iom-rules/
├── rule-manager.py              # Main rule CRUD toolkit
├── get_schemas.py               # Schema generation and resource type testing
├── requirements.txt             # Python dependencies
├── .env.sample                  # API credentials template
├── rules/                       # Rule templates and examples
├── exported-custom-rules/       # Exported rules from CrowdStrike
├── resource-support/           # Resource type support documentation
│   ├── all-resource-types-azure.txt
│   ├── all-resource-types-gcp.txt
│   ├── resource-type-support-aws.md
│   ├── resource-type-support-azure.md
│   ├── resource-type-support-gcp.md
│   └── schema-*.json           # Individual resource schemas
└── schemas/                    # Generated schemas from discovery
```

---
**Version:** 2.1 | Focused rule management toolkit for CRUD operations on CrowdStrike custom IOM rules. Schema functionality moved to separate get_schemas.py module.