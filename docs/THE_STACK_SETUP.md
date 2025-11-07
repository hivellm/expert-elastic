# The Stack Dataset Setup Guide - Expert Elastic

## Overview

This guide explains how to collect Elasticsearch code examples from The Stack dataset to enrich the expert-elastic training dataset.

## What is The Stack?

**The Stack** is a massive dataset containing source code in over 300 programming languages, totaling ~3.1 TB of data. It's maintained by BigCode and available on HuggingFace.

- **Dataset:** https://huggingface.co/datasets/bigcode/the-stack
- **Paper:** https://arxiv.org/abs/2211.15533
- **Size:** ~3.1 TB of code

## Why Use The Stack?

✅ **Real-world patterns** - Production code from actual projects  
✅ **Massive scale** - Potentially 10,000-25,000 Elasticsearch examples  
✅ **Diverse use cases** - Different domains and applications  
✅ **Multiple languages** - Python, JavaScript, TypeScript, Java, Go, Ruby  
✅ **Production quality** - Real code used in production systems

## Prerequisites

### 1. Accept Dataset Terms

Visit https://huggingface.co/datasets/bigcode/the-stack and click "Access repository" to accept the terms of use.

### 2. Install Dependencies

```bash
# Install datasets library
pip install datasets

# Or use CLI venv_windows (recommended)
F:/Node/hivellm/expert/cli/venv_windows/Scripts/pip.exe install datasets
```

### 3. Get HuggingFace Token

**Option A: Environment Variable**
```bash
# Windows PowerShell
$env:HF_TOKEN="your_token_here"

# Windows CMD
set HF_TOKEN=your_token_here

# Linux/WSL
export HF_TOKEN=your_token_here
```

**Option B: HuggingFace CLI**
```bash
huggingface-cli login
```

**Option C: Get Token from Settings**
1. Go to https://huggingface.co/settings/tokens
2. Create a new token (read access is enough)
3. Copy the token

## Collection Process

### Step 1: Run Collection Script

```bash
cd F:/Node/hivellm/expert/experts/expert-elastic

# Basic usage (processes 10,000 files)
python scripts/collect_the_stack_elasticsearch.py

# With custom limit (recommended: 50,000 files)
python scripts/collect_the_stack_elasticsearch.py --limit 50000

# With specific languages
python scripts/collect_the_stack_elasticsearch.py --limit 50000 --languages python javascript typescript

# With custom output path
python scripts/collect_the_stack_elasticsearch.py --limit 50000 --output datasets/raw/the_stack_elasticsearch/custom.jsonl
```

### Step 2: Monitor Progress

The script will:
1. Load The Stack dataset in streaming mode
2. Filter files mentioning Elasticsearch keywords
3. Extract Query DSL, mappings, and pipelines
4. Generate instructions from code context
5. Validate JSON/DSL syntax
6. Save examples to JSONL file

**Expected output:**
```
================================================================================
Loading Elasticsearch code from bigcode/the-stack
Languages: python, javascript, typescript, java, go, ruby
================================================================================
[OK] Dataset loaded (streaming mode)

Processing files (limit: 50000)...
Processing: 100%|████████████| 50000/50000 [45:23<00:00, 18.4it/s]

================================================================================
Collection Summary:
  Processed files: 1,234
  Skipped files: 48,766
  Total examples: 5,678
================================================================================

Saving to F:\Node\hivellm\expert\experts\expert-elastic\datasets\raw\the_stack_elasticsearch\the_stack_elasticsearch.jsonl...
Writing: 100%|████████████| 5678/5678 [00:02<00:00, 2341.2it/s]

[OK] Saved 5,678 examples to the_stack_elasticsearch.jsonl
     File size: 12.3 MB
     Metadata: the_stack_elasticsearch_metadata.json
```

### Step 3: Preprocess Dataset

After collection, integrate with the main dataset:

```bash
# Preprocess all sources including The Stack
python preprocess.py --all

# Or preprocess only The Stack
python preprocess.py --source the_stack
```

## Expected Results

### Conservative Estimate
- **Files processed:** 50,000 files
- **Files with Elasticsearch:** ~1,000-2,000 files
- **Examples extracted:** ~5,000-10,000 examples
- **After deduplication:** ~3,000-7,000 unique examples

### Optimistic Estimate
- **Files processed:** 100,000 files
- **Files with Elasticsearch:** ~2,000-5,000 files
- **Examples extracted:** ~10,000-25,000 examples
- **After deduplication:** ~7,000-15,000 unique examples

### Distribution
- **Query DSL:** ~60% (most common)
- **Mappings:** ~20%
- **Pipelines:** ~15%
- **Aggregations:** ~5%

## Troubleshooting

### Error: "No HuggingFace token found"

**Solution:**
```bash
# Set token as environment variable
$env:HF_TOKEN="your_token_here"

# Or login with CLI
huggingface-cli login
```

### Error: "You need to accept the conditions"

**Solution:**
1. Visit https://huggingface.co/datasets/bigcode/the-stack
2. Click "Access repository"
3. Accept the terms of use
4. Try again

### Error: "ModuleNotFoundError: No module named 'datasets'"

**Solution:**
```bash
pip install datasets
```

### Low Extraction Rate

If you're getting very few examples:

1. **Increase limit:**
   ```bash
   python scripts/collect_the_stack_elasticsearch.py --limit 100000
   ```

2. **Check keywords:** The script searches for Elasticsearch-related keywords. If your code uses different patterns, you may need to adjust the keywords in the script.

3. **Verify language support:** Currently supports Python, JavaScript, TypeScript, Java, Go, Ruby. Other languages may need additional extraction patterns.

## Integration with Existing Dataset

The collected examples will be automatically integrated when you run:

```bash
python preprocess.py --all
```

The preprocessing script will:
1. Load examples from `datasets/raw/the_stack_elasticsearch/`
2. Convert to ChatML format
3. Validate JSON/DSL syntax
4. Deduplicate against existing examples
5. Merge with other sources

## File Structure

After collection, you'll have:

```
expert-elastic/
├── datasets/
│   ├── raw/
│   │   └── the_stack_elasticsearch/
│   │       ├── the_stack_elasticsearch.jsonl      # Collected examples
│   │       └── the_stack_elasticsearch_metadata.json  # Metadata
│   └── train.jsonl  # Final processed dataset (after preprocessing)
```

## Performance Tips

1. **Use streaming mode:** The script uses streaming mode by default, so it doesn't download the entire dataset.

2. **Start small:** Test with `--limit 1000` first to verify everything works.

3. **Process in batches:** For very large collections, consider processing in batches:
   ```bash
   python scripts/collect_the_stack_elasticsearch.py --limit 10000 --output batch1.jsonl
   python scripts/collect_the_stack_elasticsearch.py --limit 10000 --output batch2.jsonl
   # Then merge batches
   ```

4. **Monitor disk space:** The Stack is large. Make sure you have enough disk space.

## Next Steps

After collecting The Stack examples:

1. ✅ Run preprocessing: `python preprocess.py --all`
2. ✅ Validate dataset: `python scripts/validate_dataset.py`
3. ✅ Check statistics: Review `datasets/metadata.json`
4. ✅ Train expert: `../../cli/target/release/expert-cli train`

## References

- **The Stack Dataset:** https://huggingface.co/datasets/bigcode/the-stack
- **The Stack Paper:** https://arxiv.org/abs/2211.15533
- **BigCode Project:** https://www.bigcode-project.org/
- **HuggingFace Datasets:** https://huggingface.co/docs/datasets/

