#!/usr/bin/env python3
"""
Kibana Sample Data Collector

Generates queries and mappings from Kibana sample datasets:
- eCommerce
- Flights
- Web Logs

Note: This script generates synthetic query examples based on common
patterns from these datasets. For actual data, you can load Kibana
sample data and extract real queries.

Output: ~3-5k query examples
"""

import json
from pathlib import Path
from typing import Dict, List, Any
import random

OUTPUT_DIR = Path("../datasets/raw/kibana_samples")


# Sample dataset schemas
ECOMMERCE_SCHEMA = {
    "index": "kibana_sample_data_ecommerce",
    "fields": {
        "customer_id": "keyword",
        "customer_first_name": "text",
        "customer_last_name": "text",
        "customer_full_name": "text",
        "customer_gender": "keyword",
        "customer_phone": "keyword",
        "email": "keyword",
        "order_id": "keyword",
        "order_date": "date",
        "products": "nested",
        "products.product_name": "text",
        "products.sku": "keyword",
        "products.price": "float",
        "products.quantity": "integer",
        "total_quantity": "integer",
        "taxful_total_price": "float",
        "taxless_total_price": "float",
        "currency": "keyword",
        "geoip.country_iso_code": "keyword",
        "geoip.city_name": "keyword"
    }
}

FLIGHTS_SCHEMA = {
    "index": "kibana_sample_data_flights",
    "fields": {
        "FlightNum": "keyword",
        "Carrier": "keyword",
        "Origin": "keyword",
        "OriginCountry": "keyword",
        "OriginCityName": "keyword",
        "Dest": "keyword",
        "DestCountry": "keyword",
        "DestCityName": "keyword",
        "FlightDelay": "boolean",
        "FlightDelayType": "keyword",
        "DistanceMiles": "float",
        "DistanceKilometers": "float",
        "AvgTicketPrice": "float",
        "timestamp": "date",
        "dayOfWeek": "integer"
    }
}

WEBLOGS_SCHEMA = {
    "index": "kibana_sample_data_logs",
    "fields": {
        "agent": "text",
        "bytes": "long",
        "clientip": "ip",
        "extension": "keyword",
        "geo.coordinates": "geo_point",
        "geo.dest": "keyword",
        "geo.src": "keyword",
        "host": "keyword",
        "ip": "ip",
        "machine.os": "keyword",
        "machine.ram": "long",
        "memory": "long",
        "message": "text",
        "phpmemory": "long",
        "referer": "keyword",
        "request": "text",
        "response": "keyword",
        "tags": "keyword",
        "timestamp": "date",
        "url": "text",
        "utc_time": "date"
    }
}


def generate_query_examples(schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate query DSL examples for a schema"""
    examples = []
    index = schema["index"]
    fields = schema["fields"]
    
    # 1. Simple match queries
    text_fields = [k for k, v in fields.items() if v == "text"]
    for field in text_fields[:3]:
        query = {
            "query": {
                "match": {
                    field: "search term"
                }
            }
        }
        
        instructions = [
            f"Busque no índice {index} por documentos onde {field} contém 'search term'.",
            f"Search {index} for documents where {field} matches 'search term'.",
            f"Encontre documentos em {index} com {field} igual a 'search term'."
        ]
        
        examples.append({
            "task": "query_dsl",
            "index": index,
            "instruction": random.choice(instructions),
            "output": json.dumps(query, ensure_ascii=False, separators=(',', ':'))
        })
    
    # 2. Range queries
    date_fields = [k for k, v in fields.items() if v == "date"]
    for field in date_fields[:2]:
        query = {
            "query": {
                "range": {
                    field: {
                        "gte": "now-30d",
                        "lte": "now"
                    }
                }
            }
        }
        
        instructions = [
            f"Liste documentos em {index} dos últimos 30 dias usando {field}.",
            f"Get documents from {index} from the last 30 days based on {field}.",
            f"Filtre {index} por documentos recentes (últimos 30 dias) em {field}."
        ]
        
        examples.append({
            "task": "query_dsl",
            "index": index,
            "instruction": random.choice(instructions),
            "output": json.dumps(query, ensure_ascii=False, separators=(',', ':'))
        })
    
    # 3. Term queries
    keyword_fields = [k for k, v in fields.items() if v == "keyword"][:4]
    for field in keyword_fields:
        query = {
            "query": {
                "term": {
                    field: "exact_value"
                }
            }
        }
        
        instructions = [
            f"Busque documentos em {index} onde {field} é exatamente 'exact_value'.",
            f"Find documents in {index} with exact match on {field}.",
            f"Filtrar {index} por {field} igual a 'exact_value'."
        ]
        
        examples.append({
            "task": "query_dsl",
            "index": index,
            "instruction": random.choice(instructions),
            "output": json.dumps(query, ensure_ascii=False, separators=(',', ':'))
        })
    
    # 4. Aggregations
    numeric_fields = [k for k, v in fields.items() if v in ["float", "long", "integer"]]
    if numeric_fields:
        field = numeric_fields[0]
        query = {
            "size": 0,
            "aggs": {
                "avg_value": {
                    "avg": {
                        "field": field
                    }
                }
            }
        }
        
        instructions = [
            f"Calcule a média de {field} no índice {index}.",
            f"Calculate the average of {field} in {index}.",
            f"Obtenha o valor médio de {field} em {index}."
        ]
        
        examples.append({
            "task": "query_dsl",
            "index": index,
            "instruction": random.choice(instructions),
            "output": json.dumps(query, ensure_ascii=False, separators=(',', ':'))
        })
    
    # 5. Terms aggregation (top N)
    if keyword_fields:
        field = keyword_fields[0]
        query = {
            "size": 0,
            "aggs": {
                "top_values": {
                    "terms": {
                        "field": field,
                        "size": 10
                    }
                }
            }
        }
        
        instructions = [
            f"Liste os 10 valores mais comuns de {field} em {index}.",
            f"Get the top 10 most common values for {field} in {index}.",
            f"Mostre os valores mais frequentes de {field} no índice {index}."
        ]
        
        examples.append({
            "task": "query_dsl",
            "index": index,
            "instruction": random.choice(instructions),
            "output": json.dumps(query, ensure_ascii=False, separators=(',', ':'))
        })
    
    # 6. Bool queries (combination)
    if len(keyword_fields) >= 2:
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {keyword_fields[0]: "value1"}},
                        {"term": {keyword_fields[1]: "value2"}}
                    ]
                }
            }
        }
        
        instructions = [
            f"Busque em {index} documentos onde {keyword_fields[0]} é 'value1' E {keyword_fields[1]} é 'value2'.",
            f"Find documents in {index} where {keyword_fields[0]} equals 'value1' AND {keyword_fields[1]} equals 'value2'.",
            f"Filtre {index} por documentos que atendem ambas condições: {keyword_fields[0]}='value1' e {keyword_fields[1]}='value2'."
        ]
        
        examples.append({
            "task": "query_dsl",
            "index": index,
            "instruction": random.choice(instructions),
            "output": json.dumps(query, ensure_ascii=False, separators=(',', ':'))
        })
    
    # 7. Date histogram aggregation
    if date_fields:
        field = date_fields[0]
        query = {
            "size": 0,
            "aggs": {
                "over_time": {
                    "date_histogram": {
                        "field": field,
                        "calendar_interval": "day"
                    }
                }
            }
        }
        
        instructions = [
            f"Agrupe documentos de {index} por dia usando {field}.",
            f"Create a daily histogram of {index} documents based on {field}.",
            f"Mostre distribuição diária dos documentos em {index} por {field}."
        ]
        
        examples.append({
            "task": "query_dsl",
            "index": index,
            "instruction": random.choice(instructions),
            "output": json.dumps(query, ensure_ascii=False, separators=(',', ':'))
        })
    
    # 8. Exists query
    field = list(fields.keys())[0]
    query = {
        "query": {
            "exists": {
                "field": field
            }
        }
    }
    
    instructions = [
        f"Encontre documentos em {index} que possuem o campo {field}.",
        f"Get all documents from {index} where {field} exists.",
        f"Liste documentos de {index} onde {field} está presente."
    ]
    
    examples.append({
        "task": "query_dsl",
        "index": index,
        "instruction": random.choice(instructions),
        "output": json.dumps(query, ensure_ascii=False, separators=(',', ':'))
    })
    
    return examples


def generate_mapping_examples(schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate mapping examples from schema"""
    examples = []
    index = schema["index"]
    fields = schema["fields"]
    
    # Create full mapping
    properties = {}
    for field, field_type in fields.items():
        # Handle nested fields
        if "." in field:
            parts = field.split(".")
            current = properties
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {"properties": {}}
                elif "properties" not in current[part]:
                    current[part]["properties"] = {}
                current = current[part]["properties"]
            current[parts[-1]] = {"type": field_type}
        else:
            properties[field] = {"type": field_type}
    
    mapping = {
        "mappings": {
            "properties": properties
        }
    }
    
    instructions = [
        f"Create the complete mapping for {index} index.",
        f"Generate the full mapping for {index} index.",
        f"Define the Elasticsearch mapping for {index}."
    ]
    
    examples.append({
        "task": "mapping_create",
        "domain": f"kibana:{index}",
        "instruction": random.choice(instructions),
        "output": json.dumps(mapping, ensure_ascii=False, separators=(',', ':'))
    })
    
    return examples


def collect_kibana_samples():
    """Main collection function"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("="*70)
    print("Kibana Sample Data Collection")
    print("="*70)
    
    all_examples = []
    
    schemas = [ECOMMERCE_SCHEMA, FLIGHTS_SCHEMA, WEBLOGS_SCHEMA]
    
    for schema in schemas:
        index_name = schema["index"]
        print(f"\nProcessing {index_name}...")
        
        # Generate queries
        query_examples = generate_query_examples(schema)
        all_examples.extend(query_examples)
        print(f"  Generated {len(query_examples)} query examples")
        
        # Generate mappings
        mapping_examples = generate_mapping_examples(schema)
        all_examples.extend(mapping_examples)
        print(f"  Generated {len(mapping_examples)} mapping examples")
    
    # Save examples
    output_file = OUTPUT_DIR / "kibana_samples.jsonl"
    print(f"\nSaving {len(all_examples)} examples to {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in all_examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    # Save metadata
    metadata = {
        "source": "Kibana Sample Data",
        "datasets": ["eCommerce", "Flights", "Web Logs"],
        "total_examples": len(all_examples),
        "note": "Synthetic examples based on Kibana sample data schemas"
    }
    
    metadata_file = OUTPUT_DIR / "metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"[OK] Kibana samples collection complete!")
    print(f"     Total examples: {len(all_examples)}")
    print(f"     Output: {output_file}")
    print(f"{'='*70}")


if __name__ == "__main__":
    collect_kibana_samples()

