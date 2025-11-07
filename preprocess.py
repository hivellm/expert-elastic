#!/usr/bin/env python3
"""
Elasticsearch Dataset Preprocessing for expert-elastic

Processes multiple sources:
- ECS (Elastic Common Schema): field mappings
- Integrations: package fields and pipelines
- Kibana Samples: real-world queries and mappings
- Detection Rules: KQL/EQL queries
- Elastic Labs: NL→DSL examples

Features:
- ChatML formatting for Qwen3
- Multi-task support (mapping, query_dsl, kql, eql, pipeline)
- JSON validation
- Deduplication by task+input
- Multi-language support (PT/EN)

Usage:
    # Process all sources
    python preprocess.py --all
    
    # Process specific sources
    python preprocess.py --source ecs --source integrations
    
    # Custom output
    python preprocess.py --all --output datasets/processed
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from collections import defaultdict
import hashlib

# JSON validation
try:
    import json as json_validator
    JSON_VALIDATION_AVAILABLE = True
except ImportError:
    JSON_VALIDATION_AVAILABLE = False


def validate_json(text: str) -> bool:
    """Validate JSON syntax"""
    if not text or not text.strip():
        return False
    try:
        json_validator.loads(text)
        return True
    except Exception:
        return False


def format_chatml(
    task: str,
    instruction: str,
    output: str,
    domain: str = "",
    index: str = "",
    dialect: str = "elastic"
) -> str:
    """
    Format example with ChatML for Qwen3
    
    Args:
        task: mapping_create, query_dsl, kql, eql, pipeline_create
        instruction: User instruction in PT or EN
        output: Expected output (JSON, KQL, or EQL)
        domain: Optional domain context (e.g., 'ecs:nginx', 'security')
        index: Optional index name (e.g., 'kibana_sample_data_ecommerce')
    """
    system_content = f"Dialect: {dialect}\nTask: {task}"
    if domain:
        system_content += f"\nDomain: {domain}"
    if index:
        system_content += f"\nIndex: {index}"
    
    return (
        f"<|system|>\n{system_content}\n<|end|>\n"
        f"<|user|>\n{instruction}\n<|end|>\n"
        f"<|assistant|>\n{output}\n<|end|>"
    )


def deduplicate_key(task: str, instruction: str) -> str:
    """Generate deduplication key from task+instruction"""
    combined = f"{task}:{instruction.strip().lower()}"
    return hashlib.md5(combined.encode()).hexdigest()


def load_ecs_examples(raw_dir: Path) -> List[Dict[str, Any]]:
    """Load ECS mapping examples from raw/ecs/"""
    examples = []
    ecs_dir = raw_dir / "ecs"
    
    if not ecs_dir.exists():
        print(f"[ECS] Directory not found: {ecs_dir}")
        return examples
    
    # Load processed ECS examples
    for jsonl_file in ecs_dir.glob("*.jsonl"):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    example = json.loads(line)
                    examples.append(example)
                except Exception as e:
                    print(f"[ECS] Error loading {jsonl_file}: {e}")
    
    print(f"[ECS] Loaded {len(examples)} examples")
    return examples


def load_integration_examples(raw_dir: Path) -> List[Dict[str, Any]]:
    """Load integration mapping/pipeline examples from raw/integrations/"""
    examples = []
    integrations_dir = raw_dir / "integrations"
    
    if not integrations_dir.exists():
        print(f"[Integrations] Directory not found: {integrations_dir}")
        return examples
    
    for jsonl_file in integrations_dir.glob("*.jsonl"):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    example = json.loads(line)
                    examples.append(example)
                except Exception as e:
                    print(f"[Integrations] Error loading {jsonl_file}: {e}")
    
    print(f"[Integrations] Loaded {len(examples)} examples")
    return examples


def load_kibana_examples(raw_dir: Path) -> List[Dict[str, Any]]:
    """Load Kibana sample data examples from raw/kibana_samples/"""
    examples = []
    kibana_dir = raw_dir / "kibana_samples"
    
    if not kibana_dir.exists():
        print(f"[Kibana] Directory not found: {kibana_dir}")
        return examples
    
    for jsonl_file in kibana_dir.glob("*.jsonl"):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    example = json.loads(line)
                    examples.append(example)
                except Exception as e:
                    print(f"[Kibana] Error loading {jsonl_file}: {e}")
    
    print(f"[Kibana] Loaded {len(examples)} examples")
    return examples


def load_detection_rules(raw_dir: Path) -> List[Dict[str, Any]]:
    """Load detection rules (KQL/EQL) from raw/detection_rules/"""
    examples = []
    rules_dir = raw_dir / "detection_rules"
    
    if not rules_dir.exists():
        print(f"[Rules] Directory not found: {rules_dir}")
        return examples
    
    for jsonl_file in rules_dir.glob("*.jsonl"):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    example = json.loads(line)
                    examples.append(example)
                except Exception as e:
                    print(f"[Rules] Error loading {jsonl_file}: {e}")
    
    print(f"[Rules] Loaded {len(examples)} examples")
    return examples


def load_elastic_labs(raw_dir: Path) -> List[Dict[str, Any]]:
    """Load Elastic Labs NL→DSL examples from raw/elastic_labs/"""
    examples = []
    labs_dir = raw_dir / "elastic_labs"
    
    if not labs_dir.exists():
        print(f"[Labs] Directory not found: {labs_dir}")
        return examples
    
    for jsonl_file in labs_dir.glob("*.jsonl"):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    example = json.loads(line)
                    examples.append(example)
                except Exception as e:
                    print(f"[Labs] Error loading {jsonl_file}: {e}")
    
    print(f"[Labs] Loaded {len(examples)} examples")
    return examples


def load_elasticsearch_examples(raw_dir: Path) -> List[Dict[str, Any]]:
    """Load Elasticsearch official examples from raw/elasticsearch_examples/"""
    examples = []
    es_dir = raw_dir / "elasticsearch_examples"
    
    if not es_dir.exists():
        print(f"[Elasticsearch] Directory not found: {es_dir}")
        return examples
    
    for jsonl_file in es_dir.glob("*.jsonl"):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    example = json.loads(line)
                    examples.append(example)
                except Exception as e:
                    print(f"[Elasticsearch] Error loading {jsonl_file}: {e}")
    
    print(f"[Elasticsearch] Loaded {len(examples)} examples")
    return examples


def load_synthetic_kql_eql_pipelines(raw_dir: Path) -> List[Dict[str, Any]]:
    """Load synthetic KQL/EQL/Pipeline examples"""
    examples = []
    synth_dir = raw_dir / "synthetic_kql_eql_pipelines"
    
    if not synth_dir.exists():
        print(f"[Synthetic] Directory not found: {synth_dir}")
        return examples
    
    for jsonl_file in synth_dir.glob("*.jsonl"):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    example = json.loads(line)
                    examples.append(example)
                except Exception as e:
                    print(f"[Synthetic] Error loading {jsonl_file}: {e}")
    
    print(f"[Synthetic] Loaded {len(examples)} examples")
    return examples


def load_dsl_examples(raw_dir: Path) -> List[Dict[str, Any]]:
    """Load DSL query examples from raw/dsl_examples/"""
    examples = []
    dsl_dir = raw_dir / "dsl_examples"
    
    if not dsl_dir.exists():
        print(f"[DSL] Directory not found: {dsl_dir}")
        return examples
    
    for jsonl_file in dsl_dir.glob("*.jsonl"):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    example = json.loads(line)
                    examples.append(example)
                except Exception as e:
                    print(f"[DSL] Error loading {jsonl_file}: {e}")
    
    print(f"[DSL] Loaded {len(examples)} examples")
    return examples


def load_documentation_examples(raw_dir: Path) -> List[Dict[str, Any]]:
    """Load documentation examples from raw/documentation/"""
    examples = []
    doc_dir = raw_dir / "documentation"
    
    if not doc_dir.exists():
        print(f"[DOCUMENTATION] Directory not found: {doc_dir}")
        return examples
    
    for jsonl_file in doc_dir.glob("*.jsonl"):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    example = json.loads(line)
                    examples.append(example)
                except Exception as e:
                    print(f"[DOCUMENTATION] Error loading {jsonl_file}: {e}")
    
    print(f"[DOCUMENTATION] Loaded {len(examples)} examples")
    return examples


def load_the_stack_examples(raw_dir: Path) -> List[Dict[str, Any]]:
    """Load The Stack Elasticsearch examples from raw/the_stack_elasticsearch/
    
    Limited to 10,000 random samples to maintain quality and avoid dataset pollution.
    """
    import random
    
    examples = []
    stack_dir = raw_dir / "the_stack_elasticsearch"
    
    if not stack_dir.exists():
        print(f"[THE_STACK] Directory not found: {stack_dir}")
        return examples
    
    for jsonl_file in stack_dir.glob("*.jsonl"):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    example = json.loads(line)
                    examples.append(example)
                except Exception as e:
                    print(f"[THE_STACK] Error loading {jsonl_file}: {e}")
    
    # Limit to 10k random samples for quality
    total_loaded = len(examples)
    if total_loaded > 10000:
        examples = random.sample(examples, 10000)
        print(f"[THE_STACK] Limited to 10,000 random samples (from {total_loaded:,} total)")
    else:
        print(f"[THE_STACK] Loaded {total_loaded:,} examples")
    
    return examples


def load_complex_dsl_examples(raw_dir: Path) -> List[Dict[str, Any]]:
    """Load complex DSL query examples from raw/complex_dsl/"""
    examples = []
    complex_dsl_dir = raw_dir / "complex_dsl"
    
    if not complex_dsl_dir.exists():
        print(f"[Complex DSL] Directory not found: {complex_dsl_dir}")
        return examples
    
    for jsonl_file in complex_dsl_dir.glob("*.jsonl"):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    example = json.loads(line)
                    examples.append(example)
                except Exception as e:
                    print(f"[Complex DSL] Error loading {jsonl_file}: {e}")
    
    print(f"[Complex DSL] Loaded {len(examples)} examples")
    return examples


def process_dataset(
    sources: List[str],
    raw_dir: Path = Path("datasets/raw"),
    output_dir: Path = Path("datasets"),
    deduplicate: bool = True,
    validate: bool = True
) -> None:
    """
    Process dataset from multiple sources and save in expert format
    
    Args:
        sources: List of sources to process (ecs, integrations, kibana, rules, labs)
        raw_dir: Directory containing raw data
        output_dir: Output directory for processed dataset
        deduplicate: Whether to deduplicate examples
        validate: Whether to validate JSON outputs
    """
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load examples from all sources
    all_examples = []
    
    if "ecs" in sources or "all" in sources:
        all_examples.extend(load_ecs_examples(raw_dir))
    
    if "integrations" in sources or "all" in sources:
        all_examples.extend(load_integration_examples(raw_dir))
    
    if "kibana" in sources or "all" in sources:
        all_examples.extend(load_kibana_examples(raw_dir))
    
    if "rules" in sources or "all" in sources:
        all_examples.extend(load_detection_rules(raw_dir))
    
    if "labs" in sources or "all" in sources:
        all_examples.extend(load_elastic_labs(raw_dir))
    
    if "elasticsearch" in sources or "all" in sources:
        all_examples.extend(load_elasticsearch_examples(raw_dir))
    
    if "synthetic" in sources or "all" in sources:
        all_examples.extend(load_synthetic_kql_eql_pipelines(raw_dir))
    
    if "dsl" in sources or "all" in sources:
        all_examples.extend(load_dsl_examples(raw_dir))
    
    if "complex_dsl" in sources or "all" in sources:
        all_examples.extend(load_complex_dsl_examples(raw_dir))
    
    if "documentation" in sources or "all" in sources:
        all_examples.extend(load_documentation_examples(raw_dir))
    
    if "the_stack" in sources or "all" in sources:
        all_examples.extend(load_the_stack_examples(raw_dir))
    
    print(f"\n{'='*70}")
    print(f"Total raw examples loaded: {len(all_examples)}")
    print(f"{'='*70}\n")
    
    # Process examples
    processed = []
    seen_keys = set()
    stats = defaultdict(int)
    
    for idx, example in enumerate(all_examples):
        try:
            # Extract fields
            task = example.get("task", "")
            instruction = example.get("instruction", "")
            output = example.get("output", "")
            domain = example.get("domain", "")
            index = example.get("index", "")
            
            if not task or not instruction or not output:
                stats['missing_fields'] += 1
                continue
            
            # Filter out Portuguese instructions (common Portuguese words)
            portuguese_indicators = ["crie", "defina", "gere", "buscar", "encontrar", "detectar", 
                                    "criar", "definir", "gerar", "busque", "encontre", "detecte",
                                    "para o", "para a", "do serviço", "dos logs", "com os campos"]
            instruction_lower = instruction.lower()
            if any(pt_word in instruction_lower for pt_word in portuguese_indicators):
                stats['portuguese_filtered'] = stats.get('portuguese_filtered', 0) + 1
                continue
            
            # Validate JSON outputs (for mapping, query_dsl, pipeline tasks)
            if validate and task in ["mapping_create", "query_dsl", "pipeline_create"]:
                if not validate_json(output):
                    stats['invalid_json'] += 1
                    continue
            
            # Deduplicate
            if deduplicate:
                dedup_key = deduplicate_key(task, instruction)
                if dedup_key in seen_keys:
                    stats['duplicates'] += 1
                    continue
                seen_keys.add(dedup_key)
            
            # Format with ChatML
            text = format_chatml(task, instruction, output, domain, index)
            processed.append({"text": text})
            
            # Track stats by task
            stats[f'task_{task}'] += 1
            stats['processed'] += 1
            
            if (idx + 1) % 1000 == 0:
                print(f"Processed {idx + 1}/{len(all_examples)} examples...")
        
        except Exception as e:
            stats['errors'] += 1
            if stats['errors'] < 10:
                print(f"Error processing example {idx}: {e}")
    
    # Save processed dataset
    output_file = output_dir / "train.jsonl"
    print(f"\nSaving {len(processed)} examples to {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in processed:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    # Save metadata
    metadata = {
        "total_raw_examples": len(all_examples),
        "processed_examples": stats['processed'],
        "sources": sources,
        "skipped": {
            "missing_fields": stats['missing_fields'],
            "invalid_json": stats['invalid_json'],
            "duplicates": stats['duplicates'],
            "portuguese_filtered": stats.get('portuguese_filtered', 0),
            "errors": stats['errors']
        },
        "tasks": {
            "mapping_create": stats.get('task_mapping_create', 0),
            "query_dsl": stats.get('task_query_dsl', 0),
            "kql": stats.get('task_kql', 0),
            "eql": stats.get('task_eql', 0),
            "pipeline_create": stats.get('task_pipeline_create', 0)
        }
    }
    
    metadata_file = output_dir / "metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    # Print summary
    print("\n" + "="*70)
    print("PREPROCESSING SUMMARY")
    print("="*70)
    print(f"Total raw examples:     {len(all_examples)}")
    print(f"Processed:              {stats['processed']}")
    print(f"Missing fields:         {stats['missing_fields']}")
    if validate:
        print(f"Invalid JSON:           {stats['invalid_json']}")
    if deduplicate:
        print(f"Duplicates:             {stats['duplicates']}")
    if 'portuguese_filtered' in stats:
        print(f"Portuguese filtered:    {stats['portuguese_filtered']}")
    print(f"Errors:                 {stats['errors']}")
    print("\nTask distribution:")
    print(f"  - Mapping creation:   {stats.get('task_mapping_create', 0)}")
    print(f"  - Query DSL:          {stats.get('task_query_dsl', 0)}")
    print(f"  - KQL:                {stats.get('task_kql', 0)}")
    print(f"  - EQL:                {stats.get('task_eql', 0)}")
    print(f"  - Pipeline creation:  {stats.get('task_pipeline_create', 0)}")
    print(f"\nOutput: {output_file}")
    print(f"Stats:  {metadata_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Preprocess Elasticsearch datasets for expert-elastic"
    )
    
    parser.add_argument(
        "--source",
        type=str,
        action="append",
        choices=["ecs", "integrations", "kibana", "rules", "labs", "elasticsearch", "synthetic", "dsl", "complex_dsl", "all"],
        help="Sources to process (can be specified multiple times)"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all sources (shortcut for --source all)"
    )
    
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=Path("datasets/raw"),
        help="Directory containing raw data (default: datasets/raw)"
    )
    
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("datasets"),
        help="Output directory (default: datasets)"
    )
    
    parser.add_argument(
        "--no-deduplicate",
        action="store_true",
        help="Skip deduplication"
    )
    
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip JSON validation"
    )
    
    args = parser.parse_args()
    
    # Determine sources
    sources = args.source or []
    if args.all or not sources:
        sources = ["all"]
    
    print("="*70)
    print("Elasticsearch Dataset Preprocessing for expert-elastic")
    print("="*70)
    print(f"Sources: {', '.join(sources)}")
    print(f"Raw dir: {args.raw_dir}")
    print(f"Output: {args.output}")
    print(f"Deduplicate: {not args.no_deduplicate}")
    print(f"Validate JSON: {not args.no_validate}")
    print("="*70)
    print()
    
    process_dataset(
        sources=sources,
        raw_dir=args.raw_dir,
        output_dir=args.output,
        deduplicate=not args.no_deduplicate,
        validate=not args.no_validate
    )


if __name__ == "__main__":
    main()

