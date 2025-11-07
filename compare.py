"""
Qualitative Checkpoint Comparison - Expert Elastic

This script runs the same prompts on all available checkpoints
and displays results for qualitative analysis by an external LLM.

Run with: F:/Node/hivellm/expert/cli/venv_windows/Scripts/python.exe compare.py
"""

import sys
import os

# Add experts root directory to path to import template
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))

# Import functions from template
from compare_checkpoints_template import (
    detect_device, find_checkpoints, load_base_model, load_checkpoints,
    generate_output, print_separator, print_test_header, print_output, main as template_main
)
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import json

# ============================================================================
# EXPERT-ELASTIC SPECIFIC CONFIGURATION
# ============================================================================

BASE_MODEL_PATH = "F:/Node/hivellm/expert/models/Qwen3-0.6B"
CHECKPOINT_DIR = "weights/qwen3-06b"

GEN_CONFIG = {
    "max_new_tokens": 200,
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 20,
    "do_sample": True,
}

# ============================================================================
# TEST CASES - EXPERT-ELASTIC
# ============================================================================

test_cases = [
    # Query DSL - Format: Dialect: elastic\nTask: query_dsl (matches training)
    {
        "id": "dsl_001",
        "category": "query_dsl",
        "system_prompt": "Dialect: elastic\nTask: query_dsl",
        "user_prompt": "Search for documents where status equals 'active'.",
        "expected_type": "json"
    },
    {
        "id": "dsl_002",
        "category": "query_dsl",
        "system_prompt": "Dialect: elastic\nTask: query_dsl",
        "user_prompt": "Find documents where message contains 'error'.",
        "expected_type": "json"
    },
    {
        "id": "dsl_003",
        "category": "query_dsl",
        "system_prompt": "Dialect: elastic\nTask: query_dsl",
        "user_prompt": "Search for documents where status is 'active' AND category is 'production'.",
        "expected_type": "json"
    },
    {
        "id": "dsl_004",
        "category": "query_dsl",
        "system_prompt": "Dialect: elastic\nTask: query_dsl",
        "user_prompt": "Get documents from the last 30 days.",
        "expected_type": "json"
    },
    {
        "id": "dsl_005",
        "category": "query_dsl",
        "system_prompt": "Dialect: elastic\nTask: query_dsl",
        "user_prompt": "Calculate the average response time.",
        "expected_type": "json"
    },
    # KQL - Format: Dialect: elastic\nTask: kql
    {
        "id": "kql_001",
        "category": "kql",
        "system_prompt": "Dialect: elastic\nTask: kql",
        "user_prompt": "Detect processes named regsvr32.exe.",
        "expected_type": "kql"
    },
    {
        "id": "kql_002",
        "category": "kql",
        "system_prompt": "Dialect: elastic\nTask: kql",
        "user_prompt": "Find events where event.category is 'process' AND event.type is 'start'.",
        "expected_type": "kql"
    },
    {
        "id": "kql_003",
        "category": "kql",
        "system_prompt": "Dialect: elastic\nTask: kql",
        "user_prompt": "Detect cmd.exe OR powershell.exe execution.",
        "expected_type": "kql"
    },
    # EQL - Format: Dialect: elastic\nTask: eql
    {
        "id": "eql_001",
        "category": "eql",
        "system_prompt": "Dialect: elastic\nTask: eql",
        "user_prompt": "Detect process creation events.",
        "expected_type": "eql"
    },
    {
        "id": "eql_002",
        "category": "eql",
        "system_prompt": "Dialect: elastic\nTask: eql",
        "user_prompt": "Detect network event followed by process creation by same user within 5 minutes.",
        "expected_type": "eql"
    },
    # Mappings - Format: Dialect: elastic\nTask: mapping_create
    {
        "id": "mapping_001",
        "category": "mapping_create",
        "system_prompt": "Dialect: elastic\nTask: mapping_create",
        "user_prompt": "Create an ECS mapping for nginx logs with fields client.ip, url.original, and http.response.status_code.",
        "expected_type": "json"
    },
    {
        "id": "mapping_002",
        "category": "mapping_create",
        "system_prompt": "Dialect: elastic\nTask: mapping_create",
        "user_prompt": "Create a mapping with keyword field 'status' and date field 'timestamp'.",
        "expected_type": "json"
    },
    # Pipelines - Format: Dialect: elastic\nTask: pipeline_create
    {
        "id": "pipeline_001",
        "category": "pipeline_create",
        "system_prompt": "Dialect: elastic\nTask: pipeline_create",
        "user_prompt": "Create a pipeline to add geoip data for source.ip field.",
        "expected_type": "json"
    },
    {
        "id": "pipeline_002",
        "category": "pipeline_create",
        "system_prompt": "Dialect: elastic\nTask: pipeline_create",
        "user_prompt": "Create a pipeline to rename field 'old_name' to 'new_name'.",
        "expected_type": "json"
    }
]

# ============================================================================
# MAIN CODE
# ============================================================================

def main():
    """Main function"""
    device = detect_device()
    
    print_separator()
    print("QUALITATIVE CHECKPOINT COMPARISON - EXPERT ELASTIC")
    print("This script generates outputs for external LLM analysis")
    print("Does not evaluate quality automatically")
    print_separator()
    
    # Find checkpoints
    checkpoints = find_checkpoints(CHECKPOINT_DIR)
    if not checkpoints:
        print(f"ERROR: No checkpoints found in: {CHECKPOINT_DIR}")
        sys.exit(1)
    
    print(f"\nCheckpoints found: {[c[0] for c in checkpoints]}")
    print(f"Total tests: {len(test_cases)}")
    print(f"Device: {device}")
    
    # Load models
    base_model, tokenizer = load_base_model(BASE_MODEL_PATH, device)
    checkpoint_models = load_checkpoints(BASE_MODEL_PATH, checkpoints, device)
    
    # Run tests
    print(f"\n[3/3] Running {len(test_cases)} tests...")
    print_separator()
    
    results = []
    
    for test_idx, test_case in enumerate(test_cases, 1):
        print_test_header(test_case, test_idx, len(test_cases))
        
        # Generate with base model
        base_output = generate_output(
            base_model, tokenizer,
            test_case['system_prompt'],
            test_case['user_prompt'],
            GEN_CONFIG,
            device
        )
        print_output("BASE MODEL", base_output)
        
        # Generate with each checkpoint
        checkpoint_outputs = {}
        for step, model in checkpoint_models.items():
            ckp_output = generate_output(
                model, tokenizer,
                test_case['system_prompt'],
                test_case['user_prompt'],
                GEN_CONFIG,
                device
            )
            checkpoint_outputs[step] = ckp_output
            print_output(f"CHECKPOINT-{step}", ckp_output)
        
        # Store result
        results.append({
            "test_id": test_case.get('id', f'test_{test_idx}'),
            "category": test_case.get('category', 'N/A'),
            "expected_type": test_case.get('expected_type', 'N/A'),
            "system_prompt": test_case['system_prompt'],
            "user_prompt": test_case['user_prompt'],
            "base_output": base_output,
            "checkpoint_outputs": checkpoint_outputs
        })
        
        print_separator()
    
    # Final summary
    print_separator()
    print("\nEXECUTION SUMMARY")
    print_separator()
    print(f"Total tests executed: {len(test_cases)}")
    print(f"Checkpoints tested: {[c[0] for c in checkpoints]}")
    print(f"Base model: {BASE_MODEL_PATH}")
    print(f"\nAll outputs have been displayed above.")
    print("\n" + "="*80)
    print("INSTRUCTIONS FOR LLM ANALYSIS:")
    print("="*80)
    print("Analyze the results above to determine:")
    print("  1. Which checkpoint produces best quality outputs")
    print("  2. Which checkpoint should be used to generate the package")
    print("  3. If training is progressing correctly")
    print("  4. Identify common issues (syntax, structure, completeness)")
    print("  5. Compare evolution between checkpoints")
    print("="*80)
    
    # Save results to JSON for later analysis
    output_file = "checkpoint_comparison_results.json"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "expert": "expert-elastic",
                "base_model": BASE_MODEL_PATH,
                "checkpoints_tested": [c[0] for c in checkpoints],
                "device": device,
                "test_config": GEN_CONFIG,
                "results": results
            }, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to: {output_file}")
    except Exception as e:
        print(f"\nWarning: Could not save results to JSON: {e}")

if __name__ == "__main__":
    main()

