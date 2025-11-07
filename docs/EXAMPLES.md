# Expert Elastic - Usage Examples

This document provides practical examples of using the expert-elastic model for various Elasticsearch tasks.

## Mapping Creation

### Example 1: ECS-compliant mapping for web server logs

**Prompt:**
```
Create an ECS mapping for nginx access logs with fields:
- client.ip (IP address)
- url.original (keyword)
- http.request.method (keyword)
- http.response.status_code (long)
- @timestamp (date)
```

**Expected Output:**
```json
{
  "index_patterns": ["logs-nginx-*"],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1
    },
    "mappings": {
      "properties": {
        "@timestamp": {"type": "date"},
        "client": {
          "properties": {
            "ip": {"type": "ip"}
          }
        },
        "url": {
          "properties": {
            "original": {"type": "keyword"}
          }
        },
        "http": {
          "properties": {
            "request": {
              "properties": {
                "method": {"type": "keyword"}
              }
            },
            "response": {
              "properties": {
                "status_code": {"type": "long"}
              }
            }
          }
        }
      }
    }
  }
}
```

### Example 2: Custom analyzer mapping

**Prompt:**
```
Create an index mapping for product search with:
- product_name (text with standard analyzer)
- sku (keyword)
- price (float)
- description (text with english analyzer)
```

**Expected Output:**
```json
{
  "mappings": {
    "properties": {
      "product_name": {
        "type": "text",
        "analyzer": "standard"
      },
      "sku": {
        "type": "keyword"
      },
      "price": {
        "type": "float"
      },
      "description": {
        "type": "text",
        "analyzer": "english"
      }
    }
  }
}
```

## Query DSL

### Example 3: Simple search query

**Prompt:**
```
Search for documents where status equals 'active' in the users index.
```

**Expected Output:**
```json
{
  "query": {
    "term": {
      "status": "active"
    }
  }
}
```

### Example 4: Complex bool query

**Prompt:**
```
Find products where:
- category is 'electronics' OR 'computers'
- price is between 100 and 1000
- in_stock is true
```

**Expected Output:**
```json
{
  "query": {
    "bool": {
      "must": [
        {
          "range": {
            "price": {
              "gte": 100,
              "lte": 1000
            }
          }
        },
        {
          "term": {
            "in_stock": true
          }
        }
      ],
      "should": [
        {"term": {"category": "electronics"}},
        {"term": {"category": "computers"}}
      ],
      "minimum_should_match": 1
    }
  }
}
```

### Example 5: Aggregation query

**Prompt:**
```
Calculate the average order value and group sales by category.
Show top 5 categories.
```

**Expected Output:**
```json
{
  "size": 0,
  "aggs": {
    "avg_order_value": {
      "avg": {
        "field": "order_total"
      }
    },
    "by_category": {
      "terms": {
        "field": "category",
        "size": 5
      },
      "aggs": {
        "total_sales": {
          "sum": {
            "field": "order_total"
          }
        }
      }
    }
  }
}
```

### Example 6: Date histogram

**Prompt:**
```
Show daily sales trend for the last 30 days.
```

**Expected Output:**
```json
{
  "query": {
    "range": {
      "@timestamp": {
        "gte": "now-30d"
      }
    }
  },
  "size": 0,
  "aggs": {
    "daily_sales": {
      "date_histogram": {
        "field": "@timestamp",
        "calendar_interval": "day"
      },
      "aggs": {
        "total": {
          "sum": {
            "field": "amount"
          }
        }
      }
    }
  }
}
```

## KQL (Kibana Query Language)

### Example 7: Process detection

**Prompt:**
```
Detect execution of cmd.exe or powershell.exe on Windows hosts.
```

**Expected Output:**
```
process.name: ("cmd.exe" or "powershell.exe") and host.os.platform: "windows"
```

### Example 8: Network connection

**Prompt:**
```
Find network connections to suspicious IP 192.168.1.100 on port 445.
```

**Expected Output:**
```
destination.ip: "192.168.1.100" and destination.port: 445 and event.category: network
```

### Example 9: File access

**Prompt:**
```
Detect access to files with .exe extension in the temp directory.
```

**Expected Output:**
```
file.path: *\\temp\\*.exe and event.type: ("creation" or "modification")
```

## EQL (Event Query Language)

### Example 10: Sequence detection

**Prompt:**
```
Detect a network connection followed by process creation by the same user within 5 minutes.
```

**Expected Output:**
```
sequence by user.name with maxspan=5m
  [network where event.category == "network"]
  [process where event.type == "start"]
```

### Example 11: Registry modification

**Prompt:**
```
Detect registry modification followed by suspicious process execution.
```

**Expected Output:**
```
sequence by host.id with maxspan=2m
  [registry where event.type == "modification" and registry.path like "*\\Run\\*"]
  [process where process.name in ("cmd.exe", "powershell.exe", "wscript.exe")]
```

### Example 12: Simple event query

**Prompt:**
```
Find all process creation events where the parent process is explorer.exe.
```

**Expected Output:**
```
process where event.type == "start" and process.parent.name == "explorer.exe"
```

## Ingest Pipelines

### Example 13: GeoIP enrichment

**Prompt:**
```
Create a pipeline to add GeoIP information for client IP addresses.
```

**Expected Output:**
```json
{
  "processors": [
    {
      "geoip": {
        "field": "client.ip",
        "target_field": "client.geo",
        "ignore_missing": true
      }
    }
  ]
}
```

### Example 14: Grok parsing

**Prompt:**
```
Create a pipeline to parse Apache access logs.
```

**Expected Output:**
```json
{
  "processors": [
    {
      "grok": {
        "field": "message",
        "patterns": [
          "%{IPORHOST:client.ip} - %{USER:user.name} \\[%{HTTPDATE:@timestamp}\\] \"%{WORD:http.request.method} %{URIPATHPARAM:url.original} HTTP/%{NUMBER:http.version}\" %{NUMBER:http.response.status_code} %{NUMBER:http.response.bytes}"
        ]
      }
    }
  ]
}
```

### Example 15: Multiple processors

**Prompt:**
```
Create a pipeline to:
1. Parse timestamp field
2. Add GeoIP for source.ip
3. Rename old_field to new_field
4. Remove temporary_field
```

**Expected Output:**
```json
{
  "processors": [
    {
      "date": {
        "field": "timestamp",
        "target_field": "@timestamp",
        "formats": ["ISO8601", "yyyy-MM-dd HH:mm:ss"]
      }
    },
    {
      "geoip": {
        "field": "source.ip",
        "target_field": "source.geo"
      }
    },
    {
      "rename": {
        "field": "old_field",
        "target_field": "new_field",
        "ignore_missing": true
      }
    },
    {
      "remove": {
        "field": "temporary_field",
        "ignore_missing": true
      }
    }
  ]
}
```

## Real-World Scenarios

### Scenario 1: E-commerce Analytics

**Task:** Set up index for product orders with analytics

**Steps:**

1. Create mapping:
```
Create an index mapping for e-commerce orders with:
- order_id (keyword)
- customer_id (keyword)
- products (nested with sku, name, price, quantity)
- total_amount (float)
- order_date (date)
- status (keyword)
```

2. Create search query:
```
Find all completed orders in the last 7 days where total_amount > 100
```

3. Create aggregation:
```
Show top 10 products by revenue, grouped by day
```

### Scenario 2: Security Monitoring

**Task:** Detect lateral movement in network

**Steps:**

1. Create KQL filter:
```
Detect RDP connections (port 3389) between internal hosts
```

2. Create EQL sequence:
```
Detect successful authentication followed by lateral RDP within 10 minutes from same source
```

3. Create pipeline:
```
Enrich security events with threat intelligence and GeoIP data
```

### Scenario 3: Log Management

**Task:** Centralize application logs

**Steps:**

1. Create ECS mapping:
```
Create ECS-compliant mapping for application logs with service.name, log.level, message, @timestamp
```

2. Create ingest pipeline:
```
Parse log level, timestamp, and extract error codes from message field
```

3. Create queries:
```
a) Count errors by service in the last hour
b) Find critical errors with response time > 1000ms
```

## Tips for Best Results

1. **Be specific:** Include field names, types, and constraints
2. **Use ECS terminology:** Follow Elastic Common Schema naming conventions
3. **Specify context:** Mention index names, time ranges, or domains
4. **Request validation:** Ask for syntactically correct outputs
5. **Combine tasks:** Request related mappings, queries, and pipelines together

## API Integration Example

```python
import requests

def generate_elasticsearch_query(instruction: str) -> dict:
    """
    Generate Elasticsearch query using expert-elastic
    """
    response = requests.post(
        "http://localhost:8000/v1/chat/completions",
        json={
            "model": "expert-elastic",
            "messages": [
                {
                    "role": "system",
                    "content": "Dialect: elastic\nTask: query_dsl"
                },
                {
                    "role": "user",
                    "content": instruction
                }
            ],
            "temperature": 0.7
        }
    )
    
    result = response.json()
    query_text = result["choices"][0]["message"]["content"]
    
    # Parse JSON query
    import json
    return json.loads(query_text)

# Usage
query = generate_elasticsearch_query(
    "Find active users who logged in within the last 24 hours"
)
print(query)
```

## Testing Your Queries

Always test generated queries in a development environment:

```bash
# Test Query DSL
curl -X POST "localhost:9200/my-index/_search?pretty" \
  -H 'Content-Type: application/json' \
  -d @query.json

# Test ingest pipeline
curl -X POST "localhost:9200/_ingest/pipeline/my-pipeline/_simulate?pretty" \
  -H 'Content-Type: application/json' \
  -d @pipeline_with_docs.json

# Test mapping
curl -X PUT "localhost:9200/test-index?pretty" \
  -H 'Content-Type: application/json' \
  -d @mapping.json
```

---

For more examples and use cases, see the main README.md.

