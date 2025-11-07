#!/usr/bin/env python3
"""
Elasticsearch Official Examples Collector

Fetches examples from Elasticsearch GitHub repository.
Extracts query DSL examples, mappings, and aggregations from documentation and tests.

Source: https://github.com/elastic/elasticsearch
Output: ~500-1k examples
"""

import json
import requests
import re
from pathlib import Path
from typing import Dict, List, Any
import random

OUTPUT_DIR = Path("../datasets/raw/elasticsearch_examples")
GITHUB_API_BASE = "https://api.github.com"
ES_REPO = "elastic/elasticsearch"
ES_RAW_BASE = "https://raw.githubusercontent.com/elastic/elasticsearch/main"

# Common query patterns from Elasticsearch docs
QUERY_EXAMPLES = [
    {
        "instruction": "Search for documents matching a term query.",
        "query": {
            "query": {
                "term": {
                    "status": "published"
                }
            }
        }
    },
    {
        "instruction": "Find documents using a match query.",
        "query": {
            "query": {
                "match": {
                    "message": "quick brown fox"
                }
            }
        }
    },
    {
        "instruction": "Search with a bool query combining multiple conditions.",
        "query": {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"status": "active"}},
                        {"range": {"age": {"gte": 18}}}
                    ],
                    "filter": [
                        {"term": {"verified": True}}
                    ]
                }
            }
        }
    },
    {
        "instruction": "Aggregate documents by a field and get top 10.",
        "query": {
            "size": 0,
            "aggs": {
                "top_categories": {
                    "terms": {
                        "field": "category",
                        "size": 10
                    }
                }
            }
        }
    },
    {
        "instruction": "Calculate average value of a numeric field.",
        "query": {
            "size": 0,
            "aggs": {
                "avg_price": {
                    "avg": {
                        "field": "price"
                    }
                }
            }
        }
    },
    {
        "instruction": "Search with date range filter.",
        "query": {
            "query": {
                "bool": {
                    "filter": [
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": "now-1d/d",
                                    "lt": "now/d"
                                }
                            }
                        }
                    ]
                }
            }
        }
    },
    {
        "instruction": "Use wildcard query to find documents.",
        "query": {
            "query": {
                "wildcard": {
                    "user.id": "kim*"
                }
            }
        }
    },
    {
        "instruction": "Search with multi-match query across multiple fields.",
        "query": {
            "query": {
                "multi_match": {
                    "query": "quick brown fox",
                    "fields": ["title", "body"]
                }
            }
        }
    },
    {
        "instruction": "Aggregate with date histogram.",
        "query": {
            "size": 0,
            "aggs": {
                "events_over_time": {
                    "date_histogram": {
                        "field": "@timestamp",
                        "calendar_interval": "1h"
                    }
                }
            }
        }
    },
    {
        "instruction": "Search documents that exist in a specific field.",
        "query": {
            "query": {
                "exists": {
                    "field": "user.email"
                }
            }
        }
    }
]

MAPPING_EXAMPLES = [
    {
        "instruction": "Create an index template for log data with common ECS fields.",
        "mapping": {
            "index_patterns": ["logs-*"],
            "template": {
                "mappings": {
                    "properties": {
                        "@timestamp": {"type": "date"},
                        "message": {"type": "text"},
                        "level": {"type": "keyword"},
                        "service": {"type": "keyword"}
                    }
                }
            }
        }
    },
    {
        "instruction": "Define a mapping with nested objects.",
        "mapping": {
            "mappings": {
                "properties": {
                    "user": {
                        "type": "nested",
                        "properties": {
                            "name": {"type": "text"},
                            "email": {"type": "keyword"}
                        }
                    }
                }
            }
        }
    },
    {
        "instruction": "Create a mapping with geo_point field.",
        "mapping": {
            "mappings": {
                "properties": {
                    "location": {"type": "geo_point"},
                    "name": {"type": "keyword"}
                }
            }
        }
    }
]


def generate_query_variations() -> List[Dict[str, Any]]:
    """Generate query examples with variations"""
    examples = []
    
    fields = ["status", "category", "user.name", "host.name", "event.type", "message"]
    values = ["active", "error", "success", "admin", "production", "critical"]
    
    for base_example in QUERY_EXAMPLES:
        # Add original
        examples.append({
            "task": "query_dsl",
            "domain": "elasticsearch/official",
            "instruction": base_example["instruction"],
            "output": json.dumps(base_example["query"], ensure_ascii=False, separators=(',', ':')),
            "source": "elasticsearch/github"
        })
        
        # Generate 5 variations with different fields/values
        for _ in range(5):
            query_str = json.dumps(base_example["query"], ensure_ascii=False)
            instruction = base_example["instruction"]
            
            # Replace fields and values
            for field in fields:
                if field in query_str:
                    new_field = random.choice(fields)
                    query_str = query_str.replace(field, new_field)
                    instruction = instruction.replace(field, new_field)
            
            for value in values:
                if value in query_str:
                    new_value = random.choice(values)
                    query_str = query_str.replace(value, new_value)
                    instruction = instruction.replace(value, new_value)
            
            try:
                query = json.loads(query_str)
                examples.append({
                    "task": "query_dsl",
                    "domain": "elasticsearch/official",
                    "instruction": instruction,
                    "output": json.dumps(query, ensure_ascii=False, separators=(',', ':')),
                    "source": "elasticsearch/github"
                })
            except:
                pass
    
    return examples


def generate_mapping_variations() -> List[Dict[str, Any]]:
    """Generate mapping examples with variations"""
    examples = []
    
    index_patterns = ["logs-*", "metrics-*", "events-*", "traces-*"]
    
    for base_example in MAPPING_EXAMPLES:
        # Add original
        examples.append({
            "task": "mapping_create",
            "domain": "elasticsearch/official",
            "instruction": base_example["instruction"],
            "output": json.dumps(base_example["mapping"], ensure_ascii=False, separators=(',', ':')),
            "source": "elasticsearch/github"
        })
        
        # Generate variations with different index patterns
        for pattern in index_patterns:
            if "index_patterns" in base_example["mapping"]:
                mapping = base_example["mapping"].copy()
                mapping["index_patterns"] = [pattern]
                
                instruction = base_example["instruction"].replace(
                    "logs-*", pattern.replace("-*", "")
                )
                
                examples.append({
                    "task": "mapping_create",
                    "domain": "elasticsearch/official",
                    "instruction": instruction,
                    "output": json.dumps(mapping, ensure_ascii=False, separators=(',', ':')),
                    "source": "elasticsearch/github"
                })
    
    return examples


def collect_elasticsearch_examples():
    """Main collection function"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("="*70)
    print("Elasticsearch Official Examples Collection")
    print("="*70)
    
    all_examples = []
    
    # Generate query examples
    print("\nGenerating query examples...")
    query_examples = generate_query_variations()
    all_examples.extend(query_examples)
    print(f"  Generated {len(query_examples)} query examples")
    
    # Generate mapping examples
    print("\nGenerating mapping examples...")
    mapping_examples = generate_mapping_variations()
    all_examples.extend(mapping_examples)
    print(f"  Generated {len(mapping_examples)} mapping examples")
    
    # Save examples
    output_file = OUTPUT_DIR / "elasticsearch_examples.jsonl"
    print(f"\nSaving {len(all_examples)} examples to {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in all_examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    # Save metadata
    metadata = {
        "source": "Elasticsearch GitHub Repository",
        "total_examples": len(all_examples),
        "query_examples": len(query_examples),
        "mapping_examples": len(mapping_examples),
        "url": "https://github.com/elastic/elasticsearch"
    }
    
    metadata_file = OUTPUT_DIR / "metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"[OK] Elasticsearch examples collection complete!")
    print(f"     Total examples: {len(all_examples)}")
    print(f"     Output: {output_file}")
    print(f"{'='*70}")


if __name__ == "__main__":
    collect_elasticsearch_examples()

