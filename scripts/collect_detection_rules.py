#!/usr/bin/env python3
"""
Elastic Detection Rules Collector

Fetches security detection rules with KQL and EQL queries.

Source: https://github.com/elastic/detection-rules
Output: ~2-3k KQL + ~500-800 EQL examples
"""

import json
import requests
import toml
from pathlib import Path
from typing import Dict, List, Any
import random

OUTPUT_DIR = Path("../datasets/raw/detection_rules")
RULES_REPO = "https://api.github.com/repos/elastic/detection-rules"
RULES_RAW_BASE = "https://raw.githubusercontent.com/elastic/detection-rules/main"


def fetch_rules_tree() -> List[Dict[str, Any]]:
    """Get list of rule files from GitHub"""
    print("Fetching detection rules tree...")
    
    # Get tree of rules directory
    url = f"{RULES_REPO}/contents/rules"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    contents = response.json()
    
    # Filter for rule directories
    rule_dirs = [item for item in contents if item["type"] == "dir"]
    
    print(f"Found {len(rule_dirs)} rule categories")
    return rule_dirs


def fetch_category_rules(category_path: str) -> List[str]:
    """Get list of .toml files in a category"""
    url = f"{RULES_REPO}/contents/{category_path}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    contents = response.json()
    
    # Filter for .toml files
    toml_files = [
        item["path"] for item in contents 
        if item["type"] == "file" and item["name"].endswith(".toml")
    ]
    
    return toml_files


def fetch_rule_file(file_path: str) -> Dict[str, Any]:
    """Fetch and parse a rule TOML file"""
    url = f"{RULES_RAW_BASE}/{file_path}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    rule_data = toml.loads(response.text)
    return rule_data


def parse_rule(rule_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse rule data and extract relevant fields"""
    metadata = rule_data.get("metadata", {})
    rule = rule_data.get("rule", {})
    
    # Extract query
    query = rule.get("query", "")
    language = rule.get("language", "kuery")  # kuery = KQL
    
    # Extract metadata
    description = rule.get("description", "")
    name = rule.get("name", "")
    risk_score = rule.get("risk_score", 0)
    severity = rule.get("severity", "")
    
    # Extract MITRE ATT&CK info
    threat = rule.get("threat", [])
    tactics = []
    techniques = []
    
    for t in threat:
        if "tactic" in t:
            tactics.append(t["tactic"].get("name", ""))
        if "technique" in t:
            for tech in t["technique"]:
                techniques.append(tech.get("name", ""))
    
    return {
        "query": query,
        "language": language,
        "description": description,
        "name": name,
        "risk_score": risk_score,
        "severity": severity,
        "tactics": tactics,
        "techniques": techniques
    }


def generate_kql_instruction(rule: Dict[str, Any]) -> str:
    """Generate instruction for KQL query"""
    description = rule.get("description", "")
    name = rule.get("name", "")
    techniques = rule.get("techniques", [])
    
    # Use description or name
    base = description if description else name
    
    # Shorten if too long
    if len(base) > 150:
        base = base[:150] + "..."
    
    instructions = [
        base,
        f"Create KQL query to detect: {base}",
        f"Write a detection rule for: {base}",
        f"Generate KQL for: {base}"
    ]
    
    # Add technique-based instruction
    if techniques:
        tech = techniques[0]
        instructions.append(f"Create detection for MITRE technique: {tech}")
        instructions.append(f"Detect suspicious activity related to {tech}")
    
    return random.choice(instructions)


def generate_eql_instruction(rule: Dict[str, Any]) -> str:
    """Generate instruction for EQL query"""
    description = rule.get("description", "")
    name = rule.get("name", "")
    
    base = description if description else name
    
    if len(base) > 150:
        base = base[:150] + "..."
    
    instructions = [
        base,
        f"Write an EQL sequence query for: {base}",
        f"Detect event sequence: {base}",
        f"Create EQL query to detect: {base}"
    ]
    
    return random.choice(instructions)


def collect_detection_rules():
    """Main collection function"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("="*70)
    print("Elastic Detection Rules Collection")
    print("="*70)
    
    # Get rule directories
    rule_dirs = fetch_rules_tree()
    
    kql_examples = []
    eql_examples = []
    
    # Process ALL categories (not just first 10)
    for rule_dir in rule_dirs:
        category = rule_dir["name"]
        category_path = rule_dir["path"]
        
        print(f"\nProcessing category: {category}")
        
        try:
            # Get rule files in this category
            rule_files = fetch_category_rules(category_path)
            print(f"  Found {len(rule_files)} rules")
            
            # Process ALL rules in category (removed limit)
            for rule_file in rule_files:
                try:
                    rule_data = fetch_rule_file(rule_file)
                    parsed_rule = parse_rule(rule_data)
                    
                    query = parsed_rule["query"]
                    language = parsed_rule["language"]
                    
                    if not query:
                        continue
                    
                    # Create example based on language
                    if language in ["kuery", "kql"]:
                        instruction = generate_kql_instruction(parsed_rule)
                        
                        example = {
                            "task": "kql",
                            "domain": "security",
                            "instruction": instruction,
                            "output": query,
                            "source": f"detection-rules/{category}",
                            "severity": parsed_rule["severity"],
                            "risk_score": parsed_rule["risk_score"]
                        }
                        
                        kql_examples.append(example)
                    
                    elif language == "eql":
                        instruction = generate_eql_instruction(parsed_rule)
                        
                        example = {
                            "task": "eql",
                            "domain": "security",
                            "instruction": instruction,
                            "output": query,
                            "source": f"detection-rules/{category}",
                            "severity": parsed_rule["severity"],
                            "risk_score": parsed_rule["risk_score"]
                        }
                        
                        eql_examples.append(example)
                
                except Exception as e:
                    # Skip individual rule errors
                    pass
        
        except Exception as e:
            print(f"  Error processing category {category}: {e}")
    
    # Save KQL examples
    kql_file = OUTPUT_DIR / "kql_rules.jsonl"
    print(f"\nSaving {len(kql_examples)} KQL examples to {kql_file}")
    
    with open(kql_file, 'w', encoding='utf-8') as f:
        for example in kql_examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    # Save EQL examples
    eql_file = OUTPUT_DIR / "eql_rules.jsonl"
    print(f"Saving {len(eql_examples)} EQL examples to {eql_file}")
    
    with open(eql_file, 'w', encoding='utf-8') as f:
        for example in eql_examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    # Save metadata
    metadata = {
        "source": "Elastic Detection Rules",
        "kql_examples": len(kql_examples),
        "eql_examples": len(eql_examples),
        "total_examples": len(kql_examples) + len(eql_examples),
        "url": "https://github.com/elastic/detection-rules"
    }
    
    metadata_file = OUTPUT_DIR / "metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"[OK] Detection rules collection complete!")
    print(f"     KQL examples: {len(kql_examples)}")
    print(f"     EQL examples: {len(eql_examples)}")
    print(f"     Total: {len(kql_examples) + len(eql_examples)}")
    print(f"{'='*70}")


if __name__ == "__main__":
    collect_detection_rules()

