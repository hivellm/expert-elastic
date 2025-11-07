#!/usr/bin/env python3
"""
Mapping Creation Tests

Tests the expert's ability to generate Elasticsearch mappings.
"""

import json
import pytest

# Test scenarios for mapping creation
MAPPING_TESTS = [
    {
        "name": "ECS mapping - basic fields",
        "instruction": "Create an ECS mapping for nginx logs with fields client.ip, url.original, and http.response.status_code.",
        "required_fields": ["client.ip", "url.original", "http.response.status_code"],
        "required_types": {"client.ip": "ip", "url.original": "keyword", "http.response.status_code": "long"}
    },
    {
        "name": "Integration mapping - apache",
        "instruction": "Generate an index template for apache logs.",
        "expected_contains": ["index_patterns", "template", "mappings"]
    },
    {
        "name": "Simple keyword field",
        "instruction": "Create a mapping with a keyword field named 'status'.",
        "required_fields": ["status"],
        "required_types": {"status": "keyword"}
    },
    {
        "name": "Date field",
        "instruction": "Create a mapping with a date field named 'timestamp'.",
        "required_fields": ["timestamp"],
        "required_types": {"timestamp": "date"}
    },
    {
        "name": "IP address field",
        "instruction": "Create a mapping for an IP field named 'client_ip'.",
        "required_fields": ["client_ip"],
        "required_types": {"client_ip": "ip"}
    },
    {
        "name": "Nested object",
        "instruction": "Create a mapping with nested fields user.name and user.email.",
        "required_fields": ["user.name", "user.email"]
    },
    {
        "name": "Multiple field types",
        "instruction": "Create a mapping with keyword field 'id', text field 'message', and long field 'count'.",
        "required_fields": ["id", "message", "count"],
        "required_types": {"id": "keyword", "message": "text", "count": "long"}
    },
    {
        "name": "Index template with settings",
        "instruction": "Generate an index template for logs with 1 shard and 1 replica.",
        "expected_contains": ["index_patterns", "settings", "number_of_shards", "mappings"]
    },
    {
        "name": "Geo point field",
        "instruction": "Create a mapping with a geo_point field named 'location'.",
        "required_fields": ["location"],
        "required_types": {"location": "geo_point"}
    },
    {
        "name": "Boolean field",
        "instruction": "Create a mapping with a boolean field named 'is_active'.",
        "required_fields": ["is_active"],
        "required_types": {"is_active": "boolean"}
    }
]


def validate_mapping(mapping_json: str, test_case: dict) -> dict:
    """Validate a mapping against test case requirements"""
    try:
        mapping = json.loads(mapping_json)
    except json.JSONDecodeError as e:
        return {"valid": False, "error": f"Invalid JSON: {e}"}
    
    # Check for expected content
    if "expected_contains" in test_case:
        mapping_str = json.dumps(mapping).lower()
        for expected in test_case["expected_contains"]:
            if expected.lower() not in mapping_str:
                return {"valid": False, "error": f"Missing expected content: {expected}"}
    
    # Check for required fields
    if "required_fields" in test_case:
        # Extract properties (may be nested)
        def find_field(obj, field_path):
            """Find a field in nested properties"""
            parts = field_path.split(".")
            current = obj
            
            # Navigate through template structure
            if "template" in current and "mappings" in current["template"]:
                current = current["template"]["mappings"]
            elif "mappings" in current:
                current = current["mappings"]
            
            if "properties" in current:
                current = current["properties"]
            
            for part in parts:
                if part not in current:
                    return None
                current = current[part]
                if "properties" in current:
                    current = current["properties"]
            
            return current
        
        for field in test_case["required_fields"]:
            field_def = find_field(mapping, field)
            if field_def is None:
                return {"valid": False, "error": f"Missing required field: {field}"}
            
            # Check field type if specified
            if "required_types" in test_case and field in test_case["required_types"]:
                expected_type = test_case["required_types"][field]
                actual_type = field_def.get("type")
                if actual_type != expected_type:
                    return {"valid": False, "error": f"Field {field} has type {actual_type}, expected {expected_type}"}
    
    return {"valid": True}


def test_mapping_scenarios():
    """Test mapping generation scenarios"""
    # Note: This test requires a trained model
    # For now, we just validate the test structure
    for test_case in MAPPING_TESTS:
        assert "name" in test_case
        assert "instruction" in test_case
        assert "required_fields" in test_case or "expected_contains" in test_case


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

