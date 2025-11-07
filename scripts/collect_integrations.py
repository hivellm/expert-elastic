#!/usr/bin/env python3
"""
Elastic Integrations Collector

Fetches integration packages from Elastic Package Registry.
Extracts field definitions and ingest pipelines.

Source: https://epr.elastic.co
Output: ~10-15k examples (mappings + pipelines)
"""

import json
import requests
import yaml
from pathlib import Path
from typing import Dict, List, Any
import random
import time

OUTPUT_DIR = Path("../datasets/raw/integrations")
EPR_SEARCH_URL = "https://epr.elastic.co/search"
EPR_PACKAGE_URL = "https://epr.elastic.co/package"


def search_packages(category: str = None, limit: int = 100) -> List[Dict[str, Any]]:
    """Search for integration packages"""
    print(f"Searching packages (category={category}, limit={limit})...")
    
    params = {
        "prerelease": "false",
        "all": "true"
    }
    
    if category:
        params["category"] = category
    
    response = requests.get(EPR_SEARCH_URL, params=params, timeout=30)
    response.raise_for_status()
    
    packages = response.json()
    
    # Limit results
    if limit and len(packages) > limit:
        packages = packages[:limit]
    
    print(f"Found {len(packages)} packages")
    return packages


def fetch_package_manifest(package_name: str, version: str) -> Dict[str, Any]:
    """Fetch package manifest"""
    url = f"{EPR_PACKAGE_URL}/{package_name}/{version}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_package_fields(package_name: str, version: str) -> List[Dict[str, Any]]:
    """Fetch fields.yml from package"""
    try:
        # Try to fetch fields from package
        url = f"{EPR_PACKAGE_URL}/{package_name}/{version}/fields/fields.yml"
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            fields = yaml.safe_load(response.text)
            return fields if isinstance(fields, list) else []
    except Exception as e:
        pass
    
    return []


def fetch_package_pipelines(package_name: str, version: str) -> List[Dict[str, Any]]:
    """Fetch ingest pipelines from package"""
    pipelines = []
    
    try:
        # Common pipeline paths
        pipeline_paths = [
            "ingest_pipeline/default.yml",
            "elasticsearch/ingest_pipeline/default.yml"
        ]
        
        for path in pipeline_paths:
            url = f"{EPR_PACKAGE_URL}/{package_name}/{version}/{path}"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                pipeline = yaml.safe_load(response.text)
                if pipeline:
                    pipelines.append(pipeline)
    except Exception:
        pass
    
    return pipelines


def generate_mapping_from_fields(
    package_name: str,
    fields: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Generate mapping examples from fields"""
    examples = []
    
    # Group fields by data stream or type
    field_groups = {}
    
    for field in fields:
        field_name = field.get("name", "")
        field_type = field.get("type", "keyword")
        
        if not field_name:
            continue
        
        # Group by top-level field (e.g., "nginx" in "nginx.access")
        parts = field_name.split(".")
        group = parts[0] if len(parts) > 1 else "default"
        
        if group not in field_groups:
            field_groups[group] = []
        
        field_groups[group].append(field)
    
    # Generate mapping for each group
    for group, group_fields in field_groups.items():
        # Create batches of 3-7 fields
        for i in range(0, len(group_fields), random.randint(3, 7)):
            batch = group_fields[i:i+random.randint(3, 7)]
            
            if not batch:
                continue
            
            # Build mapping
            mapping_properties = {}
            field_names = []
            
            for field in batch:
                field_name = field.get("name", "")
                field_type = field.get("type", "keyword")
                
                field_names.append(field_name)
                
                # Map field type
                type_map = {
                    "keyword": "keyword",
                    "text": "text",
                    "long": "long",
                    "integer": "long",
                    "ip": "ip",
                    "date": "date",
                    "boolean": "boolean",
                    "float": "float",
                    "geo_point": "geo_point"
                }
                
                es_type = type_map.get(field_type, "keyword")
                
                # Handle nested fields
                if "." in field_name:
                    parts = field_name.split(".")
                    current = mapping_properties
                    
                    for part in parts[:-1]:
                        if part not in current:
                            current[part] = {"properties": {}}
                        elif "properties" not in current[part]:
                            current[part]["properties"] = {}
                        current = current[part]["properties"]
                    
                    current[parts[-1]] = {"type": es_type}
                else:
                    mapping_properties[field_name] = {"type": es_type}
            
            # Create index template
            full_mapping = {
                "index_patterns": [f"logs-{package_name}-*"],
                "template": {
                    "settings": {
                        "number_of_shards": 1
                    },
                    "mappings": {
                        "properties": mapping_properties
                    }
                }
            }
            
            # Generate instruction
            instructions = [
                f"Create a mapping for {package_name} integration with fields {', '.join(field_names[:3])}.",
                f"Generate an index template for {package_name} logs.",
                f"Define an Elasticsearch mapping for {package_name} with fields {', '.join(field_names[:2])}.",
                f"Create an index template for {package_name} including {', '.join(field_names[:3])}."
            ]
            
            example = {
                "task": "mapping_create",
                "domain": f"integration:{package_name}",
                "instruction": random.choice(instructions),
                "output": json.dumps(full_mapping, ensure_ascii=False, separators=(',', ':')),
                "source": f"integration/{package_name}",
                "field_count": len(field_names)
            }
            
            examples.append(example)
    
    return examples


def generate_pipeline_examples(
    package_name: str,
    pipelines: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Generate pipeline examples"""
    examples = []
    
    for pipeline in pipelines:
        if not isinstance(pipeline, dict):
            continue
        
        processors = pipeline.get("processors", [])
        
        if not processors:
            continue
        
        # Generate instruction
        processor_types = [list(p.keys())[0] for p in processors if p][:3]
        
        instructions = [
            f"Create an ingest pipeline for {package_name} with {', '.join(processor_types[:2])} processors.",
            f"Define an ingest pipeline to process {package_name} logs.",
            f"Generate an Elasticsearch ingest pipeline for {package_name} with {', '.join(processor_types)} processors.",
            f"Create a pipeline for {package_name} logs processing."
        ]
        
        example = {
            "task": "pipeline_create",
            "domain": f"integration:{package_name}",
            "instruction": random.choice(instructions),
            "output": json.dumps({"processors": processors}, ensure_ascii=False, separators=(',', ':')),
            "source": f"integration/{package_name}",
            "processor_count": len(processors)
        }
        
        examples.append(example)
    
    return examples


def collect_integrations():
    """Main collection function"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("="*70)
    print("Elastic Integrations Data Collection")
    print("="*70)
    
    # Search for popular integration categories with higher limits
    categories = [
        "web",
        "security",
        "observability",
        "network",
        "cloud",
        "custom"
    ]
    
    # Also search without category to get all packages
    all_packages = []
    
    # Get all packages (no category filter)
    try:
        print("Fetching all packages...")
        all_packages = search_packages(category=None, limit=200)
        time.sleep(1)
    except Exception as e:
        print(f"Error fetching all packages: {e}")
    
    # Also get category-specific packages
    for category in categories:
        try:
            packages = search_packages(category=category, limit=50)
            all_packages.extend(packages)
            time.sleep(0.5)  # Rate limiting
        except Exception as e:
            print(f"Error fetching {category} packages: {e}")
    
    # Deduplicate packages by name
    unique_packages = {}
    for pkg in all_packages:
        pkg_name = pkg.get("name", "")
        if pkg_name:
            # Keep the latest version
            if pkg_name not in unique_packages:
                unique_packages[pkg_name] = pkg
            else:
                # Compare versions and keep the latest
                current_version = unique_packages[pkg_name].get("version", "0.0.0")
                new_version = pkg.get("version", "0.0.0")
                if new_version > current_version:
                    unique_packages[pkg_name] = pkg
    
    print(f"\nFound {len(unique_packages)} unique packages to process...")
    
    all_examples = []
    processed_count = 0
    
    for pkg_name, pkg_info in unique_packages.items():
        try:
            version = pkg_info.get("version", "latest")
            
            print(f"\n[{processed_count + 1}/{len(unique_packages)}] Processing {pkg_name} v{version}")
            
            # Fetch fields
            fields = fetch_package_fields(pkg_name, version)
            if fields and len(fields) > 0:
                mapping_examples = generate_mapping_from_fields(pkg_name, fields)
                all_examples.extend(mapping_examples)
                print(f"  Generated {len(mapping_examples)} mapping examples from {len(fields)} fields")
            else:
                # Try alternative: fetch manifest and extract fields from there
                try:
                    manifest = fetch_package_manifest(pkg_name, version)
                    # Some packages have fields in the manifest
                    if "data_streams" in manifest:
                        for ds in manifest["data_streams"]:
                            if "streams" in ds:
                                for stream in ds["streams"]:
                                    if "template" in stream and "mappings" in stream["template"]:
                                        # Generate example from template mappings
                                        props = stream["template"]["mappings"].get("properties", {})
                                        if props:
                                            example = {
                                                "task": "mapping_create",
                                                "domain": f"integration:{pkg_name}",
                                                "instruction": f"Create a mapping for {pkg_name} {ds.get('name', 'logs')} data stream.",
                                                "output": json.dumps({
                                                    "index_patterns": [f"logs-{pkg_name}-*"],
                                                    "template": {
                                                        "mappings": {"properties": props}
                                                    }
                                                }, ensure_ascii=False, separators=(',', ':')),
                                                "source": f"integration/{pkg_name}"
                                            }
                                            all_examples.append(example)
                except:
                    pass
            
            # Fetch pipelines
            pipelines = fetch_package_pipelines(pkg_name, version)
            if pipelines and len(pipelines) > 0:
                pipeline_examples = generate_pipeline_examples(pkg_name, pipelines)
                all_examples.extend(pipeline_examples)
                print(f"  Generated {len(pipeline_examples)} pipeline examples")
            
            processed_count += 1
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"  Error processing {pkg_name}: {e}")
    
    # Save examples
    output_file = OUTPUT_DIR / "integrations.jsonl"
    print(f"\nSaving {len(all_examples)} examples to {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in all_examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    # Save metadata
    metadata = {
        "source": "Elastic Package Registry",
        "total_examples": len(all_examples),
        "packages_processed": processed_count,
        "url": "https://epr.elastic.co"
    }
    
    metadata_file = OUTPUT_DIR / "metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"[OK] Integrations collection complete!")
    print(f"     Total examples: {len(all_examples)}")
    print(f"     Packages processed: {processed_count}")
    print(f"     Output: {output_file}")
    print(f"{'='*70}")


if __name__ == "__main__":
    collect_integrations()

