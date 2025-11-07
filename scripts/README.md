# Data Collection Scripts

This directory contains scripts to collect training data from various Elasticsearch sources.

## Scripts Overview

### Collection Scripts

**collect_ecs.py**
- Fetches ECS (Elastic Common Schema) field definitions
- Generates ECS-compliant mapping examples
- Output: ~5-8k examples
- Source: https://github.com/elastic/ecs

**collect_integrations.py**
- Fetches integration packages from Elastic Package Registry
- Extracts field definitions and ingest pipelines
- Output: ~10-15k examples
- Source: https://epr.elastic.co

**collect_kibana_samples.py**
- Generates queries from Kibana sample data schemas
- Includes eCommerce, Flights, and Web Logs datasets
- Output: ~3-5k examples
- Note: Uses synthetic examples based on known schemas

**collect_detection_rules.py**
- Fetches security detection rules from Elastic repository
- Extracts KQL and EQL queries with descriptions
- Output: ~2-3k examples (KQL + EQL)
- Source: https://github.com/elastic/detection-rules

**collect_elastic_labs.py**
- Generates synthetic NL→DSL examples
- Template-based query generation
- Output: ~500-1k examples
- Note: Fully synthetic for bootstrapping

### Utility Scripts

**run_collection.py**
- Orchestrates all collection scripts
- Runs collectors in sequence
- Provides summary and statistics

**validate_dataset.py**
- Validates processed dataset
- Checks JSON syntax for DSL/mapping/pipeline tasks
- Basic KQL/EQL validation
- Task distribution analysis

## Usage

### Individual Collection

Run specific collectors:

```bash
# ECS mappings
python collect_ecs.py

# Integrations
python collect_integrations.py

# Kibana samples
python collect_kibana_samples.py

# Detection rules (may take several minutes)
python collect_detection_rules.py

# Elastic Labs examples
python collect_elastic_labs.py
```

### Automated Collection

Run all collectors:

```bash
# Run all collectors
python run_collection.py --all

# Run specific collectors
python run_collection.py --source ecs --source kibana

# List available collectors
python run_collection.py --list
```

## Output Structure

Each collector saves data to `../datasets/raw/<source>/`:

```
datasets/raw/
├── ecs/
│   ├── ecs_mappings.jsonl
│   └── metadata.json
├── integrations/
│   ├── integrations.jsonl
│   └── metadata.json
├── kibana_samples/
│   ├── kibana_samples.jsonl
│   └── metadata.json
├── detection_rules/
│   ├── kql_rules.jsonl
│   ├── eql_rules.jsonl
│   └── metadata.json
└── elastic_labs/
    ├── nl_to_dsl.jsonl
    └── metadata.json
```

## Data Format

All collectors output JSONL with this structure:

```json
{
  "task": "mapping_create|query_dsl|kql|eql|pipeline_create",
  "domain": "ecs:nginx|integration:apache|security|general",
  "instruction": "Natural language instruction in PT or EN",
  "output": "JSON string or query text",
  "source": "Source identifier",
  "index": "Optional index name",
  "...": "Additional metadata"
}
```

## Requirements

Install dependencies:

```bash
pip install requests pyyaml toml
```

## Notes

**Rate Limiting:**
- `collect_integrations.py` and `collect_detection_rules.py` include rate limiting
- Avoid running these scripts too frequently to respect API limits

**API Access:**
- Most scripts use public APIs (no authentication required)
- `collect_detection_rules.py` uses GitHub API (rate limited to 60 req/hour without token)

**Customization:**
- Edit scripts to adjust limits (e.g., number of packages, categories)
- Modify instruction templates for different languages
- Add new data sources by creating similar collectors

## Troubleshooting

**GitHub API rate limit exceeded:**
```bash
# Set GitHub token (optional)
export GITHUB_TOKEN=your_token_here
```

**Network errors:**
- Check internet connection
- Verify URLs are accessible
- Retry individual collectors

**Empty output:**
- Check raw data directories exist
- Verify API responses are valid
- Review script logs for errors

## Development

To create a new collector:

1. Follow the pattern from existing collectors
2. Output JSONL with standard fields (task, instruction, output)
3. Include metadata.json with statistics
4. Add to `run_collection.py` COLLECTORS dict
5. Update this README

## Next Steps

After collection:

1. **Preprocess:** `python ../preprocess.py --all`
2. **Validate:** `python validate_dataset.py`
3. **Train:** `expert-cli train`

