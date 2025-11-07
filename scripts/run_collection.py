#!/usr/bin/env python3
"""
Collection Orchestrator

Runs all collection scripts in sequence to build the complete dataset.

Usage:
    python run_collection.py --all
    python run_collection.py --source ecs --source kibana
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Collection scripts
COLLECTORS = {
    "ecs": {
        "script": "collect_ecs.py",
        "description": "ECS (Elastic Common Schema) mappings",
        "estimated": "5-8k examples"
    },
    "integrations": {
        "script": "collect_integrations.py",
        "description": "Elastic integrations (mappings + pipelines)",
        "estimated": "10-15k examples"
    },
    "kibana": {
        "script": "collect_kibana_samples.py",
        "description": "Kibana sample data (queries + mappings)",
        "estimated": "3-5k examples"
    },
    "rules": {
        "script": "collect_detection_rules.py",
        "description": "Detection rules (KQL + EQL)",
        "estimated": "2-3k examples"
    },
    "labs": {
        "script": "collect_elastic_labs.py",
        "description": "Elastic Labs NL to DSL examples",
        "estimated": "5-6k examples"
    },
    "elasticsearch": {
        "script": "collect_elasticsearch_examples.py",
        "description": "Elasticsearch official examples",
        "estimated": "500-1k examples"
    },
    "documentation": {
        "script": "collect_documentation.py",
        "description": "Elasticsearch official documentation (NEW)",
        "estimated": "2-3k examples"
    },
    "the_stack": {
        "script": "collect_the_stack_elasticsearch.py",
        "description": "The Stack - Real-world Elasticsearch code (NEW)",
        "estimated": "10-25k examples",
        "requires_auth": True
    },
    "synthetic": {
        "script": "generate_kql_eql_pipelines.py",
        "description": "Synthetic KQL/EQL/Pipeline examples",
        "estimated": "4-5k examples"
    },
    "dsl": {
        "script": "generate_dsl_examples.py",
        "description": "Large-scale DSL query examples",
        "estimated": "10k+ examples"
    }
}


def run_collector(name: str, script: str):
    """Run a collection script"""
    print(f"\n{'='*70}")
    print(f"Running: {name}")
    print(f"{'='*70}")
    
    script_path = Path(__file__).parent / script
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=False,
            text=True,
            check=True
        )
        
        print(f"\n[OK] {name} completed successfully")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] {name} failed with exit code {e.returncode}")
        return False
    
    except Exception as e:
        print(f"\n[ERROR] {name} failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Run data collection scripts for expert-elastic"
    )
    
    parser.add_argument(
        "--source",
        type=str,
        action="append",
        choices=list(COLLECTORS.keys()) + ["all"],
        help="Sources to collect (can be specified multiple times)"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Collect from all sources"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available collectors and exit"
    )
    
    args = parser.parse_args()
    
    # List collectors
    if args.list:
        print("\nAvailable collectors:")
        print("="*70)
        for name, info in COLLECTORS.items():
            print(f"\n{name}:")
            print(f"  Description: {info['description']}")
            print(f"  Estimated:   {info['estimated']}")
            print(f"  Script:      {info['script']}")
        print()
        return
    
    # Determine sources
    sources = args.source or []
    if args.all or "all" in sources or not sources:
        sources = list(COLLECTORS.keys())
    elif args.source:
        sources = [s for s in args.source if s != "all"]
    
    # Print plan
    print("="*70)
    print("Expert-Elastic Data Collection")
    print("="*70)
    print(f"\nSources to collect: {', '.join(sources)}")
    print(f"Total collectors: {len(sources)}")
    print()
    
    for source in sources:
        if source in COLLECTORS:
            info = COLLECTORS[source]
            print(f"  - {source}: {info['description']} ({info['estimated']})")
    
    print("\n" + "="*70)
    print("Starting collection...")
    print()
    
    # Run collectors
    results = {}
    
    for source in sources:
        if source not in COLLECTORS:
            print(f"[SKIP] Unknown source: {source}")
            continue
        
        info = COLLECTORS[source]
        success = run_collector(source, info["script"])
        results[source] = success
    
    # Print summary
    print("\n" + "="*70)
    print("COLLECTION SUMMARY")
    print("="*70)
    
    successful = [name for name, status in results.items() if status]
    failed = [name for name, status in results.items() if not status]
    
    print(f"\nSuccessful: {len(successful)}/{len(results)}")
    for name in successful:
        print(f"  ✓ {name}")
    
    if failed:
        print(f"\nFailed: {len(failed)}/{len(results)}")
        for name in failed:
            print(f"  ✗ {name}")
    
    print("\n" + "="*70)
    print("Next steps:")
    print("  1. Run preprocessing: python preprocess.py --all")
    print("  2. Validate dataset: python scripts/validate_dataset.py")
    print("  3. Train expert: expert-cli train")
    print("="*70)


if __name__ == "__main__":
    main()

