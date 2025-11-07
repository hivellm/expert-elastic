#!/usr/bin/env python3
"""
Basic Expert Tests

Tests basic functionality of the expert-elastic model.
"""

import json
import pytest
from pathlib import Path

# Test data
TEST_QUERIES = [
    {
        "name": "Simple term query",
        "instruction": "Search for documents where status is 'active'.",
        "expected_contains": ["query", "term", "status"]
    },
    {
        "name": "Range query",
        "instruction": "Find documents from the last 30 days.",
        "expected_contains": ["query", "range", "gte"]
    },
    {
        "name": "KQL query",
        "instruction": "Detect process execution of regsvr32.exe.",
        "expected_contains": ["process.name", "regsvr32"]
    }
]


def test_manifest_exists():
    """Test that manifest.json exists and is valid"""
    manifest_path = Path(__file__).parent.parent / "manifest.json"
    assert manifest_path.exists(), "manifest.json not found"
    
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    
    # Check required fields
    assert "name" in manifest
    assert manifest["name"] == "expert-elastic"
    assert "version" in manifest
    assert "capabilities" in manifest
    assert "base_models" in manifest


def test_grammar_exists():
    """Test that grammar.gbnf exists"""
    grammar_path = Path(__file__).parent.parent / "grammar.gbnf"
    assert grammar_path.exists(), "grammar.gbnf not found"


def test_preprocess_script_exists():
    """Test that preprocess.py exists"""
    preprocess_path = Path(__file__).parent.parent / "preprocess.py"
    assert preprocess_path.exists(), "preprocess.py not found"


def test_collection_scripts_exist():
    """Test that all collection scripts exist"""
    scripts_dir = Path(__file__).parent.parent / "scripts"
    
    required_scripts = [
        "collect_ecs.py",
        "collect_integrations.py",
        "collect_kibana_samples.py",
        "collect_detection_rules.py",
        "collect_elastic_labs.py",
        "run_collection.py",
        "validate_dataset.py"
    ]
    
    for script in required_scripts:
        script_path = scripts_dir / script
        assert script_path.exists(), f"{script} not found"


def test_directory_structure():
    """Test that directory structure is correct"""
    base_dir = Path(__file__).parent.parent
    
    required_dirs = [
        "datasets/raw/ecs",
        "datasets/raw/integrations",
        "datasets/raw/kibana_samples",
        "datasets/raw/detection_rules",
        "datasets/raw/elastic_labs",
        "scripts",
        "tests"
    ]
    
    for dir_path in required_dirs:
        full_path = base_dir / dir_path
        assert full_path.exists(), f"Directory {dir_path} not found"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

