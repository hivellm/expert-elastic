#!/usr/bin/env python3
"""
Elastic Labs NL→DSL Collector

Generates synthetic NL→DSL examples based on common patterns.

Note: This is a simplified implementation. For production, you would
want to scrape actual blog posts and documentation from Elastic.

Output: ~500-1k examples
"""

import json
from pathlib import Path
from typing import Dict, List, Any
import random

OUTPUT_DIR = Path("../datasets/raw/elastic_labs")


# Template-based NL→DSL examples
QUERY_TEMPLATES = [
    {
        "instruction_pt": "Buscar todos os documentos onde {field} é igual a {value}.",
        "instruction_en": "Search all documents where {field} equals {value}.",
        "query": {
            "query": {
                "term": {
                    "{field}": "{value}"
                }
            }
        }
    },
    {
        "instruction_pt": "Encontrar documentos onde {field} contém {value}.",
        "instruction_en": "Find documents where {field} contains {value}.",
        "query": {
            "query": {
                "match": {
                    "{field}": "{value}"
                }
            }
        }
    },
    {
        "instruction_pt": "Listar documentos criados nos últimos {days} dias.",
        "instruction_en": "List documents created in the last {days} days.",
        "query": {
            "query": {
                "range": {
                    "timestamp": {
                        "gte": "now-{days}d"
                    }
                }
            }
        }
    },
    {
        "instruction_pt": "Agregar documentos por {field} e contar.",
        "instruction_en": "Aggregate documents by {field} and count.",
        "query": {
            "size": 0,
            "aggs": {
                "by_{field}": {
                    "terms": {
                        "field": "{field}"
                    }
                }
            }
        }
    },
    {
        "instruction_pt": "Calcular média de {field}.",
        "instruction_en": "Calculate average of {field}.",
        "query": {
            "size": 0,
            "aggs": {
                "avg_{field}": {
                    "avg": {
                        "field": "{field}"
                    }
                }
            }
        }
    },
    {
        "instruction_pt": "Buscar documentos onde {field1} é {value1} E {field2} é {value2}.",
        "instruction_en": "Search documents where {field1} is {value1} AND {field2} is {value2}.",
        "query": {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"{field1}": "{value1}"}},
                        {"term": {"{field2}": "{value2}"}}
                    ]
                }
            }
        }
    },
    {
        "instruction_pt": "Buscar documentos onde {field1} é {value1} OU {field2} é {value2}.",
        "instruction_en": "Search documents where {field1} is {value1} OR {field2} is {value2}.",
        "query": {
            "query": {
                "bool": {
                    "should": [
                        {"term": {"{field1}": "{value1}"}},
                        {"term": {"{field2}": "{value2}"}}
                    ]
                }
            }
        }
    },
    {
        "instruction_pt": "Buscar documentos onde {field} está entre {min} e {max}.",
        "instruction_en": "Search documents where {field} is between {min} and {max}.",
        "query": {
            "query": {
                "range": {
                    "{field}": {
                        "gte": "{min}",
                        "lte": "{max}"
                    }
                }
            }
        }
    },
    {
        "instruction_pt": "Buscar documentos que possuem o campo {field}.",
        "instruction_en": "Search documents that have the {field} field.",
        "query": {
            "query": {
                "exists": {
                    "field": "{field}"
                }
            }
        }
    },
    {
        "instruction_pt": "Buscar documentos onde {field} começa com {prefix}.",
        "instruction_en": "Search documents where {field} starts with {prefix}.",
        "query": {
            "query": {
                "prefix": {
                    "{field}": "{prefix}"
                }
            }
        }
    }
]


# Sample values for substitution
SAMPLE_FIELDS = [
    "status", "category", "user.name", "host.name", "event.type",
    "source.ip", "destination.ip", "process.name", "file.name",
    "http.response.status_code", "url.path", "message", "tags"
]

SAMPLE_VALUES = [
    "active", "error", "success", "admin", "user123",
    "production", "staging", "critical", "warning", "info"
]

SAMPLE_NUMERIC_FIELDS = [
    "http.response.status_code", "bytes", "response_time",
    "count", "duration", "price", "quantity"
]


def fill_template(template: Dict[str, Any]) -> Dict[str, Any]:
    """Fill template with random values"""
    instruction_pt = template["instruction_pt"]
    instruction_en = template["instruction_en"]
    query_template = json.dumps(template["query"])
    
    # Replace placeholders
    replacements = {
        "{field}": random.choice(SAMPLE_FIELDS),
        "{field1}": random.choice(SAMPLE_FIELDS),
        "{field2}": random.choice(SAMPLE_FIELDS),
        "{value}": random.choice(SAMPLE_VALUES),
        "{value1}": random.choice(SAMPLE_VALUES),
        "{value2}": random.choice(SAMPLE_VALUES),
        "{days}": str(random.choice([7, 14, 30, 90])),
        "{min}": str(random.randint(0, 100)),
        "{max}": str(random.randint(100, 1000)),
        "{prefix}": random.choice(["prod", "test", "dev", "error", "warn"])
    }
    
    for placeholder, value in replacements.items():
        instruction_pt = instruction_pt.replace(placeholder, value)
        instruction_en = instruction_en.replace(placeholder, value)
        query_template = query_template.replace(placeholder, value)
    
    # Use English only
    instruction = instruction_en
    
    # Parse query
    query = json.loads(query_template)
    
    return {
        "instruction": instruction,
        "query": query
    }


def generate_examples() -> List[Dict[str, Any]]:
    """Generate synthetic NL→DSL examples"""
    examples = []
    
    # Generate multiple variations of each template
    # Increased from 100 to 500 iterations for more examples
    for _ in range(500):  # 500 iterations = ~5k examples (10 templates × 500)
        for template in QUERY_TEMPLATES:
            filled = fill_template(template)
            
            example = {
                "task": "query_dsl",
                "domain": "general",
                "instruction": filled["instruction"],
                "output": json.dumps(filled["query"], ensure_ascii=False, separators=(',', ':')),
                "source": "elastic-labs/synthetic"
            }
            
            examples.append(example)
    
    # Generate mapping examples
    mapping_templates = [
        {
            "instruction_pt": "Crie um mapping ECS para logs de {service} com campos {field1}, {field2} e {field3}.",
            "instruction_en": "Create an ECS mapping for {service} logs with fields {field1}, {field2}, and {field3}.",
            "mapping": {
                "index_patterns": ["logs-{service}-*"],
                "template": {
                    "mappings": {
                        "properties": {
                            "{field1}": {"type": "keyword"},
                            "{field2}": {"type": "text"},
                            "{field3}": {"type": "long"}
                        }
                    }
                }
            }
        },
        {
            "instruction_pt": "Gere um index template para {service} incluindo campos de timestamp e status.",
            "instruction_en": "Generate an index template for {service} including timestamp and status fields.",
            "mapping": {
                "index_patterns": ["logs-{service}-*"],
                "template": {
                    "mappings": {
                        "properties": {
                            "@timestamp": {"type": "date"},
                            "status": {"type": "keyword"}
                        }
                    }
                }
            }
        }
    ]
    
    services = ["nginx", "apache", "mysql", "postgresql", "redis", "elasticsearch", "kibana", "logstash"]
    
    for _ in range(200):  # 200 iterations × 2 templates = 400 mapping examples
        for template in mapping_templates:
            service = random.choice(services)
            field1 = random.choice(SAMPLE_FIELDS)
            field2 = random.choice(SAMPLE_FIELDS)
            field3 = random.choice(SAMPLE_FIELDS)
            
            instruction = template["instruction_en"]
            instruction = instruction.replace("{service}", service)
            instruction = instruction.replace("{field1}", field1)
            instruction = instruction.replace("{field2}", field2)
            instruction = instruction.replace("{field3}", field3)
            
            mapping_str = json.dumps(template["mapping"], ensure_ascii=False)
            mapping_str = mapping_str.replace("{service}", service)
            mapping_str = mapping_str.replace("{field1}", field1)
            mapping_str = mapping_str.replace("{field2}", field2)
            mapping_str = mapping_str.replace("{field3}", field3)
            
            example = {
                "task": "mapping_create",
                "domain": f"service:{service}",
                "instruction": instruction,
                "output": mapping_str,
                "source": "elastic-labs/synthetic"
            }
            examples.append(example)
    
    # Generate pipeline examples
    pipeline_templates = [
        {
            "instruction_pt": "Crie um ingest pipeline para adicionar geoip ao campo {field}.",
            "instruction_en": "Create an ingest pipeline to add geoip to field {field}.",
            "pipeline": {
                "processors": [
                    {"geoip": {"field": "{field}", "target_field": "{field}.geo"}}
                ]
            }
        },
        {
            "instruction_pt": "Defina um pipeline para renomear o campo {old_field} para {new_field}.",
            "instruction_en": "Define a pipeline to rename field {old_field} to {new_field}.",
            "pipeline": {
                "processors": [
                    {"rename": {"field": "{old_field}", "target_field": "{new_field}"}}
                ]
            }
        }
    ]
    
    ip_fields = ["source.ip", "destination.ip", "client.ip", "server.ip"]
    old_new_pairs = [
        ("message", "log.message"),
        ("timestamp", "@timestamp"),
        ("host", "host.name"),
        ("service", "service.name")
    ]
    
    for _ in range(300):  # 300 iterations × 2 templates = 600 pipeline examples
        for template in pipeline_templates:
            if "{field}" in template["instruction_pt"]:
                field = random.choice(ip_fields)
                instruction = template["instruction_en"]
                instruction = instruction.replace("{field}", field)
                pipeline_str = json.dumps(template["pipeline"], ensure_ascii=False)
                pipeline_str = pipeline_str.replace("{field}", field)
            else:
                old_field, new_field = random.choice(old_new_pairs)
                instruction = template["instruction_en"]
                instruction = instruction.replace("{old_field}", old_field)
                instruction = instruction.replace("{new_field}", new_field)
                pipeline_str = json.dumps(template["pipeline"], ensure_ascii=False)
                pipeline_str = pipeline_str.replace("{old_field}", old_field)
                pipeline_str = pipeline_str.replace("{new_field}", new_field)
            
            example = {
                "task": "pipeline_create",
                "domain": "general",
                "instruction": instruction,
                "output": pipeline_str,
                "source": "elastic-labs/synthetic"
            }
            examples.append(example)
    
    return examples


def collect_elastic_labs():
    """Main collection function"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("="*70)
    print("Elastic Labs NL to DSL Collection")
    print("="*70)
    
    print("\nGenerating synthetic examples...")
    examples = generate_examples()
    
    # Save examples
    output_file = OUTPUT_DIR / "nl_to_dsl.jsonl"
    print(f"\nSaving {len(examples)} examples to {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    # Save metadata
    metadata = {
        "source": "Elastic Labs (Synthetic)",
        "total_examples": len(examples),
        "note": "Template-based synthetic examples for NL→DSL training"
    }
    
    metadata_file = OUTPUT_DIR / "metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"[OK] Elastic Labs collection complete!")
    print(f"     Total examples: {len(examples)}")
    print(f"     Output: {output_file}")
    print(f"{'='*70}")


if __name__ == "__main__":
    collect_elastic_labs()

