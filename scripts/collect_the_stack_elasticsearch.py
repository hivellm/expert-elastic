#!/usr/bin/env python3
"""
Extract Elasticsearch code examples from bigcode/the-stack dataset.

This script:
1. Loads The Stack dataset (streaming)
2. Filters files mentioning Elasticsearch
3. Extracts query DSL, mappings, pipelines from code
4. Generates instruction-output pairs
5. Validates JSON/DSL syntax
6. Saves to datasets/raw/the_stack_elasticsearch.jsonl

Requirements:
- HuggingFace token (accept terms at https://huggingface.co/datasets/bigcode/the-stack)
- datasets library: pip install datasets
- Set HF_TOKEN environment variable or use huggingface-cli login

Usage:
    export HF_TOKEN=your_token_here
    python scripts/collect_the_stack_elasticsearch.py --limit 10000
"""

import json
import re
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
import argparse
from tqdm import tqdm

try:
    from datasets import load_dataset
except ImportError:
    print("[ERROR] datasets library not found. Install with: pip install datasets")
    exit(1)


# Languages that commonly use Elasticsearch
ELASTICSEARCH_LANGUAGES = ["python", "javascript", "typescript", "java", "go", "ruby"]

# Keywords to identify Elasticsearch-related code
ELASTICSEARCH_KEYWORDS = [
    "elasticsearch",
    "elasticsearch-py",
    "elasticsearch-js",
    "elasticsearch-java",
    "es.",
    "client.search",
    "client.index",
    "client.indices",
    "client.ingest",
    "query_dsl",
    "QueryBuilders",
    "SearchRequest",
    "elasticsearch_dsl",
]


def extract_json_from_code(code: str, start_pattern: str) -> Optional[Dict[str, Any]]:
    """Extract JSON object from code starting with a pattern."""
    # Find pattern in code
    pattern_idx = code.find(start_pattern)
    if pattern_idx == -1:
        return None
    
    # Find first opening brace after pattern
    search_start = pattern_idx + len(start_pattern)
    brace_start = code.find('{', search_start)
    if brace_start == -1:
        return None
    
    # Find matching closing brace
    brace_count = 0
    brace_end = brace_start
    
    for i in range(brace_start, len(code)):
        if code[i] == '{':
            brace_count += 1
        elif code[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                brace_end = i + 1
                break
    
    if brace_count != 0:
        return None
    
    json_text = code[brace_start:brace_end]
    
    # Try to parse JSON
    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        # Try cleaning up common issues
        json_text = json_text.replace('\n', ' ').replace('\t', ' ')
        json_text = re.sub(r',\s*}', '}', json_text)
        json_text = re.sub(r',\s*]', ']', json_text)
        try:
            return json.loads(json_text)
        except:
            return None


def extract_query_dsl(code: str, language: str) -> List[Dict[str, Any]]:
    """Extract Query DSL examples from code."""
    examples = []
    
    if language == "python":
        # Pattern: client.search(..., body={"query": {...}})
        patterns = [
            r'body\s*=\s*\{[^}]*"query"[^}]*\}',
            r'body:\s*\{[^}]*"query"[^}]*\}',
            r'\{"query"\s*:\s*\{[^}]*\}\}',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, code, re.DOTALL)
            for match in matches:
                json_obj = extract_json_from_code(code, match.group(0))
                if json_obj and "query" in json_obj:
                    examples.append({
                        "type": "query_dsl",
                        "json": json_obj,
                        "raw_code": match.group(0)[:200]
                    })
    
    elif language in ["javascript", "typescript"]:
        # Pattern: body: { query: {...} }
        patterns = [
            r'body\s*:\s*\{[^}]*query[^}]*\}',
            r'\{\s*query\s*:\s*\{[^}]*\}\s*\}',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, code, re.DOTALL)
            for match in matches:
                json_obj = extract_json_from_code(code, match.group(0))
                if json_obj and "query" in json_obj:
                    examples.append({
                        "type": "query_dsl",
                        "json": json_obj,
                        "raw_code": match.group(0)[:200]
                    })
    
    elif language == "java":
        # Pattern: QueryBuilders.matchQuery(...)
        # More complex, would need AST parsing
        pass
    
    return examples


def extract_mappings(code: str, language: str) -> List[Dict[str, Any]]:
    """Extract mapping definitions from code."""
    examples = []
    
    if language == "python":
        # Pattern: client.indices.create(..., body={"mappings": {...}})
        pattern = r'"mappings"\s*:\s*\{[^}]*\}'
        matches = re.finditer(pattern, code, re.DOTALL)
        for match in matches:
            json_obj = extract_json_from_code(code, match.group(0))
            if json_obj and "mappings" in json_obj:
                examples.append({
                    "type": "mapping_create",
                    "json": json_obj,
                    "raw_code": match.group(0)[:200]
                })
    
    return examples


def extract_pipelines(code: str, language: str) -> List[Dict[str, Any]]:
    """Extract ingest pipeline definitions from code."""
    examples = []
    
    if language == "python":
        # Pattern: client.ingest.put_pipeline(..., body={"processors": [...]})
        pattern = r'"processors"\s*:\s*\[[^\]]*\]'
        matches = re.finditer(pattern, code, re.DOTALL)
        for match in matches:
            json_obj = extract_json_from_code(code, match.group(0))
            if json_obj and "processors" in json_obj:
                examples.append({
                    "type": "pipeline_create",
                    "json": json_obj,
                    "raw_code": match.group(0)[:200]
                })
    
    return examples


def generate_instruction(code_example: Dict[str, Any], context: str, language: str) -> str:
    """Generate natural language instruction from code context."""
    # Try to extract from function/class name
    func_match = re.search(r'(?:def|function|class)\s+(\w+)', context)
    if func_match:
        func_name = func_match.group(1)
        # Convert camelCase/snake_case to readable
        readable = re.sub(r'([a-z])([A-Z])', r'\1 \2', func_name).lower()
        return f"Create Elasticsearch {code_example['type']} for {readable}"
    
    # Try to extract from comments
    comment_match = re.search(r'(?:#|//|/\*)\s*(.+?)(?:\n|\*/)', context)
    if comment_match:
        return comment_match.group(1).strip()[:200]
    
    # Default instruction
    task_type = code_example['type'].replace('_', ' ')
    return f"Create Elasticsearch {task_type}"


def process_file(content: str, language: str, file_path: str = "") -> List[Dict[str, Any]]:
    """Process a single file and extract Elasticsearch examples."""
    examples = []
    
    # Check if file mentions Elasticsearch
    content_lower = content.lower()
    if not any(keyword.lower() in content_lower for keyword in ELASTICSEARCH_KEYWORDS):
        return examples
    
    # Extract different types of examples
    query_examples = extract_query_dsl(content, language)
    mapping_examples = extract_mappings(content, language)
    pipeline_examples = extract_pipelines(content, language)
    
    all_extracted = query_examples + mapping_examples + pipeline_examples
    
    # Generate training examples
    for extracted in all_extracted:
        instruction = generate_instruction(extracted, content, language)
        
        example = {
            "task": extracted["type"],
            "domain": f"the-stack/{language}",
            "instruction": instruction,
            "output": json.dumps(extracted["json"], ensure_ascii=False, separators=(',', ':')),
            "source": "the-stack",
            "source_file": file_path,
            "language": language
        }
        
        examples.append(example)
    
    return examples


def load_the_stack_elasticsearch(
    limit: Optional[int] = None,
    token: Optional[str] = None,
    languages: List[str] = None,
    max_check: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Load and process Elasticsearch-related files from The Stack."""
    
    if languages is None:
        languages = ELASTICSEARCH_LANGUAGES
    
    print("="*80)
    print("Loading Elasticsearch code from bigcode/the-stack")
    print(f"Languages: {', '.join(languages)}")
    print("="*80)
    
    # Get token
    if not token:
        token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    
    if not token:
        try:
            from huggingface_hub import HfFolder
            token = HfFolder.get_token()
        except Exception:
            pass
    
    if not token:
        print("[WARNING] No HuggingFace token found. Set HF_TOKEN environment variable.")
        print("          Or use: huggingface-cli login")
        print("          Accept terms at: https://huggingface.co/datasets/bigcode/the-stack")
        return []
    
    try:
        # Load dataset (streaming mode for large dataset)
        dataset = load_dataset(
            "bigcode/the-stack",
            split="train",
            streaming=True,
            token=token
        )
        print("[OK] Dataset loaded (streaming mode)")
    except Exception as e:
        print(f"[ERROR] Failed to load dataset: {e}")
        print("[INFO] Make sure you:")
        print("  1. Accepted terms at https://huggingface.co/datasets/bigcode/the-stack")
        print("  2. Set HF_TOKEN environment variable or logged in with huggingface-cli")
        return []
    
    all_examples = []
    processed_files = 0  # Files that contained Elasticsearch code
    skipped_files = 0
    checked_files = 0   # Total files checked
    max_files_to_check = max_check if max_check else (limit * 20 if limit else None)  # Check up to 20x limit to find matches
    
    print(f"\nProcessing files...")
    print(f"  Limit: {limit or 'unlimited'} files WITH Elasticsearch code")
    print(f"  Max files to check: {max_files_to_check or 'unlimited'}")
    print(f"  Languages: {', '.join(languages)}")
    print("")
    
    for example in tqdm(dataset, desc="Checking files"):
        checked_files += 1
        
        # Stop if we've checked enough files
        if max_files_to_check and checked_files >= max_files_to_check:
            print(f"\n[INFO] Reached max files to check ({max_files_to_check:,}). Stopping.")
            break
        
        # Stop if we've found enough files with Elasticsearch
        if limit and processed_files >= limit:
            print(f"\n[INFO] Found {processed_files} files with Elasticsearch code. Stopping.")
            break
        
        # Get file info
        file_ext = example.get("ext", "").lower()
        content = example.get("content", "")
        file_path = example.get("max_stars_repo_path", "") or example.get("path", "")
        
        # Determine language
        language = None
        if file_ext in ["py"]:
            language = "python"
        elif file_ext in ["js", "jsx"]:
            language = "javascript"
        elif file_ext in ["ts", "tsx"]:
            language = "typescript"
        elif file_ext in ["java"]:
            language = "java"
        elif file_ext in ["go"]:
            language = "go"
        elif file_ext in ["rb"]:
            language = "ruby"
        
        if language not in languages:
            skipped_files += 1
            continue
        
        if not content or len(content) < 100:
            skipped_files += 1
            continue
        
        # Process file
        file_examples = process_file(content, language, file_path)
        
        if file_examples:
            all_examples.extend(file_examples)
            processed_files += 1
        else:
            skipped_files += 1
    
    print(f"\n{'='*80}")
    print(f"Collection Summary:")
    print(f"  Files checked: {checked_files:,}")
    print(f"  Files with Elasticsearch: {processed_files}")
    print(f"  Files skipped (no Elasticsearch): {skipped_files:,}")
    print(f"  Total examples extracted: {len(all_examples)}")
    print(f"  Success rate: {(processed_files/checked_files*100):.2f}%" if checked_files > 0 else "  Success rate: 0%")
    print(f"{'='*80}")
    
    return all_examples


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Extract Elasticsearch code from the-stack (requires auth)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10000,
        help="Limit number of files WITH Elasticsearch code to process (default: 10000). Script will check up to 20x this limit to find matches."
    )
    parser.add_argument(
        "--max-check",
        type=int,
        default=None,
        help="Maximum number of files to check (default: 20x limit). Use to prevent checking too many files."
    )
    parser.add_argument(
        "--token",
        type=str,
        default=None,
        help="HuggingFace token (or use HF_TOKEN env var)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file path"
    )
    parser.add_argument(
        "--languages",
        nargs="+",
        default=ELASTICSEARCH_LANGUAGES,
        help=f"Languages to process (default: {', '.join(ELASTICSEARCH_LANGUAGES)})"
    )
    
    args = parser.parse_args()
    
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / "datasets" / "raw" / "the_stack_elasticsearch"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = (
        Path(args.output) if args.output
        else output_dir / "the_stack_elasticsearch.jsonl"
    )
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Load examples
    examples = load_the_stack_elasticsearch(
        limit=args.limit,
        token=args.token,
        languages=args.languages,
        max_check=args.max_check
    )
    
    if not examples:
        print("[ERROR] No examples to save")
        return
    
    # Save examples
    print(f"\nSaving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in tqdm(examples, desc="Writing"):
            json_line = json.dumps(example, ensure_ascii=False)
            f.write(json_line + '\n')
    
    # Save metadata
    metadata = {
        "source": "bigcode/the-stack",
        "total_examples": len(examples),
        "languages": args.languages,
        "task_distribution": {
            task: sum(1 for e in examples if e["task"] == task)
            for task in ["query_dsl", "mapping_create", "pipeline_create"]
        }
    }
    
    metadata_file = output_file.parent / "the_stack_elasticsearch_metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n[OK] Saved {len(examples):,} examples to {output_file}")
    print(f"     File size: {output_file.stat().st_size / 1024 / 1024:.1f} MB")
    print(f"     Metadata: {metadata_file}")


if __name__ == "__main__":
    main()

