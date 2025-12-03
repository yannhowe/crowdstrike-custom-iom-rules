#!/usr/bin/env python3
"""
CrowdStrike YAML-Based Rule Manager

A complete, self-contained tool for managing CrowdStrike custom IOM rules
using YAML configuration files. Includes all API functions and YAML parsing.
"""

import argparse
import json
import sys
import yaml
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from falconpy import APIHarnessV2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def print_json(data):
    """Pretty print JSON data with proper formatting."""
    print(json.dumps(data, indent=2, sort_keys=False))


def print_response(response, success_message=None):
    """
    Print API response in a formatted way.
    
    Args:
        response: API response dictionary
        success_message: Optional success message to display
    """
    if response["status_code"] in [200, 201]:
        if success_message:
            print(f"\n✓ {success_message}\n")
        print_json(response["body"])
        return True
    else:
        print(f"\n✗ Error: HTTP {response['status_code']}\n")
        print_json(response["body"])
        return False


def get_sample_resource_ids(falcon, filter_query=None, sort="resource_id|asc", limit=500, offset=0):
    """
    Get sample resource IDs for writing custom rules.
    
    Args:
        falcon: APIHarnessV2 instance
        filter_query: FQL filter string
        sort: Sort field and direction
        limit: Maximum number of IDs to return (1-1000)
        offset: Number of results to skip
    """
    params = {
        "sort": sort,
        "limit": limit,
        "offset": offset
    }
    
    if filter_query:
        params["filter"] = filter_query
    
    response = falcon.command(
        override="GET,/cloud-security-assets/queries/resources/v1",
        parameters=params
    )
    
    if print_response(response):
        return response["body"].get("resources", [])
    return None


def get_sample_resource(falcon, resource_ids):
    """
    Get detailed sample resource information.
    
    Args:
        falcon: APIHarnessV2 instance
        resource_ids: List of resource IDs (max 100)
    """
    if isinstance(resource_ids, str):
        resource_ids = [resource_ids]
    
    if len(resource_ids) > 100:
        print("Warning: Maximum 100 IDs allowed. Using first 100.")
        resource_ids = resource_ids[:100]
    
    params = {
        "ids": resource_ids
    }
    
    response = falcon.command(
        override="GET,/cloud-security-assets/entities/resources/v1",
        parameters=params
    )
    
    if print_response(response):
        return response["body"].get("resources", [])
    return None


def get_input_schema(falcon, cloud_provider, resource_type, domain="CSPM", subdomain="IOM"):
    """
    Get input schema for a specific resource type.
    
    Args:
        falcon: APIHarnessV2 instance
        cloud_provider: aws, azure, gcp, or oci
        resource_type: Cloud provider resource type
        domain: Must be CSPM
        subdomain: Must be IOM
    """
    params = {
        "domain": domain,
        "subdomain": subdomain,
        "cloud_provider": cloud_provider,
        "resource_type": resource_type  # Don't URL encode - API expects original format
    }
    
    response = falcon.command(
        override="GET,/cloud-policies/combined/rules/input-schema/v1",
        parameters=params,
        headers={"Content-Type": "application/json"}  # Explicit content type
    )
    
    if print_response(response):
        return response["body"].get("resources", [])
    return None


def test_rule_logic(falcon, cloud_provider, resource_type, logic, resource_ids):
    """
    Test and evaluate rule logic against cloud assets.
    
    Args:
        falcon: APIHarnessV2 instance
        cloud_provider: aws, azure, gcp, or oci
        resource_type: Cloud provider resource type
        logic: Rego rule logic as string
        resource_ids: List of resource IDs to test (max 100)
    """
    if isinstance(resource_ids, str):
        resource_ids = [resource_ids]
    
    if len(resource_ids) > 100:
        print("Warning: Maximum 100 IDs allowed. Using first 100.")
        resource_ids = resource_ids[:100]
    
    params = {
        "cloud_provider": cloud_provider,
        "resource_type": resource_type
    }
    
    body = {
        "logic": logic,
        "ids": resource_ids
    }
    
    response = falcon.command(
        override="POST,/cloud-policies/entities/evaluation/v1",
        parameters=params,
        body=body
    )
    
    if print_response(response, "Rule evaluation completed"):
        return response["body"].get("resources", [])
    return None


def create_custom_rule(falcon, name, description, resource_type, logic, platform, 
                       provider, domain="CSPM", subdomain="IOM", severity=0,
                       alert_info=None, remediation=None, attack_types=None, controls=None):
    """
    Create a custom cloud configuration rule.
    
    Args:
        falcon: APIHarnessV2 instance
        name: Rule name
        description: Rule description
        resource_type: Cloud provider resource type
        logic: Rego rule logic as string
        platform: AWS, Azure, GCP, or OCI (case sensitive)
        provider: AWS, Azure, GCP, or OCI (case sensitive, must match platform)
        domain: Domain name (default: CSPM)
        subdomain: Subdomain name (default: IOM)
        severity: 0=critical, 1=high, 2=medium, 3=informational
        alert_info: Alert logic description
        remediation: Remediation steps
        attack_types: List of attack types
        controls: List of control mappings
    """
    body = {
        "name": name,
        "description": description,
        "domain": domain,
        "subdomain": subdomain,
        "resource_type": resource_type,
        "logic": logic,
        "platform": platform,
        "provider": provider,
        "severity": severity
    }
    
    if alert_info:
        body["alert_info"] = alert_info
    if remediation:
        body["remediation"] = remediation
    if attack_types:
        body["attack_types"] = attack_types
    
    # Always include controls field (empty array if not specified)
    body["controls"] = controls if controls else []
    
    response = falcon.command(
        override="POST,/cloud-policies/entities/rules/v1",
        body=body
    )
    
    if print_response(response, f"Custom rule '{name}' created successfully"):
        return response["body"].get("resources", [])
    return None


def get_custom_rules(falcon, filter_query=None, limit=100, offset=0, sort=None):
    """
    Get a list of custom rule IDs.
    
    Args:
        falcon: APIHarnessV2 instance
        filter_query: FQL filter string
        limit: Maximum number of rule IDs to return (max 500)
        offset: Number of results to skip
        sort: Sort field and direction
    """
    params = {
        "limit": limit,
        "offset": offset
    }
    
    if filter_query:
        params["filter"] = filter_query
    if sort:
        params["sort"] = sort
    
    response = falcon.command(
        override="GET,/cloud-policies/queries/rules/v1",
        parameters=params
    )
    
    if print_response(response):
        return response["body"].get("resources", [])
    return None


def get_rule_details(falcon, rule_uuids):
    """
    Get detailed information about specific rules.
    
    Args:
        falcon: APIHarnessV2 instance
        rule_uuids: List of rule UUIDs
    """
    if isinstance(rule_uuids, str):
        rule_uuids = [rule_uuids]
    
    params = {
        "ids": rule_uuids
    }
    
    response = falcon.command(
        override="GET,/cloud-policies/entities/rules/v1",
        parameters=params
    )
    
    if print_response(response):
        return response["body"].get("resources", [])
    return None


def update_custom_rule(falcon, rule_uuid, name=None, description=None, severity=None,
                       alert_info=None, attack_types=None, rule_logic_list=None):
    """
    Update an existing custom rule.
    
    Args:
        falcon: APIHarnessV2 instance
        rule_uuid: UUID of the rule to update
        name: New rule name
        description: New rule description
        severity: New severity (0-3)
        alert_info: New alert info
        attack_types: New attack types
        rule_logic_list: List containing logic update objects
    """
    body = {
        "uuid": rule_uuid
    }
    
    if name:
        body["name"] = name
    if description:
        body["description"] = description
    if severity is not None:
        body["severity"] = severity
    if alert_info:
        body["alert_info"] = alert_info
    if attack_types:
        body["attack_types"] = attack_types
    if rule_logic_list:
        body["rule_logic_list"] = rule_logic_list
    
    response = falcon.command(
        override="PATCH,/cloud-policies/entities/rules/v1",
        body=body
    )
    
    if print_response(response, f"Custom rule '{rule_uuid}' updated successfully"):
        return response["body"].get("resources", [])
    return None


def delete_custom_rules(falcon, rule_uuids):
    """
    Delete one or more custom rules.
    
    Args:
        falcon: APIHarnessV2 instance
        rule_uuids: List of rule UUIDs to delete
    """
    if isinstance(rule_uuids, str):
        rule_uuids = [rule_uuids]
    
    params = {
        "ids": rule_uuids
    }
    
    response = falcon.command(
        override="DELETE,/cloud-policies/entities/rules/v1",
        parameters=params
    )
    
    count = len(rule_uuids)
    if print_response(response, f"{count} custom rule(s) deleted successfully"):
        return response["body"].get("resources", [])
    return None


def save_to_file(data, filename):
    """
    Save data to a JSON file.
    
    Args:
        data: Data to save
        filename: Output filename
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n✓ Data saved to: {filename}")
    except Exception as e:
        print(f"\n✗ Error saving to file: {str(e)}")


def load_yaml_config(config_file):
    """
    Load and parse YAML configuration file.
    
    Args:
        config_file: Path to YAML configuration file
        
    Returns:
        Parsed YAML configuration dictionary
    """
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print(f"✗ Error: Configuration file '{config_file}' not found")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"✗ Error parsing YAML file: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error loading configuration: {str(e)}")
        sys.exit(1)


def validate_yaml_config(config):
    """
    Validate YAML configuration structure.
    
    Args:
        config: Parsed YAML configuration
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(config, dict):
        print("✗ Error: Configuration must be a dictionary")
        return False
    
    if 'rule' not in config:
        print("✗ Error: Configuration must contain 'rule' section")
        return False
    
    rule = config['rule']
    required_fields = ['name', 'description', 'resource_type', 'platform', 'provider', 'logic']
    
    for field in required_fields:
        if field not in rule:
            print(f"✗ Error: Missing required field 'rule.{field}'")
            return False
    
    # Validate platform and provider match
    if rule['platform'] != rule['provider']:
        print("✗ Error: 'platform' and 'provider' must have the same value")
        return False
    
    # Validate severity if present
    if 'severity' in rule and rule['severity'] not in [0, 1, 2, 3]:
        print("✗ Error: 'severity' must be 0 (critical), 1 (high), 2 (medium), or 3 (informational)")
        return False
    
    return True


def validate_rego_syntax(rego_logic):
    """
    Basic validation of Rego syntax.
    
    Args:
        rego_logic: Rego logic string
        
    Returns:
        True if basic validation passes, False otherwise
    """
    if not rego_logic.strip():
        print("✗ Error: Rego logic cannot be empty")
        return False
    
    if not rego_logic.strip().startswith('package crowdstrike'):
        print("✗ Error: Rego logic must start with 'package crowdstrike'")
        return False
    
    if 'default result = "fail"' not in rego_logic:
        print("✗ Warning: Rego logic should include 'default result = \"fail\"'")
    
    if 'result = "pass"' not in rego_logic:
        print("✗ Warning: Rego logic should include 'result = \"pass\"' condition")
    
    return True


def create_rule_from_yaml(config_file, environment="production"):
    """
    Create a custom rule from YAML configuration.
    
    Args:
        config_file: Path to YAML configuration file
        environment: Target environment (staging/production)
    """
    print(f"🚀 Creating rule from YAML configuration: {config_file}")
    print(f"📍 Target environment: {environment}")
    print("=" * 60)
    
    # Load and validate configuration
    config = load_yaml_config(config_file)
    
    if not validate_yaml_config(config):
        sys.exit(1)
    
    rule = config['rule']
    
    # Validate Rego logic
    if not validate_rego_syntax(rule['logic']):
        sys.exit(1)
    
    # Initialize Falcon API
    falcon = APIHarnessV2()
    
    # Prepare rule parameters
    name = rule['name']
    description = rule['description']
    resource_type = rule['resource_type']
    logic = rule['logic']
    platform = rule['platform']
    provider = rule['provider']
    domain = rule.get('domain', 'CSPM')
    subdomain = rule.get('subdomain', 'IOM')
    severity = rule.get('severity', 1)
    alert_info = rule.get('alert_info')
    remediation = rule.get('remediation')
    attack_types = rule.get('attack_types')
    
    # Process controls if present
    controls = None
    if 'controls' in rule:
        controls = rule['controls']
    
    print(f"📋 Rule Details:")
    print(f"   Name: {name}")
    print(f"   Description: {description}")
    print(f"   Resource Type: {resource_type}")
    print(f"   Platform: {platform}")
    print(f"   Severity: {severity}")
    print(f"   Domain: {domain}")
    print(f"   Subdomain: {subdomain}")
    print()
    
    # Create the rule
    result = create_custom_rule(
        falcon, name, description, resource_type, logic,
        platform, provider, domain, subdomain, severity,
        alert_info, remediation, attack_types, controls
    )
    
    if result:
        print(f"✅ Rule '{name}' created successfully!")
        
        # Save result to file
        output_file = f"created-rule-{name.lower().replace(' ', '-').replace('_', '-')}.json"
        save_to_file(result, output_file)
    else:
        print(f"❌ Failed to create rule '{name}'")
        sys.exit(1)


def test_rule_from_yaml(config_file, environment="staging"):
    """
    Test a rule from YAML configuration.
    
    Args:
        config_file: Path to YAML configuration file
        environment: Target environment for testing
    """
    print(f"🧪 Testing rule from YAML configuration: {config_file}")
    print(f"📍 Test environment: {environment}")
    print("=" * 60)
    
    # Load and validate configuration
    config = load_yaml_config(config_file)
    
    if not validate_yaml_config(config):
        sys.exit(1)
    
    rule = config['rule']
    
    # Validate Rego logic
    if not validate_rego_syntax(rule['logic']):
        sys.exit(1)
    
    # Initialize Falcon API
    falcon = APIHarnessV2()
    
    # Get test resource IDs
    resource_ids = []
    if 'testing' in config and 'sample_resource_ids' in config['testing']:
        resource_ids = config['testing']['sample_resource_ids']
        print(f"📋 Using configured test resource IDs: {resource_ids}")
    else:
        # Try to get sample resource IDs automatically
        print(f"🔍 Searching for sample {rule['resource_type']} resources...")
        provider_map = {"AWS": "aws", "Azure": "azure", "GCP": "gcp", "OCI": "oci"}
        provider_lower = provider_map.get(rule['platform'], rule['platform'].lower())
        
        filter_query = f'cloud_provider:"{provider_lower}"+resource_type:"{rule["resource_type"]}"'
        sample_ids = get_sample_resource_ids(falcon, filter_query, limit=5)
        
        if sample_ids:
            resource_ids = sample_ids[:3]  # Use first 3 for testing
            print(f"📋 Found sample resource IDs: {resource_ids}")
        else:
            print("⚠️  No sample resources found. Please provide test resource IDs in the YAML configuration.")
            return
    
    if not resource_ids:
        print("❌ No resource IDs available for testing")
        return
    
    # Test the rule logic
    provider_map = {"AWS": "aws", "Azure": "azure", "GCP": "gcp", "OCI": "oci"}
    provider_lower = provider_map.get(rule['platform'], rule['platform'].lower())
    
    print(f"🔬 Testing rule logic against {len(resource_ids)} resources...")
    result = test_rule_logic(
        falcon, provider_lower, rule['resource_type'], 
        rule['logic'], resource_ids
    )
    
    if result:
        print("✅ Rule testing completed successfully!")
        
        # Save test results
        output_file = f"test-results-{rule['name'].lower().replace(' ', '-').replace('_', '-')}.json"
        save_to_file(result, output_file)
        
        # Display summary
        print("\n📊 Test Results Summary:")
        for i, resource_result in enumerate(result):
            resource_id = resource_ids[i] if i < len(resource_ids) else f"resource-{i}"
            evaluation = resource_result.get('evaluation', {})
            result_status = evaluation.get('result', 'unknown')
            print(f"   {resource_id}: {result_status}")
    else:
        print("❌ Rule testing failed")
        sys.exit(1)


def validate_rule_from_yaml(config_file):
    """
    Validate a rule from YAML configuration without creating it.
    
    Args:
        config_file: Path to YAML configuration file
    """
    print(f"✅ Validating YAML configuration: {config_file}")
    print("=" * 60)
    
    # Load and validate configuration
    config = load_yaml_config(config_file)
    
    print("📋 Configuration Structure Validation:")
    if not validate_yaml_config(config):
        print("❌ Configuration validation failed")
        sys.exit(1)
    else:
        print("✅ Configuration structure is valid")
    
    rule = config['rule']
    
    print("\n🔍 Rego Logic Validation:")
    if not validate_rego_syntax(rule['logic']):
        print("❌ Rego logic validation failed")
        sys.exit(1)
    else:
        print("✅ Rego logic validation passed")
    
    print("\n📊 Rule Summary:")
    print(f"   Name: {rule['name']}")
    print(f"   Description: {rule['description']}")
    print(f"   Resource Type: {rule['resource_type']}")
    print(f"   Platform: {rule['platform']}")
    print(f"   Severity: {rule.get('severity', 1)}")
    print(f"   Logic Length: {len(rule['logic'])} characters")
    
    if 'testing' in config:
        testing = config['testing']
        if 'sample_resource_ids' in testing:
            print(f"   Test Resources: {len(testing['sample_resource_ids'])} configured")
    
    if 'metadata' in config:
        metadata = config['metadata']
        print(f"   Version: {metadata.get('version', 'N/A')}")
        print(f"   Author: {metadata.get('author', 'N/A')}")
    
    print("\n✅ All validations passed! Rule is ready for deployment.")


def validate_all_rules_command(rules_dir="rules", continue_on_error=False):
    """
    Validate all rules from YAML files in the specified directory.
    
    Args:
        rules_dir: Directory containing YAML rule files
        continue_on_error: Continue validating other rules if one fails
    """
    print("✅ Validating All Rules from Directory")
    print("=" * 60)
    
    if not os.path.exists(rules_dir):
        print(f"❌ Rules directory '{rules_dir}' not found")
        sys.exit(1)
    
    # Find all YAML files in the directory
    yaml_files = []
    for file in os.listdir(rules_dir):
        if file.endswith(('.yaml', '.yml')) and not file.startswith('.'):
            yaml_files.append(os.path.join(rules_dir, file))
    
    if not yaml_files:
        print(f"❌ No YAML files found in '{rules_dir}' directory")
        sys.exit(1)
    
    print(f"📋 Found {len(yaml_files)} YAML rule file(s):")
    for i, file in enumerate(yaml_files, 1):
        print(f"   {i}. {file}")
    
    print(f"\n🔄 Continue on error: {'Yes' if continue_on_error else 'No'}")
    print()
    
    # Track results
    valid_rules = []
    invalid_rules = []
    
    # Process each YAML file
    for yaml_file in yaml_files:
        print(f"✅ Validating: {yaml_file}")
        print("-" * 40)
        
        try:
            # Load and validate configuration
            config = load_yaml_config(yaml_file)
            
            # Validate YAML structure
            print("📋 Configuration Structure Validation:")
            if not validate_yaml_config(config):
                if continue_on_error:
                    print(f"⚠️  Configuration validation failed for {yaml_file}")
                    invalid_rules.append({"file": yaml_file, "error": "Configuration validation failed"})
                    print()
                    continue
                else:
                    print(f"❌ Stopping due to configuration validation errors in {yaml_file}")
                    sys.exit(1)
            else:
                print("✅ Configuration structure is valid")
            
            rule = config['rule']
            
            # Validate Rego logic
            print("\n🔍 Rego Logic Validation:")
            if not validate_rego_syntax(rule['logic']):
                if continue_on_error:
                    print(f"⚠️  Rego validation failed for {yaml_file}")
                    invalid_rules.append({"file": yaml_file, "error": "Rego validation failed"})
                    print()
                    continue
                else:
                    print(f"❌ Stopping due to Rego validation errors in {yaml_file}")
                    sys.exit(1)
            else:
                print("✅ Rego logic validation passed")
            
            # Display rule summary
            print("\n📊 Rule Summary:")
            print(f"   Name: {rule['name']}")
            print(f"   Description: {rule['description']}")
            print(f"   Resource Type: {rule['resource_type']}")
            print(f"   Platform: {rule['platform']}")
            print(f"   Severity: {rule.get('severity', 1)}")
            print(f"   Logic Length: {len(rule['logic'])} characters")
            
            if 'testing' in config:
                testing = config['testing']
                if 'sample_resource_ids' in testing:
                    print(f"   Test Resources: {len(testing['sample_resource_ids'])} configured")
            
            if 'metadata' in config:
                metadata = config['metadata']
                print(f"   Version: {metadata.get('version', 'N/A')}")
                print(f"   Author: {metadata.get('author', 'N/A')}")
            
            print("✅ All validations passed!")
            valid_rules.append({"file": yaml_file, "name": rule['name']})
        
        except Exception as e:
            error_msg = str(e)
            if continue_on_error:
                print(f"⚠️  Error validating {yaml_file}: {error_msg}")
                invalid_rules.append({"file": yaml_file, "error": error_msg})
            else:
                print(f"❌ Error validating {yaml_file}: {error_msg}")
                sys.exit(1)
        
        print()  # Add spacing between files
    
    # Summary
    print("=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)
    
    print(f"✅ Valid rules: {len(valid_rules)} rule(s)")
    for rule in valid_rules:
        print(f"   • {rule['name']} from {rule['file']}")
    
    if invalid_rules:
        print(f"\n❌ Invalid rules: {len(invalid_rules)} rule(s)")
        for rule in invalid_rules:
            print(f"   • {rule['file']} - {rule['error']}")
    
    # Save summary to file
    summary = {
        "total_files": len(yaml_files),
        "valid": len(valid_rules),
        "invalid": len(invalid_rules),
        "valid_rules": valid_rules,
        "invalid_rules": invalid_rules,
        "timestamp": "2025-12-03T05:57:00Z"
    }
    
    output_file = "validation-summary.json"
    save_to_file(summary, output_file)
    
    if invalid_rules and not continue_on_error:
        sys.exit(1)
    elif invalid_rules:
        print(f"\n⚠️  Completed with {len(invalid_rules)} validation failures")
    else:
        print(f"\n🎉 All {len(valid_rules)} rules are valid and ready for deployment!")


def list_rules_from_yaml(filter_query=None, limit=100):
    """
    List existing custom rules.
    
    Args:
        filter_query: Optional FQL filter
        limit: Maximum number of rules to return
    """
    print("📋 Listing Custom Rules")
    print("=" * 60)
    
    # Initialize Falcon API
    falcon = APIHarnessV2()
    
    # Get rule list
    result = get_custom_rules(falcon, filter_query, limit)
    
    if result:
        print(f"✅ Found {len(result)} custom rules")
        
        # Save results to file
        output_file = "custom-rules-list.json"
        save_to_file(result, output_file)
    else:
        print("❌ Failed to retrieve custom rules")
        sys.exit(1)


def get_schema_from_yaml(config_file):
    """
    Get input schema for the resource type specified in YAML config.
    
    Args:
        config_file: Path to YAML configuration file
    """
    print(f"📋 Getting Input Schema from YAML: {config_file}")
    print("=" * 60)
    
    # Load configuration
    config = load_yaml_config(config_file)
    
    if not validate_yaml_config(config):
        sys.exit(1)
    
    rule = config['rule']
    
    # Initialize Falcon API
    falcon = APIHarnessV2()
    
    # Map platform to provider format
    provider_map = {"AWS": "aws", "Azure": "azure", "GCP": "gcp", "OCI": "oci"}
    provider_lower = provider_map.get(rule['platform'], rule['platform'].lower())
    
    print(f"🔍 Getting schema for {rule['resource_type']} on {rule['platform']}...")
    
    # Get input schema
    result = get_input_schema(
        falcon, provider_lower, rule['resource_type'],
        rule.get('domain', 'CSPM'), rule.get('subdomain', 'IOM')
    )
    
    if result:
        print("✅ Schema retrieved successfully!")
        
        # Save schema to file
        output_file = f"schema-{rule['resource_type'].lower().replace('::', '-')}.json"
        save_to_file(result, output_file)
    else:
        print("❌ Failed to retrieve schema")
        sys.exit(1)

def get_resource_ids_command(provider=None, resource_type=None, filter_query=None, limit=10):
    """
    Get real resource IDs for testing rules.
    
    Args:
        provider: Cloud provider (aws, azure, gcp, oci)
        resource_type: Resource type (e.g., EC2::Instance)
        filter_query: FQL filter string
        limit: Maximum number of IDs to return
    """
    print("🔍 Getting Real Resource IDs")
    print("=" * 60)
    
    # Initialize Falcon API
    falcon = APIHarnessV2()
    
    # Build filter query
    filters = []
    if provider:
        filters.append(f'cloud_provider:"{provider}"')
    if resource_type:
        filters.append(f'resource_type:"{resource_type}"')
    if filter_query:
        filters.append(filter_query)
    
    combined_filter = "+".join(filters) if filters else None
    
    if combined_filter:
        print(f"📋 Filter: {combined_filter}")
    else:
        print("📋 No filters applied - getting all resources")
    
    print(f"📊 Limit: {limit}")
    print()
    
    # Get resource IDs
    result = get_sample_resource_ids(falcon, combined_filter, limit=limit)
    
    if result:
        print(f"✅ Found {len(result)} resource IDs")
        
        # Save results to file
        output_file = "resource-ids.json"
        save_to_file(result, output_file)
        
        # Display first few IDs
        print("\n📋 Sample Resource IDs:")
        for i, resource_id in enumerate(result[:5]):
            print(f"   {i+1}. {resource_id}")
        
        if len(result) > 5:
            print(f"   ... and {len(result) - 5} more (see {output_file})")
        
        # Get detailed info for first resource
        if result:
            print(f"\n🔍 Getting details for first resource: {result[0]}")
            details = get_sample_resource(falcon, [result[0]])
            if details:
                detail_file = "sample-resource-details.json"
                save_to_file(details, detail_file)
                print(f"✅ Resource details saved to: {detail_file}")
    else:
        print("❌ No resource IDs found")
        sys.exit(1)


def delete_rules_command(rule_ids, confirm=False):
    """
    Delete custom rules by UUID.
    
    Args:
        rule_ids: List of rule UUIDs to delete
        confirm: Skip confirmation prompt if True
    """
    print("🗑️  Deleting Custom Rules")
    print("=" * 60)
    
    # Initialize Falcon API
    falcon = APIHarnessV2()
    
    # Show rules to be deleted
    print(f"📋 Rules to delete: {len(rule_ids)}")
    for i, rule_id in enumerate(rule_ids, 1):
        print(f"   {i}. {rule_id}")
    
    # Confirmation prompt
    if not confirm:
        response = input(f"\n⚠️  Are you sure you want to delete {len(rule_ids)} rule(s)? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("❌ Operation cancelled")
            return
    
    print(f"\n🗑️  Deleting {len(rule_ids)} rule(s)...")
    
    # Delete the rules
    result = delete_custom_rules(falcon, rule_ids)
    
    if result is not None:
        print(f"✅ Successfully deleted {len(rule_ids)} rule(s)")
        
        # Save result to file
        output_file = "deleted-rules-result.json"
        save_to_file({"deleted_rule_ids": rule_ids, "result": result}, output_file)
    else:
        print("❌ Failed to delete rules")
        sys.exit(1)


def update_rule_command(rule_id, name=None, description=None, severity=None, alert_info=None):
    """
    Update an existing custom rule.
    
    Args:
        rule_id: Rule UUID to update
        name: New rule name
        description: New rule description
        severity: New severity (0-3)
        alert_info: New alert info
    """
    print("📝 Updating Custom Rule")
    print("=" * 60)
    
    # Initialize Falcon API
    falcon = APIHarnessV2()
    
    print(f"📋 Rule ID: {rule_id}")
    
    # Show what will be updated
    updates = []
    if name:
        updates.append(f"Name: {name}")
    if description:
        updates.append(f"Description: {description}")
    if severity is not None:
        severity_names = {0: "Critical", 1: "High", 2: "Medium", 3: "Informational"}
        updates.append(f"Severity: {severity} ({severity_names.get(severity, 'Unknown')})")
    if alert_info:
        updates.append(f"Alert Info: {alert_info}")
    
    if not updates:
        print("❌ No updates specified. Use --name, --description, --severity, or --alert-info")
        sys.exit(1)
    
    print("📝 Updates to apply:")
    for update in updates:
        print(f"   • {update}")
    
    print(f"\n📝 Updating rule...")
    
    # Update the rule
    result = update_custom_rule(
        falcon, rule_id, name, description, severity, alert_info
    )
    
    if result:
        print(f"✅ Rule '{rule_id}' updated successfully!")
        
        # Save result to file
        output_file = f"updated-rule-{rule_id}.json"
        save_to_file(result, output_file)
    else:
        print(f"❌ Failed to update rule '{rule_id}'")
        sys.exit(1)


def get_rule_details_command(rule_ids):
    """
    Get detailed information about specific rules.
    
    Args:
        rule_ids: List of rule UUIDs to get details for
    """
    print("📋 Getting Rule Details")
    print("=" * 60)
    
    # Initialize Falcon API
    falcon = APIHarnessV2()
    
    print(f"🔍 Getting details for {len(rule_ids)} rule(s)...")
    
    # Get rule details
    result = get_rule_details(falcon, rule_ids)
    
    if result:
        print(f"✅ Retrieved details for {len(result)} rule(s)")
        
        # Save result to file
        output_file = "rule-details.json"
        save_to_file(result, output_file)
        
        # Display summary
        print("\n📊 Rule Summary:")
        for rule in result:
            print(f"   • {rule.get('name', 'Unknown')} ({rule.get('uuid', 'No UUID')})")
            print(f"     Platform: {rule.get('provider', 'Unknown')}")
            print(f"     Severity: {rule.get('severity', 'Unknown')}")
            print(f"     Created: {rule.get('created_at', 'Unknown')}")
            print()
    else:
        print("❌ Failed to retrieve rule details")
        sys.exit(1)


def create_all_rules_command(rules_dir="rules", environment="production", continue_on_error=False):
    """
    Create all rules from YAML files in the specified directory.
    
    Args:
        rules_dir: Directory containing YAML rule files
        environment: Target environment (staging/production)
        continue_on_error: Continue creating other rules if one fails
    """
    print("🚀 Creating All Rules from Directory")
    print("=" * 60)
    
    if not os.path.exists(rules_dir):
        print(f"❌ Rules directory '{rules_dir}' not found")
        sys.exit(1)
    
    # Find all YAML files in the directory
    yaml_files = []
    for file in os.listdir(rules_dir):
        if file.endswith(('.yaml', '.yml')) and not file.startswith('.'):
            yaml_files.append(os.path.join(rules_dir, file))
    
    if not yaml_files:
        print(f"❌ No YAML files found in '{rules_dir}' directory")
        sys.exit(1)
    
    print(f"📋 Found {len(yaml_files)} YAML rule file(s):")
    for i, file in enumerate(yaml_files, 1):
        print(f"   {i}. {file}")
    
    print(f"\n📍 Target environment: {environment}")
    print(f"🔄 Continue on error: {'Yes' if continue_on_error else 'No'}")
    print()
    
    # Track results
    successful_rules = []
    failed_rules = []
    
    # Process each YAML file
    for yaml_file in yaml_files:
        print(f"🔄 Processing: {yaml_file}")
        print("-" * 40)
        
        try:
            # Load and validate configuration
            config = load_yaml_config(yaml_file)
            
            if not validate_yaml_config(config):
                if continue_on_error:
                    print(f"⚠️  Skipping {yaml_file} due to validation errors")
                    failed_rules.append({"file": yaml_file, "error": "Validation failed"})
                    continue
                else:
                    print(f"❌ Stopping due to validation errors in {yaml_file}")
                    sys.exit(1)
            
            rule = config['rule']
            
            # Validate Rego logic
            if not validate_rego_syntax(rule['logic']):
                if continue_on_error:
                    print(f"⚠️  Skipping {yaml_file} due to Rego validation errors")
                    failed_rules.append({"file": yaml_file, "error": "Rego validation failed"})
                    continue
                else:
                    print(f"❌ Stopping due to Rego validation errors in {yaml_file}")
                    sys.exit(1)
            
            # Initialize Falcon API
            falcon = APIHarnessV2()
            
            # Prepare rule parameters
            name = rule['name']
            description = rule['description']
            resource_type = rule['resource_type']
            logic = rule['logic']
            platform = rule['platform']
            provider = rule['provider']
            domain = rule.get('domain', 'CSPM')
            subdomain = rule.get('subdomain', 'IOM')
            severity = rule.get('severity', 1)
            alert_info = rule.get('alert_info')
            remediation = rule.get('remediation')
            attack_types = rule.get('attack_types')
            controls = rule.get('controls')
            
            print(f"📋 Creating rule: {name}")
            
            # Create the rule
            result = create_custom_rule(
                falcon, name, description, resource_type, logic,
                platform, provider, domain, subdomain, severity,
                alert_info, remediation, attack_types, controls
            )
            
            if result:
                print(f"✅ Rule '{name}' created successfully!")
                successful_rules.append({"file": yaml_file, "name": name, "uuid": result[0].get('uuid') if result else None})
            else:
                if continue_on_error:
                    print(f"⚠️  Failed to create rule '{name}' from {yaml_file}")
                    failed_rules.append({"file": yaml_file, "name": name, "error": "API creation failed"})
                else:
                    print(f"❌ Stopping due to creation failure for rule '{name}' from {yaml_file}")
                    sys.exit(1)
        
        except Exception as e:
            error_msg = str(e)
            if continue_on_error:
                print(f"⚠️  Error processing {yaml_file}: {error_msg}")
                failed_rules.append({"file": yaml_file, "error": error_msg})
            else:
                print(f"❌ Error processing {yaml_file}: {error_msg}")
                sys.exit(1)
        
        print()  # Add spacing between files
    
    # Summary
    print("=" * 60)
    print("📊 BULK CREATION SUMMARY")
    print("=" * 60)
    
    print(f"✅ Successfully created: {len(successful_rules)} rule(s)")
    for rule in successful_rules:
        uuid_info = f" (UUID: {rule['uuid']})" if rule.get('uuid') else ""
        print(f"   • {rule['name']} from {rule['file']}{uuid_info}")
    
    if failed_rules:
        print(f"\n❌ Failed to create: {len(failed_rules)} rule(s)")
        for rule in failed_rules:
            name_info = f" ({rule.get('name', 'Unknown')})" if rule.get('name') else ""
            print(f"   • {rule['file']}{name_info} - {rule['error']}")
    
    # Save summary to file
    summary = {
        "total_files": len(yaml_files),
        "successful": len(successful_rules),
        "failed": len(failed_rules),
        "successful_rules": successful_rules,
        "failed_rules": failed_rules,
        "environment": environment,
        "timestamp": "2025-11-21T05:53:30Z"
    }
    
    output_file = f"bulk-creation-summary-{environment}.json"
    save_to_file(summary, output_file)
    
    if failed_rules and not continue_on_error:
        sys.exit(1)
    elif failed_rules:
        print(f"\n⚠️  Completed with {len(failed_rules)} failures")
    else:
        print(f"\n🎉 All {len(successful_rules)} rules created successfully!")


def deploy_all_rules_command(rules_dir="rules", environment="production", continue_on_error=False):
    """
    Deploy all rules from YAML files (idempotent: create new or update existing).
    
    Args:
        rules_dir: Directory containing YAML rule files
        environment: Target environment (staging/production)
        continue_on_error: Continue processing other rules if one fails
    """
    print("🚀 Deploying All Rules (Create/Update)")
    print("=" * 60)
    
    if not os.path.exists(rules_dir):
        print(f"❌ Rules directory '{rules_dir}' not found")
        sys.exit(1)
    
    # Find all YAML files in the directory
    yaml_files = []
    for file in os.listdir(rules_dir):
        if file.endswith(('.yaml', '.yml')) and not file.startswith('.'):
            yaml_files.append(os.path.join(rules_dir, file))
    
    if not yaml_files:
        print(f"❌ No YAML files found in '{rules_dir}' directory")
        sys.exit(1)
    
    print(f"📋 Found {len(yaml_files)} YAML rule file(s):")
    for i, file in enumerate(yaml_files, 1):
        print(f"   {i}. {file}")
    
    print(f"\n📍 Target environment: {environment}")
    print(f"🔄 Continue on error: {'Yes' if continue_on_error else 'No'}")
    print()
    
    # Initialize Falcon API once
    falcon = APIHarnessV2()
    
    # Get existing rules to check for duplicates
    print("🔍 Checking existing rules...")
    existing_rules = get_all_custom_rules_paginated(falcon, max_rules=5000)  # Use pagination to get more rules
    existing_rule_names = {}
    
    if existing_rules:
        # Get details for existing rules to map names to UUIDs
        print("📋 Getting details for existing rules...")
        rule_details = get_rule_details(falcon, existing_rules)
        if rule_details:
            for rule in rule_details:
                existing_rule_names[rule.get('name')] = rule.get('uuid')
        print(f"✅ Found {len(existing_rule_names)} existing rules")
    else:
        print("📋 No existing rules found")
    
    print()
    
    # Track results
    created_rules = []
    updated_rules = []
    failed_rules = []
    
    # Process each YAML file
    for yaml_file in yaml_files:
        print(f"🔄 Processing: {yaml_file}")
        print("-" * 40)
        
        try:
            # Load and validate configuration
            config = load_yaml_config(yaml_file)
            
            if not validate_yaml_config(config):
                if continue_on_error:
                    print(f"⚠️  Skipping {yaml_file} due to validation errors")
                    failed_rules.append({"file": yaml_file, "error": "Validation failed"})
                    continue
                else:
                    print(f"❌ Stopping due to validation errors in {yaml_file}")
                    sys.exit(1)
            
            rule = config['rule']
            
            # Validate Rego logic
            if not validate_rego_syntax(rule['logic']):
                if continue_on_error:
                    print(f"⚠️  Skipping {yaml_file} due to Rego validation errors")
                    failed_rules.append({"file": yaml_file, "error": "Rego validation failed"})
                    continue
                else:
                    print(f"❌ Stopping due to Rego validation errors in {yaml_file}")
                    sys.exit(1)
            
            # Prepare rule parameters
            name = rule['name']
            description = rule['description']
            resource_type = rule['resource_type']
            logic = rule['logic']
            platform = rule['platform']
            provider = rule['provider']
            domain = rule.get('domain', 'CSPM')
            subdomain = rule.get('subdomain', 'IOM')
            severity = rule.get('severity', 1)
            alert_info = rule.get('alert_info')
            remediation = rule.get('remediation')
            attack_types = rule.get('attack_types')
            controls = rule.get('controls')
            
            # Check if rule already exists
            existing_uuid = existing_rule_names.get(name)
            
            if existing_uuid:
                # Update existing rule
                print(f"🔄 Updating existing rule: {name} (UUID: {existing_uuid})")
                
                result = update_custom_rule(
                    falcon, existing_uuid, name, description, severity, alert_info
                )
                
                if result:
                    print(f"✅ Rule '{name}' updated successfully!")
                    updated_rules.append({"file": yaml_file, "name": name, "uuid": existing_uuid})
                else:
                    if continue_on_error:
                        print(f"⚠️  Failed to update rule '{name}' from {yaml_file}")
                        failed_rules.append({"file": yaml_file, "name": name, "error": "API update failed"})
                    else:
                        print(f"❌ Stopping due to update failure for rule '{name}' from {yaml_file}")
                        sys.exit(1)
            else:
                # Create new rule
                print(f"➕ Creating new rule: {name}")
                
                result = create_custom_rule(
                    falcon, name, description, resource_type, logic,
                    platform, provider, domain, subdomain, severity,
                    alert_info, remediation, attack_types, controls
                )
                
                if result:
                    new_uuid = result[0].get('uuid') if result else None
                    print(f"✅ Rule '{name}' created successfully! (UUID: {new_uuid})")
                    created_rules.append({"file": yaml_file, "name": name, "uuid": new_uuid})
                    # Add to existing rules for subsequent checks
                    if new_uuid:
                        existing_rule_names[name] = new_uuid
                else:
                    if continue_on_error:
                        print(f"⚠️  Failed to create rule '{name}' from {yaml_file}")
                        failed_rules.append({"file": yaml_file, "name": name, "error": "API creation failed"})
                    else:
                        print(f"❌ Stopping due to creation failure for rule '{name}' from {yaml_file}")
                        sys.exit(1)
        
        except Exception as e:
            error_msg = str(e)
            if continue_on_error:
                print(f"⚠️  Error processing {yaml_file}: {error_msg}")
                failed_rules.append({"file": yaml_file, "error": error_msg})
            else:
                print(f"❌ Error processing {yaml_file}: {error_msg}")
                sys.exit(1)
        
        print()  # Add spacing between files
    
    # Summary
    print("=" * 60)
    print("📊 DEPLOYMENT SUMMARY")
    print("=" * 60)
    
    print(f"➕ Created: {len(created_rules)} rule(s)")
    for rule in created_rules:
        uuid_info = f" (UUID: {rule['uuid']})" if rule.get('uuid') else ""
        print(f"   • {rule['name']} from {rule['file']}{uuid_info}")
    
    print(f"\n🔄 Updated: {len(updated_rules)} rule(s)")
    for rule in updated_rules:
        uuid_info = f" (UUID: {rule['uuid']})" if rule.get('uuid') else ""
        print(f"   • {rule['name']} from {rule['file']}{uuid_info}")
    
    if failed_rules:
        print(f"\n❌ Failed: {len(failed_rules)} rule(s)")
        for rule in failed_rules:
            name_info = f" ({rule.get('name', 'Unknown')})" if rule.get('name') else ""
            print(f"   • {rule['file']}{name_info} - {rule['error']}")
    
    # Save summary to file
    summary = {
        "total_files": len(yaml_files),
        "created": len(created_rules),
        "updated": len(updated_rules),
        "failed": len(failed_rules),
        "created_rules": created_rules,
        "updated_rules": updated_rules,
        "failed_rules": failed_rules,
        "environment": environment,
        "timestamp": "2025-11-21T05:54:21Z"
    }
    
    output_file = f"deployment-summary-{environment}.json"
    save_to_file(summary, output_file)
    
    total_success = len(created_rules) + len(updated_rules)
    
    if failed_rules and not continue_on_error:
        sys.exit(1)
    elif failed_rules:
        print(f"\n⚠️  Completed with {len(failed_rules)} failures")
    else:
        print(f"\n🎉 All {total_success} rules deployed successfully!")
        print(f"   • {len(created_rules)} created")
        print(f"   • {len(updated_rules)} updated")


def get_all_custom_rules_paginated(falcon, filter_query=None, max_rules=5000):
    """
    Get all custom rules using pagination to handle large numbers of rules.
    
    Args:
        falcon: APIHarnessV2 instance
        filter_query: FQL filter string
        max_rules: Maximum total number of rules to retrieve
        
    Returns:
        List of all rule IDs
    """
    all_rules = []
    offset = 0
    page_size = 500  # Maximum allowed by API
    total_retrieved = 0
    
    print(f"📋 Using pagination with {page_size} rules per request...")
    
    while total_retrieved < max_rules:
        # Calculate how many rules to request in this batch
        remaining = max_rules - total_retrieved
        current_limit = min(page_size, remaining)
        
        print(f"   📄 Fetching batch {offset // page_size + 1}: offset={offset}, limit={current_limit}")
        
        # Get this batch of rules
        batch_rules = get_custom_rules(falcon, filter_query, current_limit, offset)
        
        if not batch_rules:
            # No more rules available
            break
        
        all_rules.extend(batch_rules)
        total_retrieved += len(batch_rules)
        
        print(f"   ✅ Retrieved {len(batch_rules)} rules (total: {total_retrieved})")
        
        # If we got fewer rules than requested, we've reached the end
        if len(batch_rules) < current_limit:
            print(f"   📋 Reached end of available rules")
            break
        
        # Move to next batch
        offset += current_limit
    
    print(f"📊 Pagination complete: {len(all_rules)} total rules retrieved")
    return all_rules


def export_all_rules_command(output_dir="exported-rules", filter_query=None, limit=5000):
    """
    Export all existing rules to YAML files with automatic pagination.
    
    Args:
        output_dir: Directory to save YAML files
        filter_query: FQL filter to limit which rules to export
        limit: Maximum number of rules to export (will use pagination if > 500)
    """
    print("📤 Exporting All Rules to YAML Files")
    print("=" * 60)
    
    # Initialize Falcon API
    falcon = APIHarnessV2()
    
    # Get existing rules with pagination
    print("🔍 Fetching existing rules with pagination...")
    existing_rules = get_all_custom_rules_paginated(falcon, filter_query, limit)
    
    if not existing_rules:
        print("❌ No rules found to export")
        sys.exit(1)
    
    print(f"✅ Found {len(existing_rules)} rules to export")
    
    # Get detailed information for all rules
    print("📋 Getting detailed rule information...")
    rule_details = get_rule_details(falcon, existing_rules)
    
    if not rule_details:
        print("❌ Failed to get rule details")
        sys.exit(1)
    
    print(f"✅ Retrieved details for {len(rule_details)} rules")
    
    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created output directory: {output_dir}")
    
    # Track results
    exported_rules = []
    failed_exports = []
    
    # Process each rule
    for rule in rule_details:
        try:
            rule_name = rule.get('name', 'Unknown')
            rule_uuid = rule.get('uuid', 'unknown')
            
            print(f"📤 Exporting: {rule_name}")
            
            # Create YAML structure
            yaml_content = {
                'metadata': {
                    'version': '1.0',
                    'exported_from': 'CrowdStrike API',
                    'original_uuid': rule_uuid,
                    'created_at': rule.get('created_at'),
                    'updated_at': rule.get('updated_at', rule.get('created_at')),
                    'created_by': rule.get('created_by'),
                    'updated_by': rule.get('updated_by', rule.get('created_by'))
                },
                'rule': {
                    'name': rule_name,
                    'description': rule.get('description', ''),
                    'resource_type': rule.get('resource_types', [{}])[0].get('resource_type', 'Unknown') if rule.get('resource_types') else 'Unknown',
                    'platform': rule.get('provider', 'Unknown'),
                    'provider': rule.get('provider', 'Unknown'),
                    'domain': rule.get('domain', 'CSPM'),
                    'subdomain': rule.get('subdomain', 'IOM'),
                    'severity': rule.get('severity', 1),
                    'logic': rule.get('logic', ''),
                }
            }
            
            # Add optional fields if they exist
            if rule.get('alert_info'):
                yaml_content['rule']['alert_info'] = rule.get('alert_info')
            
            if rule.get('remediation'):
                yaml_content['rule']['remediation'] = rule.get('remediation')
            
            if rule.get('attack_types') and rule.get('attack_types') != ['']:
                yaml_content['rule']['attack_types'] = [at for at in rule.get('attack_types', []) if at]
            
            if rule.get('controls'):
                yaml_content['rule']['controls'] = rule.get('controls')
            
            # Create safe filename
            safe_name = rule_name.replace(' ', '-').replace('_', '-').lower()
            # Remove any characters that aren't alphanumeric, hyphens, or dots
            safe_name = ''.join(c for c in safe_name if c.isalnum() or c in '-.')
            filename = f"{safe_name}.yaml"
            filepath = os.path.join(output_dir, filename)
            
            # Handle duplicate filenames
            counter = 1
            original_filepath = filepath
            while os.path.exists(filepath):
                name_part = safe_name
                filepath = os.path.join(output_dir, f"{name_part}-{counter}.yaml")
                counter += 1
            
            # Write YAML file
            with open(filepath, 'w') as f:
                yaml.dump(yaml_content, f, default_flow_style=False, sort_keys=False, indent=2)
            
            exported_rules.append({
                'name': rule_name,
                'uuid': rule_uuid,
                'filename': os.path.basename(filepath)
            })
            
            print(f"   ✅ Saved to: {filepath}")
        
        except Exception as e:
            error_msg = str(e)
            print(f"   ❌ Failed to export {rule.get('name', 'Unknown')}: {error_msg}")
            failed_exports.append({
                'name': rule.get('name', 'Unknown'),
                'uuid': rule.get('uuid', 'unknown'),
                'error': error_msg
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 EXPORT SUMMARY")
    print("=" * 60)
    
    print(f"✅ Successfully exported: {len(exported_rules)} rule(s)")
    for rule in exported_rules[:10]:  # Show first 10
        print(f"   • {rule['name']} → {rule['filename']}")
    
    if len(exported_rules) > 10:
        print(f"   ... and {len(exported_rules) - 10} more")
    
    if failed_exports:
        print(f"\n❌ Failed to export: {len(failed_exports)} rule(s)")
        for rule in failed_exports:
            print(f"   • {rule['name']} - {rule['error']}")
    
    # Save summary to file
    summary = {
        "total_rules": len(rule_details),
        "exported": len(exported_rules),
        "failed": len(failed_exports),
        "output_directory": output_dir,
        "exported_rules": exported_rules,
        "failed_exports": failed_exports,
        "timestamp": "2025-11-21T05:56:08Z"
    }
    
    summary_file = os.path.join(output_dir, "export-summary.json")
    save_to_file(summary, summary_file)
    
    print(f"\n📁 All files saved to: {output_dir}")
    print(f"📋 Export summary: {summary_file}")
    
    if failed_exports:
        print(f"\n⚠️  Completed with {len(failed_exports)} failures")
    else:
        print(f"\n🎉 All {len(exported_rules)} rules exported successfully!")


def main():
    """Main function to parse arguments and execute commands."""
    parser = argparse.ArgumentParser(
        description="CrowdStrike YAML-Based Rule Manager - Complete Self-Contained Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate YAML configuration
  python3 rule-manager.py validate --config example-ec2-security-rule.yaml

  # Test rule logic
  python3 rule-manager.py test --config example-ec2-security-rule.yaml

  # Create rule in production
  python3 rule-manager.py create --config example-ec2-security-rule.yaml

  # Create rule in staging
  python3 rule-manager.py create --config example-ec2-security-rule.yaml --environment staging

  # List existing custom rules
  python3 rule-manager.py list --filter 'rule_name:"MyRule"'

  # Get input schema for resource type in YAML
  python3 rule-manager.py schema --config example-ec2-security-rule.yaml

  # Get real resource IDs for testing
  python3 rule-manager.py get-resource-ids --provider aws --resource-type "EC2::Instance" --limit 5

  # Get rule details
  python3 rule-manager.py details --rule-ids 7c4f9a81-3c50-47c7-83a2-c89459ad833f

  # Update rule
  python3 rule-manager.py update --rule-id 7c4f9a81-3c50-47c7-83a2-c89459ad833f --name "Updated-Rule-Name" --severity 1

  # Delete rule
  python3 rule-manager.py delete --rule-ids 7c4f9a81-3c50-47c7-83a2-c89459ad833f --confirm

  # Validate all rules in directory
  python3 rule-manager.py validate-all --rules-dir my-rules --continue-on-error

  # Deploy all rules (create new or update existing)
  python3 rule-manager.py deploy-all --rules-dir my-rules --continue-on-error

  # Export all custom rules to YAML files
  python3 rule-manager.py export-all --filter 'rule_origin:!"Default"' --output-dir exported-rules
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Validate command
    parser_validate = subparsers.add_parser("validate", help="Validate YAML configuration")
    parser_validate.add_argument("--config", required=True, help="Path to YAML configuration file")
    
    # Test command
    parser_test = subparsers.add_parser("test", help="Test rule logic")
    parser_test.add_argument("--config", required=True, help="Path to YAML configuration file")
    parser_test.add_argument("--environment", default="staging", choices=["staging", "production"], 
                           help="Test environment (default: staging)")
    
    # Create command
    parser_create = subparsers.add_parser("create", help="Create rule from YAML configuration")
    parser_create.add_argument("--config", required=True, help="Path to YAML configuration file")
    parser_create.add_argument("--environment", default="production", choices=["staging", "production"], 
                             help="Target environment (default: production)")
    
    # List command
    parser_list = subparsers.add_parser("list", help="List existing custom rules")
    parser_list.add_argument("--filter", help="FQL filter string")
    parser_list.add_argument("--limit", type=int, default=100, help="Maximum number of rules (default: 100)")
    
    # Schema command
    parser_schema = subparsers.add_parser("schema", help="Get input schema for resource type")
    parser_schema.add_argument("--config", required=True, help="Path to YAML configuration file")
    
    # Get resource IDs command
    parser_resources = subparsers.add_parser("get-resource-ids", help="Get real resource IDs for testing")
    parser_resources.add_argument("--provider", choices=["aws", "azure", "gcp", "oci"],
                                help="Cloud provider (aws, azure, gcp, oci)")
    parser_resources.add_argument("--resource-type", help="Resource type (e.g., EC2::Instance)")
    parser_resources.add_argument("--filter", help="FQL filter string")
    parser_resources.add_argument("--limit", type=int, default=10, help="Maximum number of IDs (default: 10)")
    
    # Delete command
    parser_delete = subparsers.add_parser("delete", help="Delete custom rules")
    parser_delete.add_argument("--rule-ids", required=True, nargs="+", help="Rule UUIDs to delete")
    parser_delete.add_argument("--confirm", action="store_true", help="Skip confirmation prompt")
    
    # Update command
    parser_update = subparsers.add_parser("update", help="Update existing custom rule")
    parser_update.add_argument("--rule-id", required=True, help="Rule UUID to update")
    parser_update.add_argument("--name", help="New rule name")
    parser_update.add_argument("--description", help="New rule description")
    parser_update.add_argument("--severity", type=int, choices=[0, 1, 2, 3], help="New severity (0=critical, 1=high, 2=medium, 3=informational)")
    parser_update.add_argument("--alert-info", help="New alert info")
    
    # Get rule details command
    parser_details = subparsers.add_parser("details", help="Get detailed information about specific rules")
    parser_details.add_argument("--rule-ids", required=True, nargs="+", help="Rule UUIDs to get details for")
    
    # Create all rules command
    parser_create_all = subparsers.add_parser("create-all", help="Create all rules from YAML files in rules directory")
    parser_create_all.add_argument("--rules-dir", default="rules", help="Directory containing YAML rule files (default: rules)")
    parser_create_all.add_argument("--environment", default="production", choices=["staging", "production"],
                                 help="Target environment (default: production)")
    parser_create_all.add_argument("--continue-on-error", action="store_true", help="Continue creating other rules if one fails")
    
    # Deploy all rules command (idempotent create/update)
    parser_deploy_all = subparsers.add_parser("deploy-all", help="Deploy all rules (create new or update existing) from YAML files")
    parser_deploy_all.add_argument("--rules-dir", default="rules", help="Directory containing YAML rule files (default: rules)")
    parser_deploy_all.add_argument("--environment", default="production", choices=["staging", "production"],
                                 help="Target environment (default: production)")
    parser_deploy_all.add_argument("--continue-on-error", action="store_true", help="Continue processing other rules if one fails")
    
    # Validate all rules command
    parser_validate_all = subparsers.add_parser("validate-all", help="Validate all rules from YAML files in directory")
    parser_validate_all.add_argument("--rules-dir", default="rules", help="Directory containing YAML rule files (default: rules)")
    parser_validate_all.add_argument("--continue-on-error", action="store_true", help="Continue validating other rules if one fails")
    
    
    # Export all rules command
    parser_export_all = subparsers.add_parser("export-all", help="Export all existing rules to YAML files")
    parser_export_all.add_argument("--output-dir", default="exported-rules", help="Directory to save YAML files (default: exported-rules)")
    parser_export_all.add_argument("--filter", help="FQL filter to limit which rules to export")
    parser_export_all.add_argument("--limit", type=int, default=5000, help="Maximum number of rules to export (default: 5000)")
    
    args = parser.parse_args()
    
    # Show help if no command provided
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Check if configuration file exists (for commands that need it)
    if hasattr(args, 'config') and args.config and not os.path.exists(args.config):
        print(f"✗ Error: Configuration file '{args.config}' not found")
        sys.exit(1)
    
    # Execute command
    try:
        if args.command == "validate":
            validate_rule_from_yaml(args.config)
        
        elif args.command == "test":
            test_rule_from_yaml(args.config, args.environment)
        
        elif args.command == "create":
            create_rule_from_yaml(args.config, args.environment)
        
        elif args.command == "list":
            list_rules_from_yaml(args.filter, args.limit)
        
        elif args.command == "schema":
            get_schema_from_yaml(args.config)
        
        elif args.command == "get-resource-ids":
            get_resource_ids_command(args.provider, getattr(args, 'resource_type'), args.filter, args.limit)
        
        elif args.command == "delete":
            delete_rules_command(args.rule_ids, args.confirm)
        
        elif args.command == "update":
            update_rule_command(args.rule_id, args.name, args.description, args.severity, getattr(args, 'alert_info'))
        
        elif args.command == "details":
            get_rule_details_command(args.rule_ids)
        
        elif args.command == "create-all":
            create_all_rules_command(args.rules_dir, args.environment, args.continue_on_error)
        
        elif args.command == "deploy-all":
            deploy_all_rules_command(args.rules_dir, args.environment, args.continue_on_error)
        
        elif args.command == "validate-all":
            validate_all_rules_command(args.rules_dir, args.continue_on_error)
        
        
        elif args.command == "export-all":
            export_all_rules_command(args.output_dir, args.filter, args.limit)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error executing command: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()