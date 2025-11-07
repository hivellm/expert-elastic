# Dataset Ready for Training - Expert Elastic

## Status: ✅ READY

The dataset has been processed and is ready for training.

## Dataset Statistics

### Current Dataset (After Preprocessing)

- **Total Examples:** 9,650 (from 19,448 raw examples)
- **File:** `datasets/train.jsonl`
- **Format:** ChatML (Qwen3 compatible)
- **Language:** English only

### Task Distribution

| Task | Examples | Percentage |
|------|----------|------------|
| **Query DSL** | 8,617 | 89.3% ⭐ |
| **Mapping Creation** | 370 | 3.8% |
| **EQL** | 366 | 3.8% |
| **KQL** | 196 | 2.0% |
| **Pipeline Creation** | 101 | 1.0% |

### Preprocessing Summary

- **Raw Examples Loaded:** 19,448
- **Processed:** 9,650
- **Skipped:**
  - Missing fields: 0
  - Invalid JSON: 153
  - Duplicates: 9,147
  - Portuguese filtered: 498
  - Errors: 0

### Sources Included

✅ **ECS** - Elastic Common Schema mappings  
✅ **Kibana Samples** - Real-world queries  
✅ **Detection Rules** - KQL/EQL security queries  
✅ **Elastic Labs** - Synthetic NL→DSL examples  
✅ **Elasticsearch Examples** - Official patterns  
✅ **Synthetic KQL/EQL/Pipelines** - Generated examples  
✅ **DSL Examples** - Large-scale Query DSL  
✅ **Complex DSL** - Advanced query patterns  
✅ **Official Documentation** - 119 examples (NEW)  
⚠️ **The Stack** - Not yet collected (optional, +10k-25k examples)

## Dataset Format

Each example follows ChatML format:

```
<|system|>
Dialect: elastic
Task: query_dsl
Domain: ecs:base
<|end|>
<|user|>
Search for documents where status equals 'active'.
<|end|>
<|assistant|>
{"query":{"term":{"status":"active"}}}
<|end|>
```

## Ready for Training

The dataset is ready to use with the expert-cli:

```bash
cd F:/Node/hivellm/expert/experts/expert-elastic
../../cli/target/release/expert-cli train
```

## Next Steps (Optional)

### 1. Collect The Stack Dataset

To add 10,000-25,000 more examples from production code:

```bash
# Accept terms at https://huggingface.co/datasets/bigcode/the-stack
export HF_TOKEN=your_token_here
pip install datasets

# Collect (recommended: 50,000 files)
python scripts/collect_the_stack_elasticsearch.py --limit 50000

# Re-preprocess to include The Stack
python preprocess.py --all
```

### 2. Validate Dataset

Run validation script:

```bash
python scripts/validate_dataset.py
```

### 3. Create Train/Validation/Test Splits

Currently all examples are in training set. Consider creating splits:

- Train: 80% (~7,720 examples)
- Validation: 10% (~965 examples)
- Test: 10% (~965 examples)

## Quality Metrics

- ✅ **Format:** ChatML (validated)
- ✅ **JSON Syntax:** All outputs validated
- ✅ **Deduplication:** 9,147 duplicates removed
- ✅ **Language:** English only (498 Portuguese filtered)
- ✅ **Coverage:** All major Elasticsearch tasks included

## File Locations

- **Training Dataset:** `datasets/train.jsonl`
- **Metadata:** `datasets/metadata.json`
- **Raw Data:** `datasets/raw/`
- **Documentation:** `docs/`

## References

- **Dataset Expansion Guide:** `docs/DATASET_EXPANSION_ANALYSIS.md`
- **The Stack Setup:** `docs/THE_STACK_SETUP.md`
- **Collection Guide:** `docs/DATASET_COLLECTION_GUIDE.md`

