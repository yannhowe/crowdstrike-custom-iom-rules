# CrowdStrike Custom IOM Rules Toolkit

A comprehensive Python toolkit for creating, managing, and deploying CrowdStrike custom Indicator of Misconfiguration (IOM) rules using YAML configuration files and Rego policy language.

## 🎯 What This Project Does

This toolkit allows you to:
- **Create custom security rules** for cloud resources (AWS, Azure, GCP, OCI)
- **Manage rules at scale** with bulk operations and automatic pagination
- **Use YAML configuration** instead of complex API calls
- **Test rules** before deployment with real cloud resources
- **Export existing rules** from your CrowdStrike environment
- **Deploy rules** across multiple environments (staging/production)

## 🚀 Quick Start

### 1. Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd crowdstrike-custom-iom-rules

# Install dependencies
pip install -r requirements.txt

# Configure your API credentials
cp .env.sample .env
# Edit .env with your CrowdStrike API credentials
```

### 2. Your First Rule

```bash
# Validate the sample rule
python rule-manager.py validate --config rules/simple-test-rule.yaml

# Create the rule in CrowdStrike
python rule-manager.py create --config rules/simple-test-rule.yaml
```

### 3. Verify It Worked

```bash
# List your custom rules
python rule-manager.py list --limit 10
```

## 📋 What's Included

### Core Tool
- **`rule-manager.py`** - Complete rule management CLI (1685+ lines of Python)

### Sample Rules
- **`rules/simple-test-rule.yaml`** - Basic EC2 state validation rule
- **`rules/example-ec2-security-rule.yaml`** - Advanced security compliance rule

### Configuration
- **`.env.sample`** - Template for API credentials
- **`requirements.txt`** - Python dependencies
- **`.gitignore`** - Protects sensitive files

## 🔧 Key Features

### Rule Management
```bash
# Create a single rule
python rule-manager.py create --config rules/my-rule.yaml

# Create all rules in a directory
python rule-manager.py create-all --rules-dir rules

# Update existing rules
python rule-manager.py update --rule-id UUID --severity 2

# Delete rules
python rule-manager.py delete --rule-ids UUID1 UUID2
```

### Testing & Validation
```bash
# Validate YAML syntax and Rego logic
python rule-manager.py validate --config rules/my-rule.yaml

# Test against real cloud resources
python rule-manager.py test --config rules/my-rule.yaml

# Get resource IDs for testing
python rule-manager.py get-resource-ids --provider aws --resource-type "EC2::Instance"
```

### Bulk Operations
```bash
# Export all existing rules to YAML files
python rule-manager.py export-all --output-dir exported-rules --limit 1000

# Deploy all rules (create new, update existing)
python rule-manager.py deploy-all --rules-dir rules --continue-on-error
```

## 📝 Rule Format

Rules are defined in simple YAML files:

```yaml
rule:
  name: "My-Security-Rule"
  description: "Ensures EC2 instances meet security requirements"
  resource_type: "AWS::EC2::Instance"
  platform: "AWS"
  provider: "AWS"
  severity: 1  # 0=critical, 1=high, 2=medium, 3=informational
  
  logic: |
    package crowdstrike
    
    default result = "fail"
    
    # Rule passes if instance is running
    result = "pass" if {
        input.resource.state == "running"
    }
    
    # Violation message for failed checks
    violation contains {"msg": msg} if {
        not input.resource.state == "running"
        msg := "EC2 instance must be in running state"
    }
```

## 🔒 Security & Credentials

### API Credentials Required
You need CrowdStrike API credentials with these scopes:
- `Cloud-Policies:READ`
- `Cloud-Policies:WRITE`
- `Cloud-Security-Assets:READ`

### Secure Configuration
```bash
# Copy the sample file
cp .env.sample .env

# Edit with your actual credentials
FALCON_CLIENT_ID=your-actual-client-id
FALCON_CLIENT_SECRET=your-actual-client-secret
FALCON_BASE_URL=https://api.crowdstrike.com
```

**⚠️ Important:** Never commit your `.env` file. It's already in `.gitignore`.

## 🌐 Supported Platforms

| Platform | Resource Types | Example |
|----------|----------------|---------|
| **AWS** | EC2, S3, RDS, IAM, Lambda | `AWS::EC2::Instance` |
| **Azure** | VMs, Storage, SQL | `Azure::Compute::VirtualMachine` |
| **GCP** | Compute, Storage, SQL | `GCP::Compute::Instance` |
| **OCI** | Compute, Storage | `OCI::Compute::Instance` |

## 📊 Enterprise Features

### Automatic Pagination
Handles large environments with thousands of rules:
```bash
# Export up to 5000 rules automatically
python rule-manager.py export-all --limit 5000
```

### Bulk Deployment
Deploy multiple rules with error handling:
```bash
# Continue processing even if some rules fail
python rule-manager.py deploy-all --continue-on-error
```

### Environment Management
```bash
# Deploy to staging first
python rule-manager.py create --config rules/my-rule.yaml --environment staging

# Then promote to production
python rule-manager.py create --config rules/my-rule.yaml --environment production
```

## 🛠️ Command Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `validate` | Check YAML and Rego syntax | `python rule-manager.py validate --config rules/my-rule.yaml` |
| `create` | Create a new rule | `python rule-manager.py create --config rules/my-rule.yaml` |
| `list` | Show existing rules | `python rule-manager.py list --limit 50` |
| `update` | Modify existing rule | `python rule-manager.py update --rule-id UUID --severity 2` |
| `delete` | Remove rules | `python rule-manager.py delete --rule-ids UUID` |
| `test` | Test rule logic | `python rule-manager.py test --config rules/my-rule.yaml` |
| `export-all` | Export to YAML files | `python rule-manager.py export-all --output-dir backup` |
| `deploy-all` | Bulk create/update | `python rule-manager.py deploy-all --rules-dir rules` |

## 🐛 Troubleshooting

### Common Issues

**"Authentication failed"**
- Check your `.env` file has correct credentials
- Verify API scopes in CrowdStrike console

**"Rule validation failed"**
- Run `validate` command first to check syntax
- Ensure Rego logic starts with `package crowdstrike`

**"No resources found for testing"**
- Use `get-resource-ids` to find valid resource IDs
- Add resource IDs to your YAML file's `testing` section

### Getting Help
```bash
# Show all available commands
python rule-manager.py --help

# Get help for specific command
python rule-manager.py create --help
```

## 📚 Learn More

- **Rule Examples**: Check the [`rules/`](rules/) directory for sample configurations
- **CrowdStrike Docs**: [Official API Documentation](https://falcon.crowdstrike.com/documentation)
- **Rego Language**: [Open Policy Agent Documentation](https://www.openpolicyagent.org/docs/latest/policy-language/)

## 🤝 Contributing

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Test your changes thoroughly
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License

This project is provided as-is for educational and operational purposes. Ensure compliance with your organization's security policies and CrowdStrike's terms of service.

---

**Need help?** Open an issue or check the troubleshooting section above.

**Version:** 1.0 | **Last Updated:** 2025-11-21