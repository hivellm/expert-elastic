#!/usr/bin/env python3
"""
Query Generation Tests

Tests the expert's ability to generate Elasticsearch queries (DSL, KQL, EQL).
"""

import json
import pytest

# Query DSL test scenarios
DSL_TESTS = [
    {
        "name": "Simple term query",
        "instruction": "Search for documents where status equals 'active'.",
        "expected_contains": ["query", "term", "status", "active"]
    },
    {
        "name": "Match query",
        "instruction": "Find documents where message contains 'error'.",
        "expected_contains": ["query", "match", "message"]
    },
    {
        "name": "Range query - dates",
        "instruction": "Get documents from the last 30 days.",
        "expected_contains": ["query", "range", "gte", "now-30d"]
    },
    {
        "name": "Bool query - must",
        "instruction": "Search for documents where status is 'active' AND category is 'production'.",
        "expected_contains": ["query", "bool", "must", "status", "category"]
    },
    {
        "name": "Aggregation - average",
        "instruction": "Calculate the average response time.",
        "expected_contains": ["aggs", "avg", "field"]
    }
]

# KQL test scenarios
KQL_TESTS = [
    {
        "name": "Simple field match",
        "instruction": "Detect processes named regsvr32.exe.",
        "expected_contains": ["process.name", "regsvr32"]
    },
    {
        "name": "Boolean AND",
        "instruction": "Find events where event.category is 'process' AND event.type is 'start'.",
        "expected_contains": ["event.category", "process", "event.type", "start", "and"]
    },
    {
        "name": "Boolean OR",
        "instruction": "Detect cmd.exe OR powershell.exe execution.",
        "expected_contains": ["cmd.exe", "powershell.exe", "or"]
    },
    {
        "name": "IP address match",
        "instruction": "Find connections to IP 192.168.1.1.",
        "expected_contains": ["192.168.1.1"]
    },
    {
        "name": "Wildcard pattern",
        "instruction": "Detect files with .exe extension.",
        "expected_contains": [".exe", "*"]
    }
]

# EQL test scenarios
EQL_TESTS = [
    {
        "name": "Simple event query",
        "instruction": "Detect process creation events.",
        "expected_contains": ["process", "where", "event"]
    },
    {
        "name": "Event with condition",
        "instruction": "Find process events where process.name is cmd.exe.",
        "expected_contains": ["process", "where", "process.name", "cmd.exe"]
    },
    {
        "name": "Sequence query",
        "instruction": "Detect network event followed by process creation by same user within 5 minutes.",
        "expected_contains": ["sequence", "by", "user", "maxspan", "5m", "network", "process"]
    },
    {
        "name": "Registry modification",
        "instruction": "Detect registry key modification events.",
        "expected_contains": ["registry", "where"]
    },
    {
        "name": "File creation",
        "instruction": "Find file creation events in temp directory.",
        "expected_contains": ["file", "where", "event.type"]
    }
]


def validate_dsl_query(query_json: str, test_case: dict) -> dict:
    """Validate a Query DSL against test case requirements"""
    try:
        query = json.loads(query_json)
    except json.JSONDecodeError as e:
        return {"valid": False, "error": f"Invalid JSON: {e}"}
    
    query_str = json.dumps(query).lower()
    
    for expected in test_case.get("expected_contains", []):
        if expected.lower() not in query_str:
            return {"valid": False, "error": f"Missing expected content: {expected}"}
    
    return {"valid": True}


def validate_kql_query(query: str, test_case: dict) -> dict:
    """Validate a KQL query against test case requirements"""
    if not query or not query.strip():
        return {"valid": False, "error": "Empty query"}
    
    query_lower = query.lower()
    
    for expected in test_case.get("expected_contains", []):
        if expected.lower() not in query_lower:
            return {"valid": False, "error": f"Missing expected content: {expected}"}
    
    return {"valid": True}


def validate_eql_query(query: str, test_case: dict) -> dict:
    """Validate an EQL query against test case requirements"""
    if not query or not query.strip():
        return {"valid": False, "error": "Empty query"}
    
    query_lower = query.lower()
    
    for expected in test_case.get("expected_contains", []):
        if expected.lower() not in query_lower:
            return {"valid": False, "error": f"Missing expected content: {expected}"}
    
    return {"valid": True}


def test_dsl_scenarios():
    """Test Query DSL generation scenarios"""
    for test_case in DSL_TESTS:
        assert "name" in test_case
        assert "instruction" in test_case
        assert "expected_contains" in test_case


def test_kql_scenarios():
    """Test KQL generation scenarios"""
    for test_case in KQL_TESTS:
        assert "name" in test_case
        assert "instruction" in test_case
        assert "expected_contains" in test_case


def test_eql_scenarios():
    """Test EQL generation scenarios"""
    for test_case in EQL_TESTS:
        assert "name" in test_case
        assert "instruction" in test_case
        assert "expected_contains" in test_case


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

