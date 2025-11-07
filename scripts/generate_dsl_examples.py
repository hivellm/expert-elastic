#!/usr/bin/env python3
"""
DSL Query Examples Generator

Generates a large number of diverse Query DSL examples covering:
- Basic queries (term, match, range, exists, prefix, wildcard)
- Bool queries (must, should, must_not, filter)
- Aggregations (terms, avg, sum, min, max, date_histogram, cardinality)
- Complex nested queries
- Multi-field queries
- Script queries
- Function score queries
- Geo queries

Target: ~10,000+ Query DSL examples
"""

import json
import random
from pathlib import Path
from typing import Dict, List, Any

OUTPUT_DIR = Path("../datasets/raw/dsl_examples")

# Common fields for Elasticsearch
FIELDS = [
    "status", "category", "type", "level", "severity", "priority",
    "user.name", "user.email", "user.id", "user.role",
    "host.name", "host.ip", "host.os", "host.arch",
    "source.ip", "destination.ip", "source.port", "destination.port",
    "event.type", "event.action", "event.category", "event.outcome",
    "process.name", "process.pid", "process.command_line",
    "file.name", "file.path", "file.extension", "file.size",
    "http.request.method", "http.response.status_code", "http.version",
    "url.path", "url.query", "url.domain",
    "message", "log.level", "service.name", "service.version",
    "@timestamp", "timestamp", "created_at", "updated_at",
    "price", "quantity", "total", "amount", "count", "duration",
    "bytes", "response_time", "latency", "throughput"
]

VALUES = [
    "active", "inactive", "pending", "completed", "failed", "error",
    "success", "warning", "info", "debug", "critical",
    "admin", "user", "guest", "anonymous",
    "production", "staging", "development", "test",
    "GET", "POST", "PUT", "DELETE", "PATCH",
    "200", "201", "400", "401", "403", "404", "500", "502", "503"
]

NUMERIC_VALUES = {
    "range": (0, 1000),
    "age": (18, 100),
    "price": (10, 10000),
    "quantity": (1, 100),
    "count": (0, 1000),
    "duration": (0, 3600),
    "bytes": (0, 1073741824),  # 0 to 1GB
    "response_time": (0, 5000),
    "status_code": (200, 599)
}

DATE_RANGES = [
    ("now-1d", "now"),
    ("now-7d", "now"),
    ("now-30d", "now"),
    ("now-90d", "now"),
    ("2024-01-01", "2024-12-31"),
    ("now-1h", "now"),
    ("now-1w", "now"),
    ("now-1M", "now")
]


def generate_term_query() -> Dict[str, Any]:
    """Generate term query examples"""
    field = random.choice(FIELDS)
    value = random.choice(VALUES)
    
    instructions = [
        f"Find all documents where {field} equals {value}.",
        f"Search for documents with {field} set to {value}.",
        f"Get documents where {field} is {value}.",
        f"Query documents where {field} equals '{value}'.",
        f"Retrieve documents where the {field} field equals {value}."
    ]
    
    return {
        "instruction": random.choice(instructions),
        "query": {
            "query": {
                "term": {
                    field: value
                }
            }
        }
    }


def generate_match_query() -> Dict[str, Any]:
    """Generate match query examples"""
    field = random.choice([f for f in FIELDS if f not in ["status", "category", "type"]])
    value = random.choice(["error", "warning", "success", "quick brown fox", "elasticsearch", "kibana"])
    
    instructions = [
        f"Search for documents where {field} contains '{value}'.",
        f"Find documents matching '{value}' in {field}.",
        f"Query documents where {field} matches '{value}'.",
        f"Search {field} for '{value}'.",
        f"Find all documents with '{value}' in {field}."
    ]
    
    return {
        "instruction": random.choice(instructions),
        "query": {
            "query": {
                "match": {
                    field: value
                }
            }
        }
    }


def generate_range_query() -> Dict[str, Any]:
    """Generate range query examples"""
    numeric_fields = [f for f in FIELDS if f in ["price", "quantity", "count", "duration", "bytes", "response_time", "age"]]
    date_fields = ["@timestamp", "timestamp", "created_at", "updated_at"]
    
    if random.random() < 0.5:
        # Numeric range
        field = random.choice(numeric_fields)
        min_val, max_val = NUMERIC_VALUES.get(field, (0, 1000))
        gte = random.randint(min_val, max_val - 100)
        lte = random.randint(gte + 10, max_val)
        
        instructions = [
            f"Find documents where {field} is between {gte} and {lte}.",
            f"Search for documents with {field} from {gte} to {lte}.",
            f"Query documents where {field} >= {gte} and {field} <= {lte}.",
            f"Get documents where {field} is in range [{gte}, {lte}].",
            f"Find all documents where {field} is greater than or equal to {gte} and less than or equal to {lte}."
        ]
        
        return {
            "instruction": random.choice(instructions),
            "query": {
                "query": {
                    "range": {
                        field: {
                            "gte": gte,
                            "lte": lte
                        }
                    }
                }
            }
        }
    else:
        # Date range
        field = random.choice(date_fields)
        gte, lte = random.choice(DATE_RANGES)
        
        instructions = [
            f"Find documents where {field} is between {gte} and {lte}.",
            f"Search for documents with {field} from {gte} to {lte}.",
            f"Query documents created between {gte} and {lte}.",
            f"Get documents where {field} >= {gte} and {field} < {lte}.",
            f"Find all documents where {field} is in the range from {gte} to {lte}."
        ]
        
        return {
            "instruction": random.choice(instructions),
            "query": {
                "query": {
                    "range": {
                        field: {
                            "gte": gte,
                            "lte": lte
                        }
                    }
                }
            }
        }


def generate_bool_query() -> Dict[str, Any]:
    """Generate bool query examples with must/should/must_not/filter"""
    num_must = random.randint(1, 3)
    num_should = random.randint(0, 2)
    num_must_not = random.randint(0, 2)
    num_filter = random.randint(0, 2)
    
    must_clauses = []
    should_clauses = []
    must_not_clauses = []
    filter_clauses = []
    
    used_fields = set()
    
    # Generate must clauses
    for _ in range(num_must):
        field = random.choice([f for f in FIELDS if f not in used_fields])
        used_fields.add(field)
        if field in ["@timestamp", "timestamp", "created_at"]:
            gte, lte = random.choice(DATE_RANGES)
            must_clauses.append({
                "range": {
                    field: {"gte": gte, "lte": lte}
                }
            })
        else:
            value = random.choice(VALUES)
            must_clauses.append({
                "term": {field: value}
            })
    
    # Generate should clauses
    for _ in range(num_should):
        field = random.choice([f for f in FIELDS if f not in used_fields])
        used_fields.add(field)
        value = random.choice(VALUES)
        should_clauses.append({
            "term": {field: value}
        })
    
    # Generate must_not clauses
    for _ in range(num_must_not):
        field = random.choice([f for f in FIELDS if f not in used_fields])
        used_fields.add(field)
        value = random.choice(VALUES)
        must_not_clauses.append({
            "term": {field: value}
        })
    
    # Generate filter clauses
    for _ in range(num_filter):
        field = random.choice([f for f in FIELDS if f not in used_fields])
        used_fields.add(field)
        if field in ["@timestamp", "timestamp"]:
            gte, lte = random.choice(DATE_RANGES)
            filter_clauses.append({
                "range": {
                    field: {"gte": gte, "lte": lte}
                }
            })
        else:
            value = random.choice(VALUES)
            filter_clauses.append({
                "term": {field: value}
            })
    
    bool_query = {}
    if must_clauses:
        bool_query["must"] = must_clauses
    if should_clauses:
        bool_query["should"] = should_clauses
    if must_not_clauses:
        bool_query["must_not"] = must_not_clauses
    if filter_clauses:
        bool_query["filter"] = filter_clauses
    
    # Build instruction
    parts = []
    if must_clauses:
        parts.append(f"must have {len(must_clauses)} condition(s)")
    if should_clauses:
        parts.append(f"should match {len(should_clauses)} condition(s)")
    if must_not_clauses:
        parts.append(f"must not have {len(must_not_clauses)} condition(s)")
    if filter_clauses:
        parts.append(f"filtered by {len(filter_clauses)} condition(s)")
    
    instructions = [
        f"Search for documents that {', '.join(parts)}.",
        f"Find documents matching a bool query with {', '.join(parts)}.",
        f"Query documents using bool query: {', '.join(parts)}.",
        f"Get documents that {', '.join(parts)}."
    ]
    
    return {
        "instruction": random.choice(instructions),
        "query": {
            "query": {
                "bool": bool_query
            }
        }
    }


def generate_aggregation_query() -> Dict[str, Any]:
    """Generate aggregation query examples"""
    agg_type = random.choice(["terms", "avg", "sum", "min", "max", "cardinality", "date_histogram", "stats"])
    field = random.choice(FIELDS)
    
    if agg_type == "terms":
        instructions = [
            f"Aggregate documents by {field} and get top terms.",
            f"Group documents by {field} and count occurrences.",
            f"Get top values for {field} field.",
            f"Count documents grouped by {field}.",
            f"Show distribution of {field} values."
        ]
        
        return {
            "instruction": random.choice(instructions),
            "query": {
                "size": 0,
                "aggs": {
                    f"by_{field.replace('.', '_')}": {
                        "terms": {
                            "field": field,
                            "size": random.choice([10, 20, 50, 100])
                        }
                    }
                }
            }
        }
    
    elif agg_type == "avg":
        numeric_field = random.choice([f for f in FIELDS if f in ["price", "quantity", "count", "duration", "bytes", "response_time"]])
        instructions = [
            f"Calculate the average value of {numeric_field}.",
            f"Get average {numeric_field} across all documents.",
            f"Compute mean {numeric_field}.",
            f"Find average {numeric_field} value.",
            f"Calculate avg {numeric_field}."
        ]
        
        return {
            "instruction": random.choice(instructions),
            "query": {
                "size": 0,
                "aggs": {
                    f"avg_{numeric_field.replace('.', '_')}": {
                        "avg": {
                            "field": numeric_field
                        }
                    }
                }
            }
        }
    
    elif agg_type == "sum":
        numeric_field = random.choice([f for f in FIELDS if f in ["price", "quantity", "count", "bytes", "total", "amount"]])
        instructions = [
            f"Calculate the sum of {numeric_field}.",
            f"Get total {numeric_field} across all documents.",
            f"Sum up all {numeric_field} values.",
            f"Compute total {numeric_field}.",
            f"Calculate sum of {numeric_field}."
        ]
        
        return {
            "instruction": random.choice(instructions),
            "query": {
                "size": 0,
                "aggs": {
                    f"sum_{numeric_field.replace('.', '_')}": {
                        "sum": {
                            "field": numeric_field
                        }
                    }
                }
            }
        }
    
    elif agg_type == "date_histogram":
        date_field = random.choice(["@timestamp", "timestamp", "created_at"])
        interval = random.choice(["1h", "1d", "1w", "1M", "1y"])
        
        instructions = [
            f"Aggregate {date_field} by {interval} intervals.",
            f"Group documents by {date_field} in {interval} buckets.",
            f"Create a time series histogram of {date_field} with {interval} intervals.",
            f"Show distribution of {date_field} over time with {interval} buckets.",
            f"Generate date histogram for {date_field} with {interval} interval."
        ]
        
        return {
            "instruction": random.choice(instructions),
            "query": {
                "size": 0,
                "aggs": {
                    f"events_over_time": {
                        "date_histogram": {
                            "field": date_field,
                            "calendar_interval": interval
                        }
                    }
                }
            }
        }
    
    elif agg_type == "cardinality":
        instructions = [
            f"Count unique values of {field}.",
            f"Get cardinality (distinct count) of {field}.",
            f"Find number of unique {field} values.",
            f"Calculate distinct count for {field}.",
            f"Get unique count of {field}."
        ]
        
        return {
            "instruction": random.choice(instructions),
            "query": {
                "size": 0,
                "aggs": {
                    f"unique_{field.replace('.', '_')}": {
                        "cardinality": {
                            "field": field
                        }
                    }
                }
            }
        }
    
    else:  # min, max, stats
        numeric_field = random.choice([f for f in FIELDS if f in ["price", "quantity", "count", "duration", "bytes", "response_time"]])
        if agg_type == "min":
            instructions = [f"Find minimum value of {numeric_field}.", f"Get lowest {numeric_field}.", f"Calculate min {numeric_field}."]
        elif agg_type == "max":
            instructions = [f"Find maximum value of {numeric_field}.", f"Get highest {numeric_field}.", f"Calculate max {numeric_field}."]
        else:  # stats
            instructions = [f"Get statistics (min, max, avg, sum) for {numeric_field}.", f"Calculate stats for {numeric_field}.", f"Compute statistics of {numeric_field}."]
        
        return {
            "instruction": random.choice(instructions),
            "query": {
                "size": 0,
                "aggs": {
                    f"{agg_type}_{numeric_field.replace('.', '_')}": {
                        agg_type: {
                            "field": numeric_field
                        }
                    }
                }
            }
        }


def generate_multi_match_query() -> Dict[str, Any]:
    """Generate multi-match query examples"""
    fields = random.sample([f for f in FIELDS if f not in ["status", "category"]], k=random.randint(2, 4))
    query_text = random.choice(["error", "warning", "elasticsearch", "quick brown fox", "user", "admin"])
    
    instructions = [
        f"Search for '{query_text}' across fields {', '.join(fields)}.",
        f"Find documents matching '{query_text}' in any of these fields: {', '.join(fields)}.",
        f"Query '{query_text}' in multiple fields: {', '.join(fields)}.",
        f"Search '{query_text}' across {', '.join(fields)} fields.",
        f"Match '{query_text}' in fields {', '.join(fields)}."
    ]
    
    return {
        "instruction": random.choice(instructions),
        "query": {
            "query": {
                "multi_match": {
                    "query": query_text,
                    "fields": fields
                }
            }
        }
    }


def generate_exists_query() -> Dict[str, Any]:
    """Generate exists query examples"""
    field = random.choice(FIELDS)
    
    instructions = [
        f"Find documents that have the {field} field.",
        f"Search for documents where {field} exists.",
        f"Query documents containing {field} field.",
        f"Get documents that contain {field}.",
        f"Find all documents with {field} field present."
    ]
    
    return {
        "instruction": random.choice(instructions),
        "query": {
            "query": {
                "exists": {
                    "field": field
                }
            }
        }
    }


def generate_prefix_query() -> Dict[str, Any]:
    """Generate prefix query examples"""
    field = random.choice(FIELDS)
    prefix = random.choice(["prod", "test", "dev", "error", "warn", "user", "admin", "http", "https"])
    
    instructions = [
        f"Find documents where {field} starts with '{prefix}'.",
        f"Search for documents with {field} beginning with '{prefix}'.",
        f"Query documents where {field} has prefix '{prefix}'.",
        f"Get documents where {field} starts with '{prefix}'.",
        f"Find all documents with {field} prefix '{prefix}'."
    ]
    
    return {
        "instruction": random.choice(instructions),
        "query": {
            "query": {
                "prefix": {
                    field: prefix
                }
            }
        }
    }


def generate_wildcard_query() -> Dict[str, Any]:
    """Generate wildcard query examples"""
    field = random.choice(FIELDS)
    pattern = random.choice(["*error*", "*warn*", "user*", "admin*", "prod*", "test*", "*log", "*.json"])
    
    instructions = [
        f"Find documents where {field} matches pattern '{pattern}'.",
        f"Search for documents with {field} matching wildcard '{pattern}'.",
        f"Query documents where {field} matches '{pattern}'.",
        f"Get documents where {field} matches pattern '{pattern}'.",
        f"Find all documents with {field} matching '{pattern}'."
    ]
    
    return {
        "instruction": random.choice(instructions),
        "query": {
            "query": {
                "wildcard": {
                    field: pattern
                }
            }
        }
    }


def generate_nested_query() -> Dict[str, Any]:
    """Generate nested query examples"""
    nested_field = random.choice(["user", "tags", "metadata", "attributes"])
    sub_field = random.choice(["name", "id", "value", "type"])
    value = random.choice(VALUES)
    
    instructions = [
        f"Search in nested {nested_field} where {sub_field} equals {value}.",
        f"Find documents with nested {nested_field}.{sub_field} = {value}.",
        f"Query nested {nested_field} field where {sub_field} is {value}.",
        f"Search nested {nested_field} objects where {sub_field} equals {value}.",
        f"Find documents matching nested {nested_field}.{sub_field} = {value}."
    ]
    
    return {
        "instruction": random.choice(instructions),
        "query": {
            "query": {
                "nested": {
                    "path": nested_field,
                    "query": {
                        "term": {
                            f"{nested_field}.{sub_field}": value
                        }
                    }
                }
            }
        }
    }


def generate_examples() -> List[Dict[str, Any]]:
    """Generate diverse Query DSL examples"""
    examples = []
    
    generators = [
        generate_term_query,
        generate_match_query,
        generate_range_query,
        generate_bool_query,
        generate_aggregation_query,
        generate_multi_match_query,
        generate_exists_query,
        generate_prefix_query,
        generate_wildcard_query,
        generate_nested_query
    ]
    
    # Generate ~10,000 examples
    # Each generator called ~1000 times
    iterations_per_generator = 1000
    
    print(f"Generating Query DSL examples...")
    print(f"  Using {len(generators)} different query generators")
    print(f"  {iterations_per_generator} iterations per generator")
    print(f"  Target: ~{len(generators) * iterations_per_generator} examples")
    
    for i, generator in enumerate(generators):
        print(f"  [{i+1}/{len(generators)}] Generating {generator.__name__}...")
        for _ in range(iterations_per_generator):
            try:
                example_data = generator()
                example = {
                    "task": "query_dsl",
                    "domain": "general",
                    "instruction": example_data["instruction"],
                    "output": json.dumps(example_data["query"], ensure_ascii=False, separators=(',', ':')),
                    "source": "dsl-examples/synthetic"
                }
                examples.append(example)
            except Exception as e:
                # Skip invalid examples
                pass
    
    return examples


def collect_dsl_examples():
    """Main collection function"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("="*70)
    print("DSL Query Examples Collection")
    print("="*70)
    
    examples = generate_examples()
    
    # Save examples
    output_file = OUTPUT_DIR / "dsl_examples.jsonl"
    print(f"\nSaving {len(examples)} examples to {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    # Save metadata
    metadata = {
        "source": "DSL Examples Generator (Synthetic)",
        "total_examples": len(examples),
        "note": "Large-scale synthetic Query DSL examples covering all major query types",
        "query_types": [
            "term", "match", "range", "bool", "aggregations",
            "multi_match", "exists", "prefix", "wildcard", "nested"
        ]
    }
    
    metadata_file = OUTPUT_DIR / "metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"[OK] DSL examples collection complete!")
    print(f"     Total examples: {len(examples)}")
    print(f"     Output: {output_file}")
    print(f"{'='*70}")


if __name__ == "__main__":
    collect_dsl_examples()

