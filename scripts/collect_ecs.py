#!/usr/bin/env python3
"""
ECS (Elastic Common Schema) Collector

Fetches ECS field definitions and generates mapping examples.

Source: https://github.com/elastic/ecs
Output: ~5-8k mapping examples
"""

import json
import yaml
import requests
from pathlib import Path
from typing import Dict, List, Any
import random

OUTPUT_DIR = Path("../datasets/raw/ecs")
ECS_REPO = "https://api.github.com/repos/elastic/ecs"
ECS_RAW_BASE = "https://raw.githubusercontent.com/elastic/ecs/main"


def fetch_ecs_version() -> str:
    """Get latest ECS version from GitHub"""
    print("Fetching latest ECS version...")
    response = requests.get(f"{ECS_REPO}/tags", timeout=30)
    response.raise_for_status()
    tags = response.json()
    if tags:
        return tags[0]["name"]  # Latest tag (e.g., 'v8.11.0')
    return "main"


def fetch_schema_files(version: str = "main") -> List[str]:
    """Get list of YAML schema files"""
    print(f"Fetching schema files for version {version}...")
    
    # ECS schemas are in schemas/ directory
    schemas = [
        "base.yml",
        "client.yml",
        "server.yml",
        "host.yml",
        "user.yml",
        "process.yml",
        "file.yml",
        "network.yml",
        "http.yml",
        "url.yml",
        "dns.yml",
        "event.yml",
        "log.yml",
        "source.yml",
        "destination.yml",
        "geo.yml",
        "container.yml",
        "cloud.yml",
        "agent.yml",
        "ecs.yml"
    ]
    
    return schemas


def parse_ecs_field(field_name: str, field_def: Dict[str, Any]) -> Dict[str, Any]:
    """Parse ECS field definition to Elasticsearch mapping"""
    mapping = {}
    
    # Map ECS types to Elasticsearch types
    type_mapping = {
        "keyword": "keyword",
        "text": "text",
        "long": "long",
        "integer": "long",
        "ip": "ip",
        "date": "date",
        "boolean": "boolean",
        "float": "float",
        "geo_point": "geo_point",
        "object": "object",
        "nested": "nested",
        "flattened": "flattened"
    }
    
    field_type = field_def.get("type", "keyword")
    es_type = type_mapping.get(field_type, "keyword")
    
    if es_type in ["object", "nested"]:
        mapping["type"] = es_type
        if "fields" in field_def:
            mapping["properties"] = {}
    else:
        mapping["type"] = es_type
    
    # Add additional properties
    if field_def.get("index") is False:
        mapping["index"] = False
    
    if "ignore_above" in field_def:
        mapping["ignore_above"] = field_def["ignore_above"]
    
    return mapping


def generate_mapping_instruction(field_group: str, fields: List[str]) -> str:
    """Generate natural language instruction for mapping creation (English only)"""
    instructions = [
        f"Create an ECS mapping for {field_group} with fields {', '.join(fields[:3])}.",
        f"Generate an index template for {field_group} logs including {', '.join(fields[:3])}.",
        f"Define an Elasticsearch mapping for {field_group} with ECS fields {', '.join(fields[:2])}.",
        f"Create an index template for {field_group} with fields {', '.join(fields[:3])}.",
        f"Generate a mapping for {field_group} including {', '.join(fields[:2])}.",
    ]
    return random.choice(instructions)


def process_schema_file(schema_name: str, version: str = "main") -> List[Dict[str, Any]]:
    """Process a single ECS schema file"""
    examples = []
    
    try:
        # Fetch YAML file
        url = f"{ECS_RAW_BASE}/schemas/{schema_name}"
        print(f"  Fetching {schema_name}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Parse YAML
        schema_data = yaml.safe_load(response.text)
        
        if not schema_data:
            return examples
        
        # Extract field group name
        field_group = schema_name.replace(".yml", "")
        
        # ECS YAML structure: list of objects, each with a "fields" array
        fields = []
        if isinstance(schema_data, list):
            for item in schema_data:
                if isinstance(item, dict) and "fields" in item:
                    # Extract fields from this item
                    item_fields = item.get("fields", [])
                    if isinstance(item_fields, list):
                        fields.extend(item_fields)
                elif isinstance(item, dict) and "name" in item:
                    # Direct field definition
                    fields.append(item)
        elif isinstance(schema_data, dict):
            if "fields" in schema_data:
                fields = schema_data["fields"]
            elif "name" in schema_data:
                # Single field
                fields = [schema_data]
        
        if not fields or len(fields) == 0:
            print(f"    No fields found in {schema_name}")
            return examples
        
        print(f"    Found {len(fields)} fields")
        
        # Generate mapping examples
        # Generate multiple examples per schema with different field combinations
        # Group fields by 3-7 for realistic mappings
        num_examples = min(20, max(5, len(fields) // 2))  # Generate 5-20 examples per schema
        
        for _ in range(num_examples):
            # Randomly select 3-7 fields (ensure we have enough fields)
            if len(fields) < 3:
                # If less than 3 fields, use all fields
                field_batch = fields
            else:
                num_fields = random.randint(3, min(7, len(fields)))
                field_batch = random.sample(fields, num_fields)
            
            if not field_batch:
                continue
            
            # Build mapping
            mapping_properties = {}
            field_names = []
            
            for field in field_batch:
                field_name = field.get("name", "")
                if not field_name:
                    continue
                
                field_names.append(field_name)
                
                # Handle nested fields (e.g., "client.ip" -> nested structure)
                if "." in field_name:
                    parts = field_name.split(".")
                    current = mapping_properties
                    
                    for part_idx, part in enumerate(parts[:-1]):
                        if part not in current:
                            current[part] = {"properties": {}}
                        elif "properties" not in current[part]:
                            current[part]["properties"] = {}
                        current = current[part]["properties"]
                    
                    # Last part is the actual field
                    current[parts[-1]] = parse_ecs_field(field_name, field)
                else:
                    mapping_properties[field_name] = parse_ecs_field(field_name, field)
            
            if not field_names:
                continue
            
            # Create full mapping with index template
            full_mapping = {
                "index_patterns": [f"logs-{field_group}-*"],
                "template": {
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 1
                    },
                    "mappings": {
                        "properties": mapping_properties
                    }
                }
            }
            
            # Generate instruction
            instruction = generate_mapping_instruction(field_group, field_names)
            
            # Create example
            example = {
                "task": "mapping_create",
                "domain": f"ecs:{field_group}",
                "instruction": instruction,
                "output": json.dumps(full_mapping, ensure_ascii=False, separators=(',', ':')),
                "source": f"ecs/{schema_name}",
                "field_count": len(field_names)
            }
            
            examples.append(example)
    
    except Exception as e:
        print(f"  Error processing {schema_name}: {e}")
    
    return examples


def collect_ecs_data():
    """Main collection function"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("="*70)
    print("ECS (Elastic Common Schema) Data Collection")
    print("="*70)
    
    # Get latest version
    version = fetch_ecs_version()
    print(f"Using ECS version: {version}\n")
    
    # Get schema files
    schemas = fetch_schema_files(version)
    
    # Process each schema
    all_examples = []
    for schema in schemas:
        examples = process_schema_file(schema, version)
        all_examples.extend(examples)
        print(f"  Generated {len(examples)} examples from {schema}")
    
    # Save examples
    output_file = OUTPUT_DIR / "ecs_mappings.jsonl"
    print(f"\nSaving {len(all_examples)} examples to {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in all_examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    # Save metadata
    metadata = {
        "source": "ECS (Elastic Common Schema)",
        "version": version,
        "total_examples": len(all_examples),
        "schemas_processed": len(schemas),
        "url": "https://github.com/elastic/ecs"
    }
    
    metadata_file = OUTPUT_DIR / "metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"[OK] ECS collection complete!")
    print(f"     Total examples: {len(all_examples)}")
    print(f"     Output: {output_file}")
    print(f"{'='*70}")


if __name__ == "__main__":
    collect_ecs_data()

