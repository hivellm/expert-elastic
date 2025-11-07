#!/usr/bin/env python3
"""
Dataset Validator

Validates the processed dataset for:
- JSON syntax (for DSL/mapping/pipeline tasks)
- KQL/EQL syntax (basic validation)
- Field completeness
- Task distribution

Usage:
    python validate_dataset.py --input ../datasets/train.jsonl
"""

import argparse
import json
from pathlib import Path
from typing import Dict, Any
from collections import defaultdict


def validate_json_output(output: str) -> bool:
    """Validate JSON syntax"""
    try:
        json.loads(output)
        return True
    except Exception:
        return False


def validate_kql(query: str) -> bool:
    """Basic KQL validation"""
    if not query or not query.strip():
        return False
    
    # Basic checks
    # KQL should have field:value patterns or boolean operators
    has_field_value = ":" in query
    has_operator = any(op in query.lower() for op in ["and", "or", "not"])
    
    return has_field_value or has_operator


def validate_eql(query: str) -> bool:
    """Basic EQL validation"""
    if not query or not query.strip():
        return False
    
    # EQL should have event type in brackets or sequence keyword
    has_event_type = "[" in query and "]" in query
    has_sequence = "sequence" in query.lower()
    has_where = "where" in query.lower()
    
    return (has_event_type and has_where) or has_sequence


def extract_task(text: str) -> str:
    """Extract task from ChatML formatted text"""
    # Look for "Task: <task_name>" in system section
    if "Task:" in text:
        start = text.find("Task:") + 5
        end = text.find("\n", start)
        if end == -1:
            end = text.find("<|end|>", start)
        return text[start:end].strip()
    return "unknown"


def extract_output(text: str) -> str:
    """Extract output from ChatML formatted text"""
    # Look for assistant section
    if "<|assistant|>" in text:
        start = text.find("<|assistant|>") + 13
        end = text.find("<|end|>", start)
        if end > start:
            return text[start:end].strip()
    return ""


def validate_example(example: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a single example"""
    text = example.get("text", "")
    
    if not text:
        return {"valid": False, "error": "Empty text field"}
    
    # Extract task and output
    task = extract_task(text)
    output = extract_output(text)
    
    if not output:
        return {"valid": False, "error": "No output found", "task": task}
    
    # Validate based on task
    if task in ["mapping_create", "query_dsl", "pipeline_create"]:
        if not validate_json_output(output):
            return {"valid": False, "error": "Invalid JSON", "task": task}
    
    elif task == "kql":
        if not validate_kql(output):
            return {"valid": False, "error": "Invalid KQL", "task": task}
    
    elif task == "eql":
        if not validate_eql(output):
            return {"valid": False, "error": "Invalid EQL", "task": task}
    
    return {"valid": True, "task": task}


def validate_dataset(dataset_path: Path):
    """Validate entire dataset"""
    print("="*70)
    print("Dataset Validation")
    print("="*70)
    print(f"Dataset: {dataset_path}\n")
    
    if not dataset_path.exists():
        print(f"[ERROR] Dataset not found: {dataset_path}")
        return
    
    # Load dataset
    examples = []
    with open(dataset_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                example = json.loads(line)
                examples.append(example)
            except Exception as e:
                print(f"[ERROR] Line {line_num}: Failed to parse JSON: {e}")
    
    print(f"Loaded {len(examples)} examples\n")
    
    # Validate examples
    results = []
    task_counts = defaultdict(int)
    error_counts = defaultdict(int)
    
    for idx, example in enumerate(examples, 1):
        result = validate_example(example)
        results.append(result)
        
        if result["valid"]:
            task_counts[result["task"]] += 1
        else:
            error_counts[result.get("error", "unknown")] += 1
        
        if idx % 1000 == 0:
            print(f"Validated {idx}/{len(examples)} examples...")
    
    # Print results
    valid_count = sum(1 for r in results if r["valid"])
    invalid_count = len(results) - valid_count
    
    print("\n" + "="*70)
    print("VALIDATION RESULTS")
    print("="*70)
    print(f"\nTotal examples:   {len(examples)}")
    print(f"Valid:            {valid_count} ({valid_count/len(examples)*100:.1f}%)")
    print(f"Invalid:          {invalid_count} ({invalid_count/len(examples)*100:.1f}%)")
    
    print("\nTask distribution:")
    for task, count in sorted(task_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = count / valid_count * 100 if valid_count > 0 else 0
        print(f"  {task:20s}: {count:6d} ({percentage:5.1f}%)")
    
    if error_counts:
        print("\nError distribution:")
        for error, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {error:20s}: {count:6d}")
    
    # Sample invalid examples
    invalid_examples = [r for r in results if not r["valid"]]
    if invalid_examples and len(invalid_examples) <= 10:
        print(f"\nInvalid examples:")
        for idx, result in enumerate(invalid_examples[:10], 1):
            print(f"  {idx}. {result.get('error', 'unknown')} (task: {result.get('task', 'unknown')})")
    
    print("\n" + "="*70)
    
    if invalid_count == 0:
        print("[OK] All examples are valid!")
    elif invalid_count / len(examples) < 0.01:
        print(f"[WARNING] {invalid_count} invalid examples ({invalid_count/len(examples)*100:.2f}%)")
    else:
        print(f"[ERROR] {invalid_count} invalid examples ({invalid_count/len(examples)*100:.1f}%)")
        print("Consider reviewing and fixing invalid examples before training.")
    
    print("="*70)


def main():
    parser = argparse.ArgumentParser(description="Validate expert-elastic dataset")
    
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("../datasets/train.jsonl"),
        help="Path to dataset file (default: ../datasets/train.jsonl)"
    )
    
    args = parser.parse_args()
    
    validate_dataset(args.input)


if __name__ == "__main__":
    main()

