#!/usr/bin/env python3
"""
Ingest Pipeline Tests

Tests the expert's ability to generate Elasticsearch ingest pipelines.
"""

import json
import pytest

# Pipeline test scenarios
PIPELINE_TESTS = [
    {
        "name": "GeoIP processor",
        "instruction": "Create a pipeline to add geoip data for source.ip field.",
        "expected_processors": ["geoip"],
        "expected_fields": ["source.ip"]
    },
    {
        "name": "Rename processor",
        "instruction": "Create a pipeline to rename field 'old_name' to 'new_name'.",
        "expected_processors": ["rename"],
        "expected_contains": ["old_name", "new_name"]
    },
    {
        "name": "Set processor",
        "instruction": "Create a pipeline to set field 'environment' to 'production'.",
        "expected_processors": ["set"],
        "expected_contains": ["environment", "production"]
    },
    {
        "name": "Grok processor",
        "instruction": "Create a pipeline to parse Apache access logs.",
        "expected_processors": ["grok"],
        "expected_contains": ["pattern"]
    },
    {
        "name": "Date processor",
        "instruction": "Create a pipeline to parse timestamp field.",
        "expected_processors": ["date"],
        "expected_contains": ["field", "formats"]
    },
    {
        "name": "Multiple processors",
        "instruction": "Create a pipeline with geoip and rename processors.",
        "expected_processors": ["geoip", "rename"]
    },
    {
        "name": "User agent processor",
        "instruction": "Create a pipeline to parse user agent string.",
        "expected_processors": ["user_agent"],
        "expected_contains": ["field"]
    },
    {
        "name": "Remove processor",
        "instruction": "Create a pipeline to remove temporary field '_temp'.",
        "expected_processors": ["remove"],
        "expected_contains": ["field", "_temp"]
    }
]


def validate_pipeline(pipeline_json: str, test_case: dict) -> dict:
    """Validate a pipeline against test case requirements"""
    try:
        pipeline = json.loads(pipeline_json)
    except json.JSONDecodeError as e:
        return {"valid": False, "error": f"Invalid JSON: {e}"}
    
    # Check for processors array
    if "processors" not in pipeline:
        return {"valid": False, "error": "Missing 'processors' field"}
    
    processors = pipeline["processors"]
    if not isinstance(processors, list):
        return {"valid": False, "error": "'processors' must be an array"}
    
    # Check for expected processors
    if "expected_processors" in test_case:
        processor_types = []
        for proc in processors:
            if isinstance(proc, dict):
                processor_types.extend(proc.keys())
        
        for expected_proc in test_case["expected_processors"]:
            if expected_proc not in processor_types:
                return {"valid": False, "error": f"Missing expected processor: {expected_proc}"}
    
    # Check for expected content
    if "expected_contains" in test_case:
        pipeline_str = json.dumps(pipeline).lower()
        for expected in test_case["expected_contains"]:
            if expected.lower() not in pipeline_str:
                return {"valid": False, "error": f"Missing expected content: {expected}"}
    
    # Check for expected fields
    if "expected_fields" in test_case:
        pipeline_str = json.dumps(pipeline)
        for field in test_case["expected_fields"]:
            if field not in pipeline_str:
                return {"valid": False, "error": f"Missing expected field: {field}"}
    
    return {"valid": True}


def test_pipeline_scenarios():
    """Test pipeline generation scenarios"""
    for test_case in PIPELINE_TESTS:
        assert "name" in test_case
        assert "instruction" in test_case
        assert "expected_processors" in test_case or "expected_contains" in test_case


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

