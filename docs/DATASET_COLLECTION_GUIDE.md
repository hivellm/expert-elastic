# Dataset Collection Guide - Expert Elastic

## Overview

This guide explains how to collect datasets from various sources for the expert-elastic training.

## Prerequisites

### Python Dependencies

Install required Python packages:

```bash
pip install requests beautifulsoup4 pyyaml
```

Or use the CLI venv_windows (recommended):

```bash
F:/Node/hivellm/expert/cli/venv_windows/Scripts/pip.exe install beautifulsoup4
```

### Required Scripts

All collection scripts are in `scripts/` directory:
- `collect_documentation.py` - **NEW** - Official Elasticsearch documentation
- `collect_ecs.py` - ECS field definitions
- `collect_integrations.py` - Integration packages (needs fixing)
- `collect_kibana_samples.py` - Kibana sample data
- `collect_detection_rules.py` - Security detection rules
- `collect_elastic_labs.py` - Synthetic examples
- `collect_elasticsearch_examples.py` - GitHub examples
- `generate_kql_eql_pipelines.py` - Synthetic KQL/EQL/Pipelines
- `generate_dsl_examples.py` - Synthetic Query DSL

## Collection Methods

### Method 1: Run All Collectors

```bash
cd F:/Node/hivellm/expert/experts/expert-elastic
python scripts/run_collection.py --all
```

This runs all collection scripts in sequence.

### Method 2: Run Specific Sources

```bash
# Run only documentation collection (NEW)
python scripts/collect_documentation.py

# Run specific sources
python scripts/run_collection.py --source documentation --source ecs --source kibana
```

### Method 3: Run Individual Scripts

```bash
# Official documentation (NEW - HIGHEST PRIORITY)
python scripts/collect_documentation.py

# ECS mappings
python scripts/collect_ecs.py

# Kibana samples
python scripts/collect_kibana_samples.py

# Detection rules
python scripts/collect_detection_rules.py

# Elastic Labs synthetic
python scripts/collect_elastic_labs.py

# GitHub examples
python scripts/collect_elasticsearch_examples.py

# Synthetic generators
python scripts/generate_kql_eql_pipelines.py
python scripts/generate_dsl_examples.py
```

## New Dataset: Official Documentation

### What It Collects

The `collect_documentation.py` script scrapes the official Elasticsearch documentation and extracts:

- Query DSL examples (term, match, bool, range, etc.)
- Mapping examples and index templates
- Aggregation examples (terms, date_histogram, metrics)
- Ingest pipeline examples
- Code snippets with natural language descriptions

### Expected Output

- **Location:** `datasets/raw/documentation/documentation_examples.jsonl`
- **Estimated:** 2,000-3,000 examples
- **Quality:** ⭐⭐⭐⭐⭐ (Official source, highest quality)

### How It Works

1. Fetches documentation pages from https://www.elastic.co/guide/en/elasticsearch/reference/current/
2. Parses HTML to find code blocks
3. Extracts JSON from code blocks
4. Generates natural language instructions from page context
5. Saves examples in JSONL format

### Pages Scraped

- Query DSL pages (term, match, bool, range, etc.)
- Mapping pages (types, params, fields)
- Aggregation pages (terms, date_histogram, metrics)
- Ingest processor pages (geoip, grok, date, rename, set)
- Index template pages

## Output Format

All scripts output JSONL files in `datasets/raw/{source}/`:

```json
{
  "task": "query_dsl",
  "domain": "elasticsearch/official-docs",
  "instruction": "Search for documents matching a term query.",
  "output": "{\"query\":{\"term\":{\"status\":\"active\"}}}",
  "source": "elasticsearch/documentation",
  "source_url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html"
}
```

## Preprocessing

After collection, preprocess the dataset:

```bash
# Preprocess all sources
python preprocess.py --all

# Or preprocess specific sources (including documentation)
python preprocess.py --source documentation --source ecs --source kibana
```

The preprocessing script:
- Converts to ChatML format
- Validates JSON syntax
- Deduplicates examples
- Filters Portuguese instructions (English only)
- Creates train/validation/test splits

## Troubleshooting

### Documentation Collection Fails

**Error:** `ModuleNotFoundError: No module named 'bs4'`

**Solution:**
```bash
pip install beautifulsoup4
```

### Rate Limiting

If you get HTTP 429 errors, the script includes rate limiting (1 second delay between requests). If issues persist:

1. Increase delay in `collect_documentation.py`:
   ```python
   time.sleep(2)  # Increase from 1 to 2 seconds
   ```

2. Run collection in smaller batches

### Empty Output

If a script produces 0 examples:

1. Check if source URL is accessible
2. Verify output directory exists: `datasets/raw/{source}/`
3. Check script logs for errors
4. Verify source format hasn't changed

## Collection Priority

### Phase 1: Critical (Run First)

1. ✅ **Official Documentation** - Script ready, run immediately
2. ⚠️ **Integrations** - Script broken, needs debugging
3. ✅ **Synthetic Expansion** - Easy to expand

### Phase 2: Official Sources

4. 📝 **REST API Specs** - Need to create script
5. 📝 **Test Fixtures** - Need to create script
6. ✅ **GitHub Examples** - Script exists

### Phase 3: Enhancements

7. ✅ **ECS Expansion** - Easy to expand
8. ✅ **Kibana Expansion** - Easy to expand
9. 📝 **Client Examples** - Need to create script

## Expected Results

After running all collectors:

- **Current:** 9,562 examples
- **After Phase 1:** ~59,000 examples (+49,500)
- **After Phase 2:** ~65,000 examples (+5,750)
- **After Phase 3:** ~67,000 examples (+2,600)

## References

- **Documentation:** `docs/DATASET_EXPANSION_ANALYSIS.md` - Detailed analysis
- **Summary:** `docs/DATASET_EXPANSION_SUMMARY.md` - Quick reference
- **Collection Scripts:** `scripts/` directory

