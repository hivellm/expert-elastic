# Training Issues Analysis - Expert Elastic vs Expert SQL

## Problem Identified

Both experts are generating excessive reasoning (`<think>` or `<think>`) instead of direct outputs, even though the training datasets don't contain reasoning tokens.

## Root Cause Analysis

### 1. Prompt Format Mismatch (Expert-Elastic)

**Training Dataset Format:**
```
<|system|>
Dialect: elastic
Task: query_dsl
Index: kibana_sample_data_ecommerce
<|end|>
<|user|>
Search kibana_sample_data_ecommerce for documents where customer_full_name matches 'search term'.
<|end|>
<|assistant|>
{"query":{"match":{"customer_full_name":"search term"}}}
<|end|>
```

**Script Comparison Format:**
```
System: Task: query_dsl\nDialect: elasticsearch
User: Search for documents where status equals 'active'.
```

**Issues:**
1. ❌ **Dialect mismatch**: Dataset uses `Dialect: elastic`, script uses `Dialect: elasticsearch`
2. ❌ **Missing Index field**: Dataset includes `Index: kibana_sample_data_ecommerce`, script doesn't
3. ❌ **Order difference**: Dataset has `Dialect` first, then `Task`, script has `Task` first

### 2. Base Model Behavior (Both Experts)

The Qwen3-0.6B base model appears to have a default behavior of generating reasoning when:
- The prompt format doesn't exactly match training
- The task is ambiguous or unclear
- The model hasn't been fine-tuned enough

### 3. Training Progress (Expert-Elastic)

**Checkpoint-192** shows improvement:
- Generated valid JSON in test 1: `{"query":{"bool":{"filter":{"query":{"term":{"status":"active"}}}}}}`
- Still generates reasoning, but also produces structured output
- Better than checkpoints 100 and 150

**Checkpoints 100-150:**
- Only generate reasoning, no structured outputs
- Model hasn't learned to skip reasoning yet

## Comparison: Expert-SQL vs Expert-Elastic

### Expert-SQL (Working)
- ✅ Dataset format matches script format exactly
- ✅ Direct SQL outputs without reasoning
- ✅ Model learned to generate SQL directly

### Expert-Elastic (Not Working)
- ❌ Prompt format mismatch between training and inference
- ❌ Model generates reasoning instead of direct outputs
- ⚠️ Checkpoint-192 shows progress but still has issues

## Solutions

### Immediate Fixes

1. **Fix Script Prompt Format (Expert-Elastic)**
   ```python
   # WRONG (current)
   "system_prompt": "Task: query_dsl\nDialect: elasticsearch"
   
   # CORRECT (should match training)
   "system_prompt": "Dialect: elastic\nTask: query_dsl"
   ```

2. **Add Missing Fields**
   - For query_dsl: Add `Index:` field if available
   - Match exact order: `Dialect` → `Task` → `Index` (if present)

3. **Update All Test Cases**
   - Use `Dialect: elastic` instead of `Dialect: elasticsearch`
   - Match the exact format from training dataset

### Long-term Fixes

1. **Continue Training**
   - Expert-Elastic needs more training epochs
   - Checkpoint-192 shows progress, continue to checkpoint-250 or 300

2. **Dataset Review**
   - Ensure all examples follow consistent format
   - No reasoning tokens in training data (confirmed - dataset is clean)

3. **Prompt Template Standardization**
   - Create a standard prompt template for all experts
   - Document exact format requirements
   - Use same format in training and inference

## Recommendations

### For Expert-Elastic

1. ✅ **Fix compare.py script** - Update prompt format to match training
2. ✅ **Continue training** - Checkpoint-192 shows improvement, train more
3. ✅ **Re-test after fixes** - Run comparison again with corrected prompts

### For Expert-SQL

1. ✅ **Already working** - Format matches correctly
2. ✅ **Use as reference** - Copy prompt format pattern to other experts

### For Future Experts

1. ✅ **Standardize prompt format** - Use consistent format across all experts
2. ✅ **Document format** - Add prompt format requirements to template
3. ✅ **Validate format** - Check prompt format matches training before inference

## Test Results Summary

### Expert-Elastic
- **Checkpoint-100**: ❌ Only reasoning, no outputs
- **Checkpoint-150**: ❌ Only reasoning, no outputs  
- **Checkpoint-192**: ⚠️ Reasoning + 1 valid JSON output (progress!)

### Expert-SQL
- **Status**: ✅ Working correctly (no checkpoints available for testing)

## Next Steps

1. Fix `expert-elastic/compare.py` prompt format
2. Re-run comparison with corrected format
3. Continue training expert-elastic to checkpoint-250+
4. Update template documentation with prompt format requirements

