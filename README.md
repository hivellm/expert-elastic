# Expert Elastic

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/hivellm/expert-elastic/releases/tag/v0.1.0)
[![License](https://img.shields.io/badge/license-CC--BY--4.0-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-development-yellow.svg)](README.md#quick-start)

[![Base Model](https://img.shields.io/badge/base%20model-Qwen3--0.6B-orange.svg)](README.md#features)
[![Adapter](https://img.shields.io/badge/adapter-DoRA%20r%3D14-blue.svg)](README.md#training--configuration)
[![Dataset](https://img.shields.io/badge/dataset-9k%2B%20examples-brightgreen.svg)](README.md#dataset)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20CUDA-0078d4.svg)](README.md#features)

Elasticsearch expert for mappings, queries (DSL/KQL/EQL), analyzers, and ingest pipelines. Trained on official Elastic sources including ECS, integrations, Kibana samples, and detection rules.

## Quick Start

```bash
# 1. Collect data from all sources
cd F:/Node/hivellm/expert/experts/expert-elastic
python scripts/run_collection.py --all

# Or collect specific sources:
python scripts/collect_documentation.py  # Official documentation (NEW)
python scripts/collect_the_stack_elasticsearch.py --limit 50000  # The Stack (NEW - requires HF_TOKEN)
python scripts/run_collection.py --all   # Other sources

# 2. Preprocess dataset
python preprocess.py --all

# 3. Validate dataset
python scripts/validate_dataset.py

# 4. Train the expert
../../cli/target/release/expert-cli train
```

**Works best for:** Log analytics, security detection, observability, search applications  
**Limitations:** Not yet tested in production (see Known Limitations below)

## Features

- ✅ **Mapping Creation** - ECS-compliant index templates, field definitions
- ✅ **Query DSL** - Match, term, range, bool, aggregations, date histograms
- ✅ **KQL (Kibana Query Language)** - Security detection, log filtering
- ✅ **EQL (Event Query Language)** - Sequence queries, threat hunting
- ✅ **Ingest Pipelines** - Processors for data transformation (grok, geoip, rename, etc.)
- ✅ **Multi-domain support** - Security, observability, logs, metrics
- ✅ **DoRA adapter (r=14)** for complex Elasticsearch patterns
- ✅ **Grammar validation** (GBNF) for JSON/KQL/EQL syntax
- ✅ **Unsloth integration** - 2x faster training, 70% less VRAM
- ✅ **Windows optimized** with memory safety and CUDA support
- ✅ **English-only dataset** - All instructions in English for consistency

## What It Can Do ✅

### Mappings & Index Templates
- ✅ ECS (Elastic Common Schema) compliant mappings
- ✅ Integration-specific field definitions (nginx, apache, aws, gcp, etc.)
- ✅ Index templates with settings and mappings
- ✅ Nested field structures
- ✅ Custom analyzers and normalizers

### Query DSL
- ✅ Term and match queries
- ✅ Range queries (dates, numbers)
- ✅ Bool queries (must, should, must_not, filter)
- ✅ Aggregations (terms, avg, sum, date_histogram, etc.)
- ✅ Exists and wildcard queries
- ✅ Multi-field searches

### KQL (Kibana Query Language)
- ✅ Field:value patterns
- ✅ Boolean operators (AND, OR, NOT)
- ✅ Wildcards and fuzzy matching
- ✅ Security detection patterns
- ✅ MITRE ATT&CK based queries

### EQL (Event Query Language)
- ✅ Event type queries with conditions
- ✅ Sequence queries (temporal correlation)
- ✅ Join by field (e.g., by user.name)
- ✅ Maxspan time windows
- ✅ Threat hunting patterns

### Ingest Pipelines
- ✅ GeoIP enrichment
- ✅ Grok pattern parsing
- ✅ Field rename and set
- ✅ Date parsing
- ✅ User agent parsing
- ✅ Remove and trim processors

## Known Limitations ⚠️

**These are current limitations (not yet tested):**
- ⚠️ **No production testing** - Model not yet trained
- ⚠️ **No real-world benchmark** - Need to create test suite after training
- ⚠️ **No checkpoint comparison** - All checkpoints need evaluation
- ⚠️ **Unknown quality score** - Awaiting qualitative analysis

**Recommendation:** After training, create a benchmark with 30-50 scenarios covering mappings, queries (DSL/KQL/EQL), and pipelines to validate quality and select best checkpoint.

## Dataset

### Sources

**1. ECS (Elastic Common Schema)** (152 examples):
- Source: https://github.com/elastic/ecs
- Content: YAML field definitions from official ECS schemas
- Extraction: Field types, descriptions, nested structures
- Focus: ECS-compliant mappings

**2. Elastic Integrations** (0 examples - needs fixing):
- Source: https://epr.elastic.co (Package Registry)
- Content: Integration packages (nginx, apache, aws, gcp, etc.)
- Extraction: fields.yml + ingest pipelines
- Focus: Domain-specific mappings and pipelines
- **Status:** Collection script needs debugging

**3. Kibana Sample Data** (40 examples):
- Source: Kibana built-in samples (eCommerce, Flights, Web Logs)
- Content: Real-world schemas and query patterns
- Generation: Synthetic queries based on sample data
- Focus: Query DSL and aggregations

**3b. The Stack Dataset** (10,000-25,000 examples - NEW):
- Source: https://huggingface.co/datasets/bigcode/the-stack
- Content: Real-world Elasticsearch code from production codebases
- Extraction: Query DSL, mappings, pipelines from Python/JavaScript/Java/Go/Ruby code
- Focus: Production patterns, diverse use cases, multiple languages
- **Status:** Script ready - requires HuggingFace token
- **Collection:** `python scripts/collect_the_stack_elasticsearch.py --limit 50000`

**4. Detection Rules** (224 examples):
- Source: https://github.com/elastic/detection-rules
- Content: Security detection rules (KQL + EQL)
- Extraction: TOML rule files with query, description, MITRE tactics
- Focus: KQL and EQL for security use cases

**5. Elastic Labs** (6,000 examples):
- Source: Synthetic template-based examples
- Content: NL→DSL query patterns
- Generation: Template substitution with common patterns
- Focus: Query DSL bootstrapping

**6. Elasticsearch Examples** (67 examples):
- Source: Official Elasticsearch documentation patterns
- Content: Common query DSL and mapping patterns
- Focus: Standard Elasticsearch operations

**7. Synthetic KQL/EQL/Pipelines** (1,990 examples):
- Source: Synthetic generation
- Content: KQL queries, EQL sequences, ingest pipelines
- Focus: Increased coverage for KQL, EQL, and pipeline tasks

**8. DSL Examples** (9,935 raw examples, ~6,669 after deduplication):
- Source: Large-scale synthetic generation
- Content: Comprehensive Query DSL examples covering all major query types
- Focus: **Primary dataset for Query DSL** - term, match, range, bool, aggregations, multi-match, exists, prefix, wildcard, nested queries
- Query types: 10 different generators × 1,000 iterations each

**9. Official Documentation** (119 examples - NEW):
- Source: https://www.elastic.co/guide/en/elasticsearch/reference/current/
- Content: Query DSL, mappings, aggregations, pipelines from official docs
- Extraction: Web scraping documentation pages
- Focus: Official examples with explanations

**10. The Stack** (10,000-25,000 examples - NEW):
- Source: https://huggingface.co/datasets/bigcode/the-stack
- Content: Real-world Elasticsearch code from production codebases
- Languages: Python, JavaScript, TypeScript, Java, Go, Ruby
- Focus: Production patterns, diverse domains, real-world use cases
- **Collection:** `python scripts/collect_the_stack_elasticsearch.py --limit 50000`
- **Setup Guide:** See `docs/THE_STACK_SETUP.md`

### Dataset Statistics (Current)

- **Total processed**: 9,181 examples (from 18,408 raw examples)
- **Task distribution**:
  - Query DSL: 8,551 (93.1%) ⭐ **Focus on most-used function**
  - Mapping creation: 363 (4.0%)
  - KQL: 118 (1.3%)
  - EQL: 73 (0.8%)
  - Pipeline creation: 76 (0.8%)
- **Language**: English only (Portuguese instructions filtered out)
- **Deduplication**: 9,105 duplicates removed
- **Portuguese filtered**: 122 examples removed

### Dataset Expansion (Planned)

- **The Stack**: +10,000-25,000 examples (real-world production code)
- **Official Documentation**: +2,000-3,000 examples (already collected: 119)
- **Text-to-ES Bench**: +30,000 examples (academic benchmark)
- **Total potential**: ~50,000-60,000 examples

### Preprocessing Applied

- **ChatML formatting** for Qwen3 compatibility
- **JSON validation** for mappings, queries, pipelines
- **Deduplication** by task+instruction hash
- **Language filtering** - Portuguese instructions removed (English only)
- **Domain tagging** (ecs, integration, security, kibana)

### Collecting The Stack Dataset

To add real-world Elasticsearch code from The Stack:

```bash
# 1. Accept terms at https://huggingface.co/datasets/bigcode/the-stack
# 2. Set HuggingFace token
export HF_TOKEN=your_token_here  # or: huggingface-cli login

# 3. Install dependencies
pip install datasets

# 4. Run collection (recommended: 50,000 files)
python scripts/collect_the_stack_elasticsearch.py --limit 50000

# 5. Preprocess to integrate with main dataset
python preprocess.py --all
```

**Expected:** +10,000-25,000 examples from production codebases

See `docs/THE_STACK_SETUP.md` for detailed instructions.

## Data Collection

### Manual Collection (Recommended)

Run collection scripts individually:

```bash
cd scripts

# Collect ECS mappings
python collect_ecs.py

# Collect integrations
python collect_integrations.py

# Collect Kibana samples
python collect_kibana_samples.py

# Collect detection rules
python collect_detection_rules.py

# Collect Elastic Labs examples
python collect_elastic_labs.py

# Generate large-scale DSL examples
python generate_dsl_examples.py
```

### Automated Collection

Run all collectors in sequence:

```bash
# Run all collectors
python scripts/run_collection.py --all

# Run specific collectors
python scripts/run_collection.py --source ecs --source kibana

# List available collectors
python scripts/run_collection.py --list
```

## Preprocessing

After collecting raw data, preprocess into training format:

```bash
# Process all sources
python preprocess.py --all

# Process specific sources
python preprocess.py --source ecs --source integrations

# Custom output directory
python preprocess.py --all --output datasets/processed
```

**Output:**
- `datasets/train.jsonl` - ChatML formatted training data
- `datasets/metadata.json` - Statistics and task distribution

## Validation

Validate the processed dataset:

```bash
# Validate dataset
python scripts/validate_dataset.py

# Validate custom file
python scripts/validate_dataset.py --input datasets/train.jsonl
```

**Checks:**
- JSON syntax for mappings, queries, pipelines
- KQL/EQL basic syntax validation
- Field completeness (task, instruction, output)
- Task distribution analysis

## Training

### Configuration

Training parameters (from `manifest.json`):

- **Adapter:** DoRA r=14 (optimized for Elasticsearch complexity)
- **Epochs:** 2.0 (optimized for small dataset)
- **Batch size:** 2 (effective 90 with grad_accum=45)
- **Learning rate:** 5e-5
- **Scheduler:** Cosine decay
- **Max sequence length:** 1024
- **Checkpoints:** Every 50 steps (more frequent for small dataset)
- **Evaluation:** Every 50 steps

### Run Training

```bash
# Start training (from project root)
cd F:/Node/hivellm/expert
expert-cli train --manifest experts/expert-elastic/manifest.json
```

### Monitor Progress

```bash
# View training logs
tensorboard --logdir experts/expert-elastic/weights/qwen3-06b/logs
```

## Testing

Run test suite to validate functionality:

```bash
cd tests

# Run all tests
pytest -v

# Run specific test files
pytest test_expert.py -v
pytest test_mappings.py -v
pytest test_queries.py -v
pytest test_pipelines.py -v
```

**Test Coverage:**
- **test_expert.py** - Basic structure and configuration
- **test_mappings.py** - 10 mapping creation scenarios
- **test_queries.py** - 15 query scenarios (5 DSL + 5 KQL + 5 EQL)
- **test_pipelines.py** - 8 pipeline creation scenarios

## Usage Examples

### Mapping Creation

**Instruction:**
> Create an ECS mapping for nginx logs with fields client.ip, url.original, and http.response.status_code.

**Expected Output:**
```json
{
  "index_patterns": ["logs-nginx-*"],
  "template": {
    "settings": {"number_of_shards": 1},
    "mappings": {
      "properties": {
        "client": {
          "properties": {"ip": {"type": "ip"}}
        },
        "url": {
          "properties": {"original": {"type": "keyword"}}
        },
        "http": {
          "properties": {
            "response": {
              "properties": {"status_code": {"type": "long"}}
            }
          }
        }
      }
    }
  }
}
```

### Query DSL

**Instruction:**
> Search for documents where status is 'active' AND category is 'production'.

**Expected Output:**
```json
{
  "query": {
    "bool": {
      "must": [
        {"term": {"status": "active"}},
        {"term": {"category": "production"}}
      ]
    }
  }
}
```

### KQL

**Instruction:**
> Detect process execution of regsvr32.exe on Windows.

**Expected Output:**
```
process.name: "regsvr32.exe" and event.category: process
```

### EQL

**Instruction:**
> Detect web request followed by process creation by same user within 5 minutes.

**Expected Output:**
```
sequence by user.name with maxspan=5m 
  [network where event.category == "web"] 
  [process where event.type == "start"]
```

### Ingest Pipeline

**Instruction:**
> Create a pipeline to add geoip data for source.ip and destination.ip.

**Expected Output:**
```json
{
  "processors": [
    {"geoip": {"field": "source.ip", "target_field": "source.geo"}},
    {"geoip": {"field": "destination.ip", "target_field": "destination.geo"}}
  ]
}
```

## Architecture

### Model Configuration
- **Base model:** Qwen3-0.6B (int4 quantization)
- **Adapter:** DoRA r=14, alpha=28, dropout=0.1
- **Target modules:** q_proj, k_proj, v_proj, o_proj, up_proj, down_proj
- **Prompt template:** ChatML
- **VRAM overhead:** ~22MB

### Training Optimizations
- **Unsloth:** 2x faster training, 70% less VRAM
- **Windows compatible:** num_workers=0, pin_memory=false
- **Memory efficient:** Gradient checkpointing, attention_only activation checkpointing
- **Batch optimization:** Small batch (2) + high grad_accum (45) = effective batch 90

### Grammar Validation
- **JSON:** Strict RFC 8259 compliance for mappings/queries/pipelines
- **KQL:** Field:value patterns with boolean operators
- **EQL:** Event type queries with where clauses and sequences

## Project Structure

```
expert-elastic/
├── manifest.json              # Expert configuration
├── preprocess.py             # Dataset preprocessing
├── grammar.gbnf              # GBNF grammar for validation
├── README.md                 # This file
├── LICENSE                   # Apache-2.0
├── datasets/
│   ├── raw/                  # Raw data from sources
│   │   ├── ecs/              # ECS mappings
│   │   ├── integrations/     # Integration packages
│   │   ├── kibana_samples/   # Kibana sample data
│   │   ├── detection_rules/  # KQL/EQL rules
│   │   └── elastic_labs/     # NL→DSL examples
│   ├── train.jsonl           # Processed training data
│   └── metadata.json         # Dataset statistics
├── scripts/
│   ├── collect_ecs.py                # ECS collector
│   ├── collect_integrations.py       # Integrations collector
│   ├── collect_kibana_samples.py     # Kibana samples collector
│   ├── collect_detection_rules.py    # Detection rules collector
│   ├── collect_elastic_labs.py       # Elastic Labs collector
│   ├── run_collection.py             # Collection orchestrator
│   └── validate_dataset.py           # Dataset validator
├── tests/
│   ├── test_expert.py        # Basic tests
│   ├── test_mappings.py      # Mapping tests (10 scenarios)
│   ├── test_queries.py       # Query tests (15 scenarios)
│   └── test_pipelines.py     # Pipeline tests (8 scenarios)
└── weights/
    └── qwen3-06b/            # Model checkpoints (after training)
```

## Contributing

Contributions welcome! Areas for improvement:

1. **Data collection:**
   - Real Kibana sample data extraction via API
   - Additional ECS field coverage
   - More detection rules (current: ~10 categories, expandable)

2. **Preprocessing:**
   - Advanced schema normalization
   - Multi-version ECS support
   - Query complexity categorization

3. **Testing:**
   - Real-world benchmark suite
   - Checkpoint comparison framework
   - Quality score automation

4. **Documentation:**
   - Use case examples
   - Best practices guide
   - Troubleshooting section

## License

Apache-2.0 - See LICENSE file for details

## Acknowledgments

- **Elastic** for ECS, integrations, and detection rules
- **Qwen Team** for Qwen3-0.6B base model
- **Unsloth** for training optimizations
- **LLaMA-Factory** for DoRA implementation

## References

- [Elastic Common Schema (ECS)](https://github.com/elastic/ecs)
- [Elastic Package Registry](https://epr.elastic.co)
- [Elastic Detection Rules](https://github.com/elastic/detection-rules)
- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Qwen3 Model](https://huggingface.co/Qwen)
- [Unsloth](https://github.com/unslothai/unsloth)

---

**Status:** Dataset ready (9,181 examples, English only). **Query DSL-focused (93%)**. Training pending.  
**Next Steps:** Train → evaluate checkpoints → select best checkpoint → package

