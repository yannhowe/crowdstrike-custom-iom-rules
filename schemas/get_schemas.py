

#!/usr/bin/env python3
"""
CrowdStrike Schema Manager

A standalone tool for managing CrowdStrike resource schemas.
Fetches schemas from CrowdStrike APIs using resource type lists from resource-support files.
"""

import argparse
import json
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from falconpy import APIHarnessV2
from dotenv import load_dotenv

# Load environment variables from .env file (look in parent directory)
load_dotenv("../.env")


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


def generate_all_schemas_command(output_dir=".", limit=1000):
    """
    Generate schemas for all resource types discovered from existing rules.
    
    Args:
        output_dir: Directory to save schema JSON files
        limit: Maximum number of rules to scan for discovery
    """
    print("📋 Generating Schemas for All Resource Types")
    print("=" * 60)
    
    # Initialize Falcon API
    falcon = APIHarnessV2()
    
    # Step 1: Try to discover resource types from actual cloud resources (optional)
    print("🔍 Step 1: Attempting to discover resource types from cloud resources...")
    resource_types_from_assets = set()
    
    try:
        # Get sample resources from all providers (this may fail due to permissions)
        providers = ["aws", "azure", "gcp", "oci"]
        for provider in providers:
            print(f"   📡 Scanning {provider.upper()} resources...")
            filter_query = f'cloud_provider:"{provider}"'
            resource_ids = get_sample_resource_ids(falcon, filter_query, limit=min(limit//4, 250))
            
            if resource_ids:
                # Get details for a sample of resources to extract resource types
                sample_size = min(50, len(resource_ids))
                sample_ids = resource_ids[:sample_size]
                resource_details = get_sample_resource(falcon, sample_ids)
                
                if resource_details:
                    for resource in resource_details:
                        resource_type = resource.get('resource_type')
                        if resource_type:
                            resource_types_from_assets.add((provider, resource_type))
                            print(f"      ✅ Found: {resource_type}")
    except Exception as e:
        print(f"   ⚠️  Cloud resource scanning failed (insufficient permissions): {str(e)}")
    
    print(f"   📊 Discovered {len(resource_types_from_assets)} resource types from cloud assets")
    
    # Step 2: Discover resource types from existing rules (primary method)
    print("\n🔍 Step 2: Discovering resource types from existing rules...")
    resource_types_from_rules = set()
    
    # Get all existing rules (fix the function call)
    existing_rules = get_all_custom_rules_paginated(falcon, max_rules=5000)
    if existing_rules:
        rule_details = get_rule_details(falcon, existing_rules)
        if rule_details:
            for rule in rule_details:
                provider = rule.get('provider')
                resource_types = rule.get('resource_types', [])
                
                if provider and resource_types:
                    provider_lower = provider.lower()
                    for rt in resource_types:
                        resource_type = rt.get('resource_type')
                        if resource_type:
                            resource_types_from_rules.add((provider_lower, resource_type))
                            print(f"      ✅ Found: {resource_type} ({provider})")
    
    print(f"   📊 Discovered {len(resource_types_from_rules)} resource types from existing rules")
    
    # Step 3: Combine and deduplicate
    all_resource_types = resource_types_from_assets.union(resource_types_from_rules)
    print(f"\n📊 Total unique resource types discovered: {len(all_resource_types)}")
    
    if not all_resource_types:
        print("❌ No resource types found. Make sure you have existing rules in your CrowdStrike environment.")
        print("💡 Try running: python rule-manager.py list --limit 10")
        return
    
    # Step 4: Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created output directory: {output_dir}")
    
    # Step 5: Generate schemas for each resource type
    print(f"\n🔧 Step 3: Generating schemas for {len(all_resource_types)} resource types...")
    successful_schemas = []
    failed_schemas = []
    
    for provider, resource_type in sorted(all_resource_types):
        try:
            print(f"📋 Getting schema for {resource_type} ({provider.upper()})...")
            
            # Get input schema
            schema_result = get_input_schema(
                falcon, provider, resource_type, "CSPM", "IOM"
            )
            
            if schema_result:
                # Create safe filename
                safe_name = f"{provider}-{resource_type.lower().replace('::', '-').replace('_', '-')}"
                safe_name = ''.join(c for c in safe_name if c.isalnum() or c in '-.')
                filename = f"schema-{safe_name}.json"
                filepath = os.path.join(output_dir, filename)
                
                # Save schema to file
                with open(filepath, 'w') as f:
                    json.dump(schema_result, f, indent=2)
                
                successful_schemas.append({
                    'provider': provider,
                    'resource_type': resource_type,
                    'filename': filename
                })
                print(f"   ✅ Saved to: {filepath}")
            else:
                failed_schemas.append({
                    'provider': provider,
                    'resource_type': resource_type,
                    'error': 'Failed to retrieve schema'
                })
                print(f"   ❌ Failed to get schema for {resource_type}")
        
        except Exception as e:
            error_msg = str(e)
            failed_schemas.append({
                'provider': provider,
                'resource_type': resource_type,
                'error': error_msg
            })
            print(f"   ❌ Error getting schema for {resource_type}: {error_msg}")
    
    # Step 6: Generate summary
    print("\n" + "=" * 60)
    print("📊 SCHEMA GENERATION SUMMARY")
    print("=" * 60)
    
    print(f"✅ Successfully generated: {len(successful_schemas)} schema(s)")
    for schema in successful_schemas[:10]:  # Show first 10
        print(f"   • {schema['resource_type']} ({schema['provider'].upper()}) → {schema['filename']}")
    
    if len(successful_schemas) > 10:
        print(f"   ... and {len(successful_schemas) - 10} more")
    
    if failed_schemas:
        print(f"\n❌ Failed to generate: {len(failed_schemas)} schema(s)")
        for schema in failed_schemas:
            print(f"   • {schema['resource_type']} ({schema['provider'].upper()}) - {schema['error']}")
    
    # Create resource types index
    resource_types_index = {
        "total_discovered": len(all_resource_types),
        "successful_schemas": len(successful_schemas),
        "failed_schemas": len(failed_schemas),
        "resource_types": [
            {
                "provider": provider,
                "resource_type": resource_type,
                "schema_generated": any(s['provider'] == provider and s['resource_type'] == resource_type for s in successful_schemas)
            }
            for provider, resource_type in sorted(all_resource_types)
        ],
        "successful_schemas": successful_schemas,
        "failed_schemas": failed_schemas,
        "timestamp": "2025-12-03T06:11:00Z"
    }
    
    index_file = os.path.join(output_dir, "resource-types-index.json")
    with open(index_file, 'w') as f:
        json.dump(resource_types_index, f, indent=2)
    
    print(f"\n📁 All schemas saved to: {output_dir}")
    print(f"📋 Resource types index: {index_file}")
    
    if failed_schemas:
        print(f"\n⚠️  Completed with {len(failed_schemas)} failures")
    else:
        print(f"\n🎉 All {len(successful_schemas)} schemas generated successfully!")


def fetch_aws_resource_types_from_github():
    """
    Load AWS resource types from the authoritative list (fetched from AWS Config resource schema repository).
    Falls back to GitHub API if local file is not available.
    
    Returns:
        List of AWS resource types
    """
    # First try to load from the authoritative local file
    try:
        print("📋 Loading authoritative AWS resource types from local file...")
        return load_aws_resource_types_from_file("all-resource-types-aws.txt")
    except Exception as e:
        print(f"⚠️  Failed to load from local file: {str(e)}")
        print("🔍 Falling back to GitHub API...")
        
        # Fallback to GitHub API
        import urllib.request
        import urllib.parse
        
        try:
            # GitHub API URL for the resource-types directory
            api_url = "https://api.github.com/repos/awslabs/aws-config-resource-schema/contents/config/properties/resource-types"
            
            # Make request to GitHub API
            with urllib.request.urlopen(api_url) as response:
                import json
                data = json.loads(response.read().decode())
            
            # Extract resource types from filenames
            resource_types = []
            for item in data:
                if item['name'].endswith('.properties.json'):
                    # Convert filename back to resource type
                    # e.g., "AWS%3A%3AEC2%3A%3AInstance.properties.json" -> "AWS::EC2::Instance"
                    filename = item['name'].replace('.properties.json', '')
                    resource_type = urllib.parse.unquote(filename)
                    resource_types.append(resource_type)
            
            resource_types.sort()  # Sort alphabetically
            print(f"✅ Fetched {len(resource_types)} AWS resource types from GitHub API")
            return resource_types
            
        except Exception as api_error:
            print(f"❌ GitHub API also failed: {str(api_error)}")
            print("💡 Please ensure all-resource-types-aws.txt exists with the authoritative AWS resource types")
            return []


def load_aws_resource_types_from_file(filename="all-resource-types-aws.txt"):
    """
    Load AWS resource types from the AWS resource types file (fallback method).
    
    Args:
        filename: Path to the AWS resource types file
        
    Returns:
        List of AWS resource types
    """
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        # Extract resource types, filtering out comments
        resource_types = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                resource_types.append(line)
        
        print(f"📋 Loaded {len(resource_types)} AWS resource types from {filename}")
        return resource_types
        
    except FileNotFoundError:
        print(f"❌ AWS resource types file '{filename}' not found")
        return []
    except Exception as e:
        print(f"❌ Error loading AWS resource types: {str(e)}")
        return []


def load_aws_resource_types(use_github=True):
    """
    Load AWS resource types, preferring GitHub API but falling back to local file.
    
    Args:
        use_github: Whether to try fetching from GitHub first
        
    Returns:
        List of AWS resource types
    """
    if use_github:
        return fetch_aws_resource_types_from_github()
    else:
        return load_aws_resource_types_from_file()


def load_azure_resource_types_from_file(filename="all-resource-types-azure.txt", microsoft_only=True):
    """
    Load Azure resource types from the azure-resource.txt file.
    
    Args:
        filename: Path to the Azure resource types file
        microsoft_only: If True, only include Microsoft.* resource types (excludes third-party providers)
        
    Returns:
        List of Azure resource types
    """
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        # Extract resource types, filtering out operations and other non-resource entries
        resource_types = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # Skip operations, locations, and other non-resource entries
                if any(skip_pattern in line.lower() for skip_pattern in [
                    '/operations', '/locations', '/operationstatus', '/operationresults',
                    '/checknameavailability', '/usages', '/quotas', '/skus', '/capabilities',
                    '/listkeys', '/regeneratekey', '/validate', '/migrate', '/move',
                    '/export', '/import', '/backup', '/restore', '/sync', '/cancel',
                    '/restart', '/start', '/stop', '/deallocate', '/generalize',
                    '/capture', '/redeploy', '/reimage', '/performmaintenance',
                    '/assesspatches', '/installpatches', '/runcommand', '/extensions',
                    '/metricdefinitions', '/metrics', '/diagnosticsettings',
                    '/logs', '/events', '/alerts', '/recommendations', '/assessments',
                    '/securitystatuses', '/vulnerabilityassessments', '/advancedthreatprotectionsettings'
                ]):
                    continue
                
                # Only include actual resource types (those that don't end with an action)
                if '/' in line:
                    parts = line.split('/')
                    # Skip if the last part looks like an action or sub-resource operation
                    last_part = parts[-1].lower()
                    if any(action in last_part for action in [
                        'operation', 'status', 'result', 'availability', 'usage', 'quota',
                        'key', 'credential', 'token', 'secret', 'certificate', 'policy',
                        'rule', 'setting', 'configuration', 'definition', 'template',
                        'profile', 'plan', 'schedule', 'job', 'task', 'run', 'execution',
                        'deployment', 'migration', 'backup', 'restore', 'snapshot',
                        'replica', 'copy', 'sync', 'export', 'import', 'transfer',
                        'connection', 'link', 'association', 'binding', 'mapping',
                        'assignment', 'attachment', 'endpoint', 'gateway', 'proxy',
                        'filter', 'monitor', 'alert', 'notification', 'event', 'log',
                        'metric', 'diagnostic', 'health', 'status', 'state', 'info',
                        'detail', 'summary', 'report', 'analysis', 'assessment',
                        'recommendation', 'suggestion', 'advice', 'guidance', 'help'
                    ]):
                        continue
                
                # Add the resource type if it looks like a main resource
                if line.count('/') <= 2:  # Main resources typically have 1-2 slashes
                    # Apply Microsoft-only filter if requested
                    if microsoft_only and not line.startswith('Microsoft.'):
                        continue
                    resource_types.append(line)
        
        filter_note = " (Microsoft only)" if microsoft_only else ""
        print(f"📋 Loaded {len(resource_types)} Azure resource types from {filename}{filter_note}")
        return resource_types
        
    except FileNotFoundError:
        print(f"❌ Azure resource types file '{filename}' not found")
        return []
    except Exception as e:
        print(f"❌ Error loading Azure resource types: {str(e)}")
        return []


def load_gcp_resource_types_from_file(filename="all-resource-types-gcp.txt"):
    """
    Load GCP resource types from the GCP_all_resource_types.txt file.
    
    Args:
        filename: Path to the GCP resource types file
        
    Returns:
        List of GCP resource types
    """
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        # Extract resource types - GCP format is simpler, just one resource type per line
        resource_types = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # GCP resource types are in format: service.googleapis.com/ResourceType
                # or k8s.io/ResourceType, etc.
                resource_types.append(line)
        
        print(f"📋 Loaded {len(resource_types)} GCP resource types from {filename}")
        return resource_types
        
    except FileNotFoundError:
        print(f"❌ GCP resource types file '{filename}' not found")
        return []
    except Exception as e:
        print(f"❌ Error loading GCP resource types: {str(e)}")
        return []


def test_resource_type_support_command(output_dir=".", provider="aws", batch_size=10, microsoft_only=True):
    """
    Test which resource types are supported by CrowdStrike for schema generation.
    For AWS, uses known AWS Config resource types. For Azure, loads from azure-resource.txt file.
    
    Uses improved error handling and reduced retries to minimize false negatives while
    maintaining true concurrency for better performance.
    
    Args:
        output_dir: Directory to save results
        provider: Cloud provider to test (aws, azure, gcp, oci)
        batch_size: Number of concurrent requests (default: 10)
        microsoft_only: For Azure, only test Microsoft.* resource types (excludes third-party providers)
    """
    print(f"🧪 Testing Resource Type Support for {provider.upper()}")
    print("=" * 60)
    
    # Initialize Falcon API
    falcon = APIHarnessV2()
    
    # Select resource types based on provider
    if provider == "aws":
        # Load AWS resource types (try GitHub first, fallback to file)
        resource_types = load_aws_resource_types(use_github=True)
        if not resource_types:
            print("❌ No AWS resource types loaded. Please ensure all-resource-types-aws.txt exists or check internet connection.")
            sys.exit(1)
    elif provider == "azure":
        # Load Azure resource types from file (Microsoft only by default)
        resource_types = load_azure_resource_types_from_file("all-resource-types-azure.txt", microsoft_only=True)
        if not resource_types:
            print("❌ No Azure resource types loaded. Please ensure all-resource-types-azure.txt exists.")
            sys.exit(1)
        
        print(f"🔍 Testing Microsoft native resources only (excludes third-party providers)")
    elif provider == "gcp":
        # Load GCP resource types from file
        resource_types = load_gcp_resource_types_from_file("all-resource-types-gcp.txt")
        if not resource_types:
            print("❌ No GCP resource types loaded. Please ensure all-resource-types-gcp.txt exists.")
            sys.exit(1)
        
        print(f"🔍 Testing all GCP resource types from file")
    else:
        # Default to AWS if provider not recognized
        resource_types = load_aws_resource_types(use_github=True)
        if not resource_types:
            print("❌ No AWS resource types loaded as fallback. Please ensure all-resource-types-aws.txt exists or check internet connection.")
            sys.exit(1)
    
    print(f"🔍 Testing {len(resource_types)} {provider.upper()} resource types for schema support...")
    print()
    
    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created output directory: {output_dir}")
    
    # Test resource types concurrently for much better performance
    supported_types = []
    unsupported_types = []
    
    # Thread-safe lock for updating shared lists only
    results_lock = threading.Lock()
    
    def test_single_resource_type(resource_type, index):
        """Test a single resource type for schema support with retry logic and proper error handling."""
        import time
        import random
        
        max_retries = 2  # Reduced retries since we're not dealing with auth conflicts
        base_delay = 0.5  # Shorter delay
        
        for attempt in range(max_retries):
            try:
                # Add small random delay to avoid overwhelming the API
                if attempt > 0:
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
                    time.sleep(delay)
                
                # Create thread-local Falcon instance but with better error handling
                # This is actually safer than sharing a single instance across threads
                thread_falcon = APIHarnessV2()
                
                response = thread_falcon.command(
                    override="GET,/cloud-policies/combined/rules/input-schema/v1",
                    parameters={
                        "domain": "CSPM",
                        "subdomain": "IOM",
                        "cloud_provider": provider,
                        "resource_type": resource_type
                    },
                    headers={"Content-Type": "application/json"}
                )
                
                result = {
                    'resource_type': resource_type,
                    'provider': provider,
                    'index': index,
                    'response': response
                }
                
                # Check response status and body
                if response["status_code"] in [200, 201]:
                    schema_result = response["body"].get("resources", [])
                    if schema_result and len(schema_result) > 0:
                        result['supported'] = True
                        result['error'] = None
                        result['schema_result'] = schema_result
                        print(f"[{index:3d}/{len(resource_types)}] {resource_type:<40} ✅ SUPPORTED")
                        return result
                    else:
                        result['supported'] = False
                        result['error'] = 'No schema returned'
                        result['schema_result'] = None
                        print(f"[{index:3d}/{len(resource_types)}] {resource_type:<40} ❌ NOT SUPPORTED")
                        return result
                else:
                    # Check if it's the standard "resource not found" error
                    error_body = response.get("body", {})
                    errors = error_body.get("errors", [])
                    
                    is_standard_error = False
                    if errors and len(errors) > 0:
                        error_msg = errors[0].get("message", "")
                        if "resource not found or unavailable" in error_msg.lower():
                            is_standard_error = True
                    
                    if is_standard_error:
                        result['supported'] = False
                        result['error'] = 'No schema returned'
                        result['schema_result'] = None
                        print(f"[{index:3d}/{len(resource_types)}] {resource_type:<40} ❌ NOT SUPPORTED")
                    else:
                        # Highlight unexpected errors
                        result['supported'] = False
                        result['error'] = f"HTTP {response['status_code']}: {error_body}"
                        result['schema_result'] = None
                        print(f"[{index:3d}/{len(resource_types)}] {resource_type:<40} 🚨 UNEXPECTED ERROR: HTTP {response['status_code']}")
                        print(f"    Error details: {error_body}")
                    
                    return result
                
            except Exception as e:
                error_msg = str(e)
                
                # Only retry on specific transient errors, not authentication issues
                should_retry = any(keyword in error_msg.lower() for keyword in [
                    'timeout', 'connection', 'network', 'temporary', 'rate limit'
                ])
                
                if should_retry and attempt < max_retries - 1:
                    print(f"[{index:3d}/{len(resource_types)}] {resource_type:<40} 🔄 TRANSIENT ERROR (retry {attempt + 1}/{max_retries})")
                    continue
                
                # Don't retry authentication or permanent errors - fail fast
                print(f"[{index:3d}/{len(resource_types)}] {resource_type:<40} ❌ ERROR: {error_msg}")
                return {
                    'resource_type': resource_type,
                    'provider': provider,
                    'index': index,
                    'supported': False,
                    'error': f"Exception: {error_msg}",
                    'schema_result': None
                }
        
        # Should not reach here, but just in case
        return {
            'resource_type': resource_type,
            'provider': provider,
            'index': index,
            'supported': False,
            'error': 'Max retries exceeded',
            'schema_result': None
        }
    
    print(f"\n🚀 Testing {len(resource_types)} resource types concurrently (batch size: {batch_size})...")
    print(f"🔧 Using improved error handling and reduced retries for better consistency...")
    
    # Use ThreadPoolExecutor for truly concurrent API calls
    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        # Submit all tasks - each will create its own Falcon instance with better error handling
        future_to_resource = {
            executor.submit(test_single_resource_type, resource_type, i + 1): resource_type
            for i, resource_type in enumerate(resource_types)
        }
        
        # Process completed tasks as they finish
        completed_count = 0
        for future in as_completed(future_to_resource):
            result = future.result()
            completed_count += 1
            
            # Thread-safe update of results
            with results_lock:
                if result['supported']:
                    supported_types.append({
                        'resource_type': result['resource_type'],
                        'provider': result['provider'],
                        'schema_available': True
                    })
                    
                    # Save schema to file in json subdirectory
                    if result['schema_result']:
                        safe_name = result['resource_type'].lower().replace('::', '-').replace('/', '-').replace('.', '-')
                        safe_name = ''.join(c for c in safe_name if c.isalnum() or c in '-')
                        filename = f"schema-{provider}-{safe_name}.json"
                        
                        # Create json subdirectory if it doesn't exist
                        json_dir = os.path.join(output_dir, 'json')
                        if not os.path.exists(json_dir):
                            os.makedirs(json_dir)
                        
                        filepath = os.path.join(json_dir, filename)
                        
                        with open(filepath, 'w') as f:
                            json.dump(result['schema_result'], f, indent=2)
                else:
                    unsupported_types.append({
                        'resource_type': result['resource_type'],
                        'provider': result['provider'],
                        'schema_available': False,
                        'error': result['error']
                    })
            
            # Show progress every batch_size completions
            if completed_count % batch_size == 0 or completed_count == len(resource_types):
                with results_lock:
                    print(f"   📊 Progress: {completed_count}/{len(resource_types)} tested, {len(supported_types)} supported so far")
    
    # Generate summary
    print("\n" + "=" * 60)
    print("📊 RESOURCE TYPE SUPPORT SUMMARY")
    print("=" * 60)
    
    total_tested = len(resource_types)
    total_supported = len(supported_types)
    total_unsupported = len(unsupported_types)
    support_percentage = (total_supported / total_tested * 100) if total_tested > 0 else 0
    
    print(f"📊 Total tested: {total_tested}")
    print(f"✅ Supported: {total_supported} ({support_percentage:.1f}%)")
    print(f"❌ Not supported: {total_unsupported}")
    
    print(f"\n✅ SUPPORTED RESOURCE TYPES ({total_supported}):")
    for rt in supported_types:
        print(f"   • {rt['resource_type']}")
    
    if unsupported_types:
        print(f"\n❌ UNSUPPORTED RESOURCE TYPES ({total_unsupported}):")
        for rt in unsupported_types[:20]:  # Show first 20
            print(f"   • {rt['resource_type']}")
        if len(unsupported_types) > 20:
            print(f"   ... and {len(unsupported_types) - 20} more")
    
    # Save comprehensive report
    report = {
        "provider": provider,
        "total_tested": total_tested,
        "total_supported": total_supported,
        "total_unsupported": total_unsupported,
        "support_percentage": support_percentage,
        "supported_types": supported_types,
        "unsupported_types": unsupported_types,
        "timestamp": "2025-12-03T06:21:00Z"
    }
    
    report_file = os.path.join(output_dir, f"resource-type-support-report-{provider}.json")
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Generate markdown table
    print(f"\n📝 Generating markdown table...")
    if provider == "aws":
        markdown_content = generate_aws_support_markdown_table(supported_types, unsupported_types, total_tested, total_supported, support_percentage)
        markdown_file = f"resource-type-support-{provider}.md"
    elif provider == "azure":
        markdown_content = generate_azure_support_markdown_table(supported_types, unsupported_types, total_tested, total_supported, support_percentage)
        markdown_file = f"resource-type-support-{provider}.md"
    elif provider == "gcp":
        markdown_content = generate_gcp_support_markdown_table(supported_types, unsupported_types, total_tested, total_supported, support_percentage)
        markdown_file = f"resource-type-support-{provider}.md"
    else:
        markdown_content = generate_generic_support_markdown_table(provider, supported_types, unsupported_types, total_tested, total_supported, support_percentage)
        markdown_file = f"resource-type-support-{provider}.md"
    
    # Save to output directory
    markdown_filepath = os.path.join(output_dir, markdown_file)
    with open(markdown_filepath, 'w') as f:
        f.write(markdown_content)
    
    print(f"📋 Markdown table saved to: {markdown_filepath}")
    
    print(f"\n📁 Schemas saved to: {output_dir}")
    print(f"📋 Support report: {report_file}")
    print(f"\n🎉 Testing complete! {total_supported}/{total_tested} resource types are supported by CrowdStrike.")


def generate_aws_support_markdown_table(supported_types, unsupported_types, total_tested, total_supported, support_percentage):
    """
    Generate a markdown table showing AWS resource type support with links to AWS Config schema repository.
    
    Args:
        supported_types: List of supported resource types
        unsupported_types: List of unsupported resource types
        total_tested: Total number of resource types tested
        total_supported: Number of supported resource types
        support_percentage: Percentage of supported resource types
    
    Returns:
        Markdown content as string
    """
    
    def get_aws_config_link(resource_type):
        """Generate link to AWS Config resource schema repository."""
        # Convert AWS::Service::Resource to the actual file format: AWS%3A%3AService%3A%3AResource.properties.json
        import urllib.parse
        if resource_type.startswith("AWS::"):
            # URL encode the resource type (:: becomes %3A%3A)
            encoded_resource_type = urllib.parse.quote(resource_type, safe='')
            return f"https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/{encoded_resource_type}.properties.json"
        return None
    
    # Combine all resource types with their support status
    all_types = []
    
    # Add supported types
    for rt in supported_types:
        all_types.append({
            'resource_type': rt['resource_type'],
            'supported': True,
            'schema_link': get_aws_config_link(rt['resource_type'])
        })
    
    # Add unsupported types
    for rt in unsupported_types:
        all_types.append({
            'resource_type': rt['resource_type'],
            'supported': False,
            'schema_link': get_aws_config_link(rt['resource_type'])
        })
    
    # Sort by resource type
    all_types.sort(key=lambda x: x['resource_type'])
    
    # Get current timestamp
    from datetime import datetime
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Generate markdown content
    markdown = f"""# AWS Resource Type Support in CrowdStrike

This table shows which AWS Config resource types are supported by CrowdStrike for custom IOM rules.

## Summary

- **Total Tested**: {total_tested} resource types
- **Supported**: {total_supported} ({support_percentage:.1f}%)
- **Not Supported**: {total_tested - total_supported} ({100 - support_percentage:.1f}%)
- **Last Updated**: {timestamp}

## Resource Type Support Table

| Resource Type | CrowdStrike Support | AWS Config Schema |
|---------------|-------------------|------------------|
"""
    
    for rt in all_types:
        support_icon = "✅ Yes" if rt['supported'] else "❌ No"
        resource_type = rt['resource_type']
        
        if rt['schema_link']:
            schema_link = f"[View Schema]({rt['schema_link']})"
        else:
            schema_link = "N/A"
        
        markdown += f"| `{resource_type}` | {support_icon} | {schema_link} |\n"
    
    markdown += f"""
## Usage

### Supported Resource Types
For supported resource types, you can:
1. Generate schemas: `python rule-manager.py schema --config your-rule.yaml`
2. Create custom rules using the resource type in your YAML configuration
3. Test rules against real resources: `python rule-manager.py test --config your-rule.yaml`

### Example Rule Configuration
```yaml
rule:
  name: "My-Custom-Rule"
  description: "Custom rule for supported resource type"
  resource_type: "AWS::EC2::Instance"  # Must be from supported list
  platform: "AWS"
  provider: "AWS"
  severity: 1
  logic: |
    package crowdstrike
    default result = "fail"
    result = "pass" if {{
        # Your Rego logic here
    }}
```

### Regenerate This Table
```bash
python get_schemas.py test-support --provider aws
```

---
*Generated by CrowdStrike Custom IOM Rules Toolkit*
"""
    
    return markdown


def generate_azure_support_markdown_table(supported_types, unsupported_types, total_tested, total_supported, support_percentage):
    """
    Generate a markdown table showing Azure resource type support with links to Azure documentation.
    
    Args:
        supported_types: List of supported resource types
        unsupported_types: List of unsupported resource types
        total_tested: Total number of resource types tested
        total_supported: Number of supported resource types
        support_percentage: Percentage of supported resource types
    
    Returns:
        Markdown content as string
    """
    
    def get_azure_docs_link(resource_type):
        """Generate link to Azure resource documentation."""
        # Convert Microsoft.Service/resourceType to documentation format
        if '/' in resource_type:
            parts = resource_type.split('/')
            if len(parts) >= 2:
                service = parts[0].lower().replace('microsoft.', '')
                resource = parts[1].lower()
                # Generate Azure docs link (corrected pattern)
                return f"https://learn.microsoft.com/en-us/azure/templates/{service}/{resource}"
        return None
    
    # Combine all resource types with their support status
    all_types = []
    
    # Add supported types
    for rt in supported_types:
        all_types.append({
            'resource_type': rt['resource_type'],
            'supported': True,
            'docs_link': get_azure_docs_link(rt['resource_type'])
        })
    
    # Add unsupported types
    for rt in unsupported_types:
        all_types.append({
            'resource_type': rt['resource_type'],
            'supported': False,
            'docs_link': get_azure_docs_link(rt['resource_type'])
        })
    
    # Sort by resource type
    all_types.sort(key=lambda x: x['resource_type'])
    
    # Get current timestamp
    from datetime import datetime
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Generate markdown content
    markdown = f"""# Azure Resource Type Support in CrowdStrike

This table shows which Azure resource types are supported by CrowdStrike for custom IOM rules.

## Summary

- **Total Tested**: {total_tested} resource types
- **Supported**: {total_supported} ({support_percentage:.1f}%)
- **Not Supported**: {total_tested - total_supported} ({100 - support_percentage:.1f}%)
- **Last Updated**: {timestamp}

## Resource Type Support Table

| Resource Type | CrowdStrike Support |
|---------------|-------------------|
"""
    
    for rt in all_types:
        support_icon = "✅ Yes" if rt['supported'] else "❌ No"
        resource_type = rt['resource_type']
        
        markdown += f"| `{resource_type}` | {support_icon} |\n"
    
    markdown += f"""

## Usage

### Supported Resource Types
For supported resource types, you can:
1. Generate schemas: `python rule-manager.py schema --config your-rule.yaml`
2. Create custom rules using the resource type in your YAML configuration
3. Test rules against real resources: `python rule-manager.py test --config your-rule.yaml`

### Example Rule Configuration
```yaml
rule:
  name: "My-Azure-Custom-Rule"
  description: "Custom rule for supported Azure resource type"
  resource_type: "Microsoft.Compute/virtualMachines"  # Must be from supported list
  platform: "Azure"
  provider: "Azure"
  severity: 1
  logic: |
    package crowdstrike
    default result = "fail"
    result = "pass" if {{
        # Your Rego logic here
    }}
```

### Regenerate This Table
```bash
python get_schemas.py test-support --provider azure
```

---
*Generated by CrowdStrike Custom IOM Rules Toolkit*
"""
    
    return markdown


def generate_gcp_support_markdown_table(supported_types, unsupported_types, total_tested, total_supported, support_percentage):
    """
    Generate a markdown table showing GCP resource type support with links to GCP documentation.
    
    Args:
        supported_types: List of supported resource types
        unsupported_types: List of unsupported resource types
        total_tested: Total number of resource types tested
        total_supported: Number of supported resource types
        support_percentage: Percentage of supported resource types
    
    Returns:
        Markdown content as string
    """
    
    def get_gcp_docs_link(resource_type):
        """Generate link to GCP resource documentation."""
        # Convert service.googleapis.com/ResourceType to documentation format
        if '.googleapis.com/' in resource_type:
            parts = resource_type.split('.googleapis.com/')
            if len(parts) == 2:
                service = parts[0]
                # Generate GCP docs link (corrected pattern)
                return f"https://cloud.google.com/{service}"
        elif resource_type.startswith('k8s.io/'):
            # Kubernetes resources
            return "https://kubernetes.io/docs/reference/kubernetes-api/"
        return None
    
    # Combine all resource types with their support status
    all_types = []
    
    # Add supported types
    for rt in supported_types:
        all_types.append({
            'resource_type': rt['resource_type'],
            'supported': True,
            'docs_link': get_gcp_docs_link(rt['resource_type'])
        })
    
    # Add unsupported types
    for rt in unsupported_types:
        all_types.append({
            'resource_type': rt['resource_type'],
            'supported': False,
            'docs_link': get_gcp_docs_link(rt['resource_type'])
        })
    
    # Sort by resource type
    all_types.sort(key=lambda x: x['resource_type'])
    
    # Get current timestamp
    from datetime import datetime
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Generate markdown content
    markdown = f"""# GCP Resource Type Support in CrowdStrike

This table shows which GCP resource types are supported by CrowdStrike for custom IOM rules.

## Summary

- **Total Tested**: {total_tested} resource types
- **Supported**: {total_supported} ({support_percentage:.1f}%)
- **Not Supported**: {total_tested - total_supported} ({100 - support_percentage:.1f}%)
- **Last Updated**: {timestamp}

## Resource Type Support Table

| Resource Type | CrowdStrike Support |
|---------------|-------------------|
"""
    
    for rt in all_types:
        support_icon = "✅ Yes" if rt['supported'] else "❌ No"
        resource_type = rt['resource_type']
        
        markdown += f"| `{resource_type}` | {support_icon} |\n"
    
    markdown += f"""

## Usage

### Supported Resource Types
For supported resource types, you can:
1. Generate schemas: `python rule-manager.py schema --config your-rule.yaml`
2. Create custom rules using the resource type in your YAML configuration
3. Test rules against real resources: `python rule-manager.py test --config your-rule.yaml`

### Example Rule Configuration
```yaml
rule:
  name: "My-GCP-Custom-Rule"
  description: "Custom rule for supported GCP resource type"
  resource_type: "compute.googleapis.com/Instance"  # Must be from supported list
  platform: "GCP"
  provider: "GCP"
  severity: 1
  logic: |
    package crowdstrike
    default result = "fail"
    result = "pass" if {{
        # Your Rego logic here
    }}
```

### Regenerate This Table
```bash
python get_schemas.py test-support --provider gcp
```

---
*Generated by CrowdStrike Custom IOM Rules Toolkit*
"""
    
    return markdown


def generate_generic_support_markdown_table(provider, supported_types, unsupported_types, total_tested, total_supported, support_percentage):
    """
    Generate a generic markdown table showing resource type support for any provider.
    
    Args:
        provider: Cloud provider name
        supported_types: List of supported resource types
        unsupported_types: List of unsupported resource types
        total_tested: Total number of resource types tested
        total_supported: Number of supported resource types
        support_percentage: Percentage of supported resource types
    
    Returns:
        Markdown content as string
    """
    
    # Combine all resource types with their support status
    all_types = []
    
    # Add supported types
    for rt in supported_types:
        all_types.append({
            'resource_type': rt['resource_type'],
            'supported': True
        })
    
    # Add unsupported types
    for rt in unsupported_types:
        all_types.append({
            'resource_type': rt['resource_type'],
            'supported': False
        })
    
    # Sort by resource type
    all_types.sort(key=lambda x: x['resource_type'])
    
    # Get current timestamp
    from datetime import datetime
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Generate markdown content
    markdown = f"""# {provider.upper()} Resource Type Support in CrowdStrike

This table shows which {provider.upper()} resource types are supported by CrowdStrike for custom IOM rules.

## Summary

- **Total Tested**: {total_tested} resource types
- **Supported**: {total_supported} ({support_percentage:.1f}%)
- **Not Supported**: {total_tested - total_supported} ({100 - support_percentage:.1f}%)
- **Last Updated**: {timestamp}

## Resource Type Support Table

| Resource Type | CrowdStrike Support |
|---------------|-------------------|
"""
    
    for rt in all_types:
        support_icon = "✅ Yes" if rt['supported'] else "❌ No"
        resource_type = rt['resource_type']
        
        markdown += f"| `{resource_type}` | {support_icon} |\n"
    
    markdown += f"""

## Usage

### Supported Resource Types
For supported resource types, you can:
1. Generate schemas: `python rule-manager.py schema --config your-rule.yaml`
2. Create custom rules using the resource type in your YAML configuration
3. Test rules against real resources: `python rule-manager.py test --config your-rule.yaml`

### Example Rule Configuration
```yaml
rule:
  name: "My-{provider.title()}-Custom-Rule"
  description: "Custom rule for supported {provider.upper()} resource type"
  resource_type: "YourResourceType"  # Must be from supported list
  platform: "{provider.title()}"
  provider: "{provider.title()}"
  severity: 1
  logic: |
    package crowdstrike
    default result = "fail"
    result = "pass" if {{
        # Your Rego logic here
    }}
```

### Regenerate This Table
```bash
python get_schemas.py test-support --provider {provider}
```

---
*Generated by CrowdStrike Custom IOM Rules Toolkit*
"""
    
    return markdown




def main():
    """Main function to parse arguments and execute schema commands."""
    parser = argparse.ArgumentParser(
        description="CrowdStrike Schema Manager - Standalone Schema Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all schemas from existing rules
  python3 get_schemas.py generate-all --output-dir schemas --limit 1000

  # Test resource type support for AWS
  python3 get_schemas.py test-support --provider aws --output-dir schemas

  # Test resource type support for Azure
  python3 get_schemas.py test-support --provider azure --output-dir schemas

  # Test resource type support for GCP
  python3 get_schemas.py test-support --provider gcp --output-dir schemas

  # Get schema for specific resource type
  python3 get_schemas.py get-schema --provider aws --resource-type "AWS::EC2::Instance"

  # Validate existing schemas
  python3 get_schemas.py validate-schemas --schemas-dir schemas

  # Compare schemas between versions
  python3 get_schemas.py compare-schemas --old-dir old-schemas --new-dir new-schemas

  # Generate schema documentation
  python3 get_schemas.py generate-docs --schemas-dir schemas --output-dir docs
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Generate all schemas command
    parser_generate_all = subparsers.add_parser("generate-all", help="Generate schemas for all resource types")
    parser_generate_all.add_argument("--output-dir", default=".", help="Directory to save schema files (default: .)")
    parser_generate_all.add_argument("--limit", type=int, default=1000, help="Maximum number of rules to scan (default: 1000)")
    
    # Test resource type support command
    parser_test_support = subparsers.add_parser("test-support", help="Test which resource types are supported")
    parser_test_support.add_argument("--provider", required=True, choices=["aws", "azure", "gcp", "oci"], 
                                   help="Cloud provider to test")
    parser_test_support.add_argument("--output-dir", default=".",
                                   help="Directory to save results (default: .)")
    parser_test_support.add_argument("--batch-size", type=int, default=10, 
                                   help="Number of concurrent requests (default: 10)")
    parser_test_support.add_argument("--microsoft-only", action="store_true", 
                                   help="For Azure, only test Microsoft.* resources")
    
    # Get single schema command
    parser_get_schema = subparsers.add_parser("get-schema", help="Get schema for specific resource type")
    parser_get_schema.add_argument("--provider", required=True, choices=["aws", "azure", "gcp", "oci"],
                                 help="Cloud provider")
    parser_get_schema.add_argument("--resource-type", required=True, help="Resource type to get schema for")
    parser_get_schema.add_argument("--output-file", help="Output file path (optional)")
    
    # Validate schemas command
    parser_validate = subparsers.add_parser("validate-schemas", help="Validate existing schema files")
    parser_validate.add_argument("--schemas-dir", default=".", help="Directory containing schema files")
    
    # Compare schemas command
    parser_compare = subparsers.add_parser("compare-schemas", help="Compare schemas between two directories")
    parser_compare.add_argument("--old-dir", required=True, help="Directory with old schemas")
    parser_compare.add_argument("--new-dir", required=True, help="Directory with new schemas")
    parser_compare.add_argument("--output-file", default="schema-comparison.json", help="Output comparison file")
    
    # Generate documentation command
    parser_docs = subparsers.add_parser("generate-docs", help="Generate documentation from schemas")
    parser_docs.add_argument("--schemas-dir", default=".", help="Directory containing schema files")
    parser_docs.add_argument("--output-dir", default="docs", help="Directory to save documentation")
    parser_docs.add_argument("--format", choices=["markdown", "html", "json"], default="markdown",
                           help="Documentation format")
    
    # List schemas command
    parser_list = subparsers.add_parser("list-schemas", help="List available schema files")
    parser_list.add_argument("--schemas-dir", default=".", help="Directory containing schema files")
    parser_list.add_argument("--provider", choices=["aws", "azure", "gcp", "oci"], help="Filter by provider")
    
    # Cache management commands
    parser_cache = subparsers.add_parser("cache", help="Manage schema cache")
    cache_subparsers = parser_cache.add_subparsers(dest="cache_command", help="Cache operations")
    
    parser_cache_clear = cache_subparsers.add_parser("clear", help="Clear schema cache")
    parser_cache_status = cache_subparsers.add_parser("status", help="Show cache status")
    parser_cache_update = cache_subparsers.add_parser("update", help="Update cache incrementally")
    
    args = parser.parse_args()
    
    # Show help if no command provided
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Execute command
    try:
        if args.command == "generate-all":
            generate_all_schemas_command(args.output_dir, args.limit)
        
        elif args.command == "test-support":
            test_resource_type_support_command(args.output_dir, args.provider, args.batch_size, 
                                             getattr(args, 'microsoft_only', True))
        
        elif args.command == "get-schema":
            get_single_schema_command(args.provider, args.resource_type, args.output_file)
        
        elif args.command == "validate-schemas":
            validate_schemas_command(args.schemas_dir)
        
        elif args.command == "compare-schemas":
            compare_schemas_command(args.old_dir, args.new_dir, args.output_file)
        
        elif args.command == "generate-docs":
            generate_documentation_command(args.schemas_dir, args.output_dir, args.format)
        
        elif args.command == "list-schemas":
            list_schemas_command(args.schemas_dir, getattr(args, 'provider', None))
        
        elif args.command == "cache":
            if args.cache_command == "clear":
                clear_cache_command()
            elif args.cache_command == "status":
                cache_status_command()
            elif args.cache_command == "update":
                update_cache_command()
            else:
                parser_cache.print_help()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error executing command: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def get_single_schema_command(provider, resource_type, output_file=None):
    """
    Get schema for a single resource type.
    
    Args:
        provider: Cloud provider (aws, azure, gcp, oci)
        resource_type: Resource type to get schema for
        output_file: Optional output file path
    """
    print(f"📋 Getting Schema for {resource_type} ({provider.upper()})")
    print("=" * 60)
    
    # Initialize Falcon API
    falcon = APIHarnessV2()
    
    print(f"🔍 Requesting schema from CrowdStrike API...")
    
    # Get input schema
    schema_result = get_input_schema(falcon, provider, resource_type, "CSPM", "IOM")
    
    if schema_result:
        print("✅ Schema retrieved successfully!")
        
        # Determine output file
        if not output_file:
            safe_name = f"{provider}-{resource_type.lower().replace('::', '-').replace('/', '-').replace('.', '-')}"
            safe_name = ''.join(c for c in safe_name if c.isalnum() or c in '-.')
            output_file = f"schema-{safe_name}.json"
        
        # Save schema to file
        with open(output_file, 'w') as f:
            json.dump(schema_result, f, indent=2)
        
        print(f"💾 Schema saved to: {output_file}")
        
        # Display schema summary
        if schema_result and len(schema_result) > 0:
            schema_data = schema_result[0]
            if isinstance(schema_data, dict):
                resource_key = list(schema_data.keys())[0]
                config = schema_data[resource_key].get('configuration', {})
                print(f"\n📊 Schema Summary:")
                print(f"   Resource Type: {resource_type}")
                print(f"   Configuration Fields: {len(config)}")
                print(f"   File Size: {os.path.getsize(output_file)} bytes")
    else:
        print("❌ Failed to retrieve schema")
        print("💡 This resource type may not be supported by CrowdStrike")
        sys.exit(1)


def validate_schemas_command(schemas_dir):
    """
    Validate existing schema files.
    
    Args:
        schemas_dir: Directory containing schema files
    """
    print(f"✅ Validating Schema Files in {schemas_dir}")
    print("=" * 60)
    
    if not os.path.exists(schemas_dir):
        print(f"❌ Schemas directory '{schemas_dir}' not found")
        sys.exit(1)
    
    # Find all JSON schema files
    schema_files = []
    for file in os.listdir(schemas_dir):
        if file.endswith('.json') and file.startswith('schema-'):
            schema_files.append(os.path.join(schemas_dir, file))
    
    if not schema_files:
        print(f"❌ No schema files found in '{schemas_dir}'")
        sys.exit(1)
    
    print(f"📋 Found {len(schema_files)} schema files to validate")
    
    valid_schemas = []
    invalid_schemas = []
    
    for schema_file in schema_files:
        print(f"\n🔍 Validating: {os.path.basename(schema_file)}")
        
        try:
            with open(schema_file, 'r') as f:
                schema_data = json.load(f)
            
            # Basic validation
            if not isinstance(schema_data, list):
                invalid_schemas.append({"file": schema_file, "error": "Schema must be a list"})
                print("   ❌ Invalid: Schema must be a list")
                continue
            
            if len(schema_data) == 0:
                invalid_schemas.append({"file": schema_file, "error": "Schema list is empty"})
                print("   ❌ Invalid: Schema list is empty")
                continue
            
            # Check first item structure
            first_item = schema_data[0]
            if not isinstance(first_item, dict):
                invalid_schemas.append({"file": schema_file, "error": "Schema items must be dictionaries"})
                print("   ❌ Invalid: Schema items must be dictionaries")
                continue
            
            # Check for resource type key
            resource_keys = list(first_item.keys())
            if len(resource_keys) == 0:
                invalid_schemas.append({"file": schema_file, "error": "No resource type found"})
                print("   ❌ Invalid: No resource type found")
                continue
            
            resource_type = resource_keys[0]
            resource_data = first_item[resource_type]
            
            # Check required fields
            required_fields = ['configuration', 'relationships', 'resourceId', 'resourceName']
            missing_fields = [field for field in required_fields if field not in resource_data]
            
            if missing_fields:
                invalid_schemas.append({"file": schema_file, "error": f"Missing fields: {missing_fields}"})
                print(f"   ❌ Invalid: Missing fields: {missing_fields}")
                continue
            
            # Schema is valid
            config_fields = len(resource_data.get('configuration', {}))
            valid_schemas.append({
                "file": schema_file,
                "resource_type": resource_type,
                "config_fields": config_fields,
                "file_size": os.path.getsize(schema_file)
            })
            print(f"   ✅ Valid: {resource_type} ({config_fields} config fields)")
            
        except json.JSONDecodeError as e:
            invalid_schemas.append({"file": schema_file, "error": f"JSON decode error: {str(e)}"})
            print(f"   ❌ Invalid: JSON decode error: {str(e)}")
        except Exception as e:
            invalid_schemas.append({"file": schema_file, "error": f"Validation error: {str(e)}"})
            print(f"   ❌ Invalid: Validation error: {str(e)}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)
    
    print(f"✅ Valid schemas: {len(valid_schemas)}")
    for schema in valid_schemas:
        print(f"   • {schema['resource_type']} - {schema['config_fields']} fields ({schema['file_size']} bytes)")
    
    if invalid_schemas:
        print(f"\n❌ Invalid schemas: {len(invalid_schemas)}")
        for schema in invalid_schemas:
            print(f"   • {os.path.basename(schema['file'])} - {schema['error']}")
    
    # Save validation report
    report = {
        "total_files": len(schema_files),
        "valid": len(valid_schemas),
        "invalid": len(invalid_schemas),
        "valid_schemas": valid_schemas,
        "invalid_schemas": invalid_schemas,
        "timestamp": "2025-12-03T13:55:00Z"
    }
    
    report_file = os.path.join(schemas_dir, "validation-report.json")
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📋 Validation report saved to: {report_file}")
    
    if invalid_schemas:
        print(f"\n⚠️  Validation completed with {len(invalid_schemas)} failures")
        sys.exit(1)
    else:
        print(f"\n🎉 All {len(valid_schemas)} schemas are valid!")


def compare_schemas_command(old_dir, new_dir, output_file):
    """
    Compare schemas between two directories.
    
    Args:
        old_dir: Directory with old schemas
        new_dir: Directory with new schemas
        output_file: Output comparison file
    """
    print(f"🔍 Comparing Schemas: {old_dir} vs {new_dir}")
    print("=" * 60)
    
    if not os.path.exists(old_dir):
        print(f"❌ Old schemas directory '{old_dir}' not found")
        sys.exit(1)
    
    if not os.path.exists(new_dir):
        print(f"❌ New schemas directory '{new_dir}' not found")
        sys.exit(1)
    
    # Load schemas from both directories
    def load_schemas_from_dir(directory):
        schemas = {}
        for file in os.listdir(directory):
            if file.endswith('.json') and file.startswith('schema-'):
                filepath = os.path.join(directory, file)
                try:
                    with open(filepath, 'r') as f:
                        schema_data = json.load(f)
                    schemas[file] = schema_data
                except Exception as e:
                    print(f"⚠️  Error loading {file}: {str(e)}")
        return schemas
    
    old_schemas = load_schemas_from_dir(old_dir)
    new_schemas = load_schemas_from_dir(new_dir)
    
    print(f"📋 Loaded {len(old_schemas)} old schemas and {len(new_schemas)} new schemas")
    
    # Compare schemas
    comparison = {
        "added": [],
        "removed": [],
        "modified": [],
        "unchanged": [],
        "summary": {
            "old_count": len(old_schemas),
            "new_count": len(new_schemas),
            "added_count": 0,
            "removed_count": 0,
            "modified_count": 0,
            "unchanged_count": 0
        }
    }
    
    # Find added, removed, and modified schemas
    all_files = set(old_schemas.keys()) | set(new_schemas.keys())
    
    for file in all_files:
        if file in old_schemas and file in new_schemas:
            # Compare content
            if json.dumps(old_schemas[file], sort_keys=True) == json.dumps(new_schemas[file], sort_keys=True):
                comparison["unchanged"].append(file)
            else:
                comparison["modified"].append({
                    "file": file,
                    "old_size": len(json.dumps(old_schemas[file])),
                    "new_size": len(json.dumps(new_schemas[file]))
                })
        elif file in new_schemas:
            comparison["added"].append(file)
        else:
            comparison["removed"].append(file)
    
    # Update summary counts
    comparison["summary"]["added_count"] = len(comparison["added"])
    comparison["summary"]["removed_count"] = len(comparison["removed"])
    comparison["summary"]["modified_count"] = len(comparison["modified"])
    comparison["summary"]["unchanged_count"] = len(comparison["unchanged"])
    
    # Save comparison report
    with open(output_file, 'w') as f:
        json.dump(comparison, f, indent=2)
    
    # Display summary
    print(f"\n📊 Comparison Summary:")
    print(f"   ➕ Added: {comparison['summary']['added_count']} schemas")
    print(f"   ➖ Removed: {comparison['summary']['removed_count']} schemas")
    print(f"   🔄 Modified: {comparison['summary']['modified_count']} schemas")
    print(f"   ✅ Unchanged: {comparison['summary']['unchanged_count']} schemas")
    
    if comparison["added"]:
        print(f"\n➕ Added schemas:")
        for file in comparison["added"]:
            print(f"   • {file}")
    
    if comparison["removed"]:
        print(f"\n➖ Removed schemas:")
        for file in comparison["removed"]:
            print(f"   • {file}")
    
    if comparison["modified"]:
        print(f"\n🔄 Modified schemas:")
        for item in comparison["modified"]:
            print(f"   • {item['file']} ({item['old_size']} → {item['new_size']} bytes)")
    
    print(f"\n💾 Comparison report saved to: {output_file}")


def generate_documentation_command(schemas_dir, output_dir, format_type):
    """
    Generate documentation from schema files.
    
    Args:
        schemas_dir: Directory containing schema files
        output_dir: Directory to save documentation
        format_type: Documentation format (markdown, html, json)
    """
    print(f"📚 Generating {format_type.upper()} Documentation")
    print("=" * 60)
    
    if not os.path.exists(schemas_dir):
        print(f"❌ Schemas directory '{schemas_dir}' not found")
        sys.exit(1)
    
    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created output directory: {output_dir}")
    
    # Load all schemas
    schemas = {}
    for file in os.listdir(schemas_dir):
        if file.endswith('.json') and file.startswith('schema-'):
            filepath = os.path.join(schemas_dir, file)
            try:
                with open(filepath, 'r') as f:
                    schema_data = json.load(f)
                schemas[file] = schema_data
            except Exception as e:
                print(f"⚠️  Error loading {file}: {str(e)}")
    
    print(f"📋 Loaded {len(schemas)} schemas for documentation")
    
    if format_type == "markdown":
        generate_markdown_docs(schemas, output_dir)
    elif format_type == "html":
        generate_html_docs(schemas, output_dir)
    elif format_type == "json":
        generate_json_docs(schemas, output_dir)
    
    print(f"✅ Documentation generated in {output_dir}")


def generate_markdown_docs(schemas, output_dir):
    """Generate markdown documentation from schemas."""
    
    # Generate index file
    index_content = """# CrowdStrike Resource Schemas Documentation

This documentation contains schemas for CrowdStrike supported resource types.

## Available Resource Types

"""
    
    resource_list = []
    
    for filename, schema_data in schemas.items():
        if schema_data and len(schema_data) > 0:
            first_item = schema_data[0]
            if isinstance(first_item, dict):
                resource_type = list(first_item.keys())[0]
                config_fields = len(first_item[resource_type].get('configuration', {}))
                
                # Extract provider from filename
                provider = "Unknown"
                if "aws" in filename.lower():
                    provider = "AWS"
                elif "azure" in filename.lower():
                    provider = "Azure"
                elif "gcp" in filename.lower():
                    provider = "GCP"
                elif "oci" in filename.lower():
                    provider = "OCI"
                
                resource_list.append({
                    'resource_type': resource_type,
                    'provider': provider,
                    'config_fields': config_fields,
                    'filename': filename.replace('.json', '.md')
                })
                
                # Generate individual resource documentation
                doc_content = f"""# {resource_type}

**Provider:** {provider}
**Configuration Fields:** {config_fields}

## Schema Structure

```json
{json.dumps(first_item, indent=2)}
```

## Configuration Fields

"""
                
                config = first_item[resource_type].get('configuration', {})
                for field_name, field_type in config.items():
                    doc_content += f"- **{field_name}**: `{field_type}`\n"
                
                doc_content += f"""
## Usage Example

```rego
package crowdstrike

default result = "fail"

result = "pass" if {{
    # Access configuration fields like:
    # input.{resource_type.replace('::', '_').replace('.', '_').lower()}.configuration.{list(config.keys())[0] if config else 'field_name'}
    
    # Your rule logic here
}}
```

---
*Generated by CrowdStrike Schema Manager*
"""
                
                # Save individual resource doc
                doc_filename = filename.replace('.json', '.md')
                doc_filepath = os.path.join(output_dir, doc_filename)
                with open(doc_filepath, 'w') as f:
                    f.write(doc_content)
    
    # Sort resource list by provider and resource type
    resource_list.sort(key=lambda x: (x['provider'], x['resource_type']))
    
    # Add to index
    current_provider = None
    for resource in resource_list:
        if resource['provider'] != current_provider:
            current_provider = resource['provider']
            index_content += f"\n### {current_provider}\n\n"
        
        index_content += f"- [{resource['resource_type']}]({resource['filename']}) ({resource['config_fields']} fields)\n"
    
    index_content += f"""

## Summary

- **Total Resource Types:** {len(resource_list)}
- **Providers:** {len(set(r['provider'] for r in resource_list))}

---
*Generated by CrowdStrike Schema Manager*
"""
    
    # Save index file
    index_filepath = os.path.join(output_dir, "README.md")
    with open(index_filepath, 'w') as f:
        f.write(index_content)
    
    print(f"📄 Generated {len(resource_list)} markdown files + index")


def generate_html_docs(schemas, output_dir):
    """Generate HTML documentation from schemas."""
    print("🚧 HTML documentation generation not yet implemented")
    print("💡 Use markdown format for now: --format markdown")


def generate_json_docs(schemas, output_dir):
    """Generate JSON documentation from schemas."""
    
    documentation = {
        "title": "CrowdStrike Resource Schemas Documentation",
        "generated_at": "2025-12-03T13:55:00Z",
        "total_schemas": len(schemas),
        "resources": []
    }
    
    for filename, schema_data in schemas.items():
        if schema_data and len(schema_data) > 0:
            first_item = schema_data[0]
            if isinstance(first_item, dict):
                resource_type = list(first_item.keys())[0]
                config = first_item[resource_type].get('configuration', {})
                
                # Extract provider from filename
                provider = "Unknown"
                if "aws" in filename.lower():
                    provider = "AWS"
                elif "azure" in filename.lower():
                    provider = "Azure"
                elif "gcp" in filename.lower():
                    provider = "GCP"
                elif "oci" in filename.lower():
                    provider = "OCI"
                
                documentation["resources"].append({
                    "resource_type": resource_type,
                    "provider": provider,
                    "filename": filename,
                    "config_fields_count": len(config),
                    "config_fields": config,
                    "full_schema": first_item
                })
    
    # Save documentation
    doc_filepath = os.path.join(output_dir, "schemas-documentation.json")
    with open(doc_filepath, 'w') as f:
        json.dump(documentation, f, indent=2)
    
    print(f"📄 Generated JSON documentation: {doc_filepath}")


def list_schemas_command(schemas_dir, provider_filter=None):
    """
    List available schema files.
    
    Args:
        schemas_dir: Directory containing schema files
        provider_filter: Optional provider filter
    """
    print(f"📋 Listing Schema Files in {schemas_dir}")
    if provider_filter:
        print(f"🔍 Filter: {provider_filter.upper()} only")
    print("=" * 60)
    
    if not os.path.exists(schemas_dir):
        print(f"❌ Schemas directory '{schemas_dir}' not found")
        sys.exit(1)
    
    # Find schema files
    schema_files = []
    for file in os.listdir(schemas_dir):
        if file.endswith('.json') and file.startswith('schema-'):
            # Apply provider filter if specified
            if provider_filter and provider_filter.lower() not in file.lower():
                continue
            
            filepath = os.path.join(schemas_dir, file)
            try:
                with open(filepath, 'r') as f:
                    schema_data = json.load(f)
                
                if schema_data and len(schema_data) > 0:
                    first_item = schema_data[0]
                    if isinstance(first_item, dict):
                        resource_type = list(first_item.keys())[0]
                        config_fields = len(first_item[resource_type].get('configuration', {}))
                        file_size = os.path.getsize(filepath)
                        
                        # Extract provider from filename
                        provider = "Unknown"
                        if "aws" in file.lower():
                            provider = "AWS"
                        elif "azure" in file.lower():
                            provider = "Azure"
                        elif "gcp" in file.lower():
                            provider = "GCP"
                        elif "oci" in file.lower():
                            provider = "OCI"
                        
                        schema_files.append({
                            'filename': file,
                            'resource_type': resource_type,
                            'provider': provider,
                            'config_fields': config_fields,
                            'file_size': file_size
                        })
            except Exception as e:
                print(f"⚠️  Error reading {file}: {str(e)}")
    
    if not schema_files:
        filter_msg = f" for {provider_filter.upper()}" if provider_filter else ""
        print(f"❌ No schema files found{filter_msg}")
        return
    
    # Sort by provider and resource type
    schema_files.sort(key=lambda x: (x['provider'], x['resource_type']))
    
    # Display schemas grouped by provider
    current_provider = None
    total_files = 0
    total_size = 0
    
    for schema in schema_files:
        if schema['provider'] != current_provider:
            if current_provider is not None:
                print()  # Add spacing between providers
            current_provider = schema['provider']
            print(f"\n📁 {current_provider} Schemas:")
        
        size_kb = schema['file_size'] / 1024
        print(f"   • {schema['resource_type']:<50} ({schema['config_fields']:3d} fields, {size_kb:6.1f} KB)")
        total_files += 1
        total_size += schema['file_size']
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"   Total schemas: {total_files}")
    print(f"   Total size: {total_size / 1024:.1f} KB")
    print(f"   Providers: {len(set(s['provider'] for s in schema_files))}")


def clear_cache_command():
    """Clear schema cache."""
    print("🗑️  Clearing Schema Cache")
    print("=" * 60)
    
    cache_dir = ".schema_cache"
    if os.path.exists(cache_dir):
        import shutil
        shutil.rmtree(cache_dir)
        print("✅ Cache cleared successfully")
    else:
        print("📋 No cache found to clear")


def cache_status_command():
    """Show cache status."""
    print("📊 Schema Cache Status")
    print("=" * 60)
    
    cache_dir = ".schema_cache"
    if os.path.exists(cache_dir):
        cache_files = [f for f in os.listdir(cache_dir) if f.endswith('.json')]
        total_size = sum(os.path.getsize(os.path.join(cache_dir, f)) for f in cache_files)
        print(f"📁 Cache directory: {cache_dir}")
        print(f"📄 Cached schemas: {len(cache_files)}")
        print(f"💾 Total size: {total_size / 1024:.1f} KB")
    else:
        print("📋 No cache directory found")


def update_cache_command():
    """Update cache incrementally."""
    print("🔄 Updating Schema Cache")
    print("=" * 60)
    print("🚧 Incremental cache updates not yet implemented")
    print("💡 Use 'generate-all' command to refresh all schemas")


if __name__ == "__main__":
    main()
