# Dataset Expansion Summary - Expert Elastic

## Quick Overview

**Current Dataset:** 9,562 examples
**Target:** 50,000-60,000 examples (similar to expert-sql: 147k)

## Top 4 Priority Datasets

### 1. Elasticsearch Official Documentation ⭐⭐⭐⭐⭐ (CRITICAL - NEW)

**Why:** Official source, comprehensive, high quality
- **Size:** 2,000-3,000 examples
- **Content:** All query types, mappings, aggregations, pipelines
- **Effort:** Low-Medium (script ready!)
- **Impact:** +2,000-3,000 examples
- **Status:** ✅ Script `collect_documentation.py` created and ready

**Action:** Run `python scripts/collect_documentation.py`

---

### 2. Text-to-ES Bench ⭐⭐⭐⭐⭐ (CRITICAL)

**Why:** Largest and most relevant dataset specifically for Elasticsearch
- **Size:** ~37,000 examples (LED: 26k + BirdES: 11k)
- **Quality:** Academic benchmark, high quality
- **Format:** Already text-to-query pairs
- **Effort:** Medium (format conversion)
- **Impact:** +30,000 examples

**Action:** Search GitHub for "Text-to-ES Bench" or "text-to-es-bench" repository

---

### 3. Elastic Integrations (Fix Script) ⭐⭐⭐⭐⭐ (CRITICAL)

**Why:** Highest potential if script works
- **Size:** 10,000-15,000 examples
- **Content:** Mappings + pipelines from official integrations
- **Effort:** Medium-High (debug script)
- **Impact:** +10,000-15,000 examples

**Action:** Debug `scripts/collect_integrations.py` - currently returns 0 examples

---

### 4. Synthetic Generation Expansion ⭐⭐⭐⭐ (HIGH)

**Why:** Easy to generate, high impact
- **Size:** +5,000-10,000 examples
- **Content:** More patterns, pipelines, complex queries
- **Effort:** Low (scripting)
- **Impact:** +5,000-10,000 examples

**Action:** Expand `scripts/generate_dsl_examples.py` and add pipeline generators

---

## Expected Results

### Phase 1 (Critical)
- **Official Documentation:** +2,500 (NEW - script ready!)
- Text-to-ES Bench: +30,000
- Integrations (fixed): +12,000
- Synthetic expansion: +5,000
- **Total:** +49,500 examples
- **New total:** ~59,000 examples

### Phase 2 (Official Sources)
- REST API Specs: +2,000 (NEW)
- Test Fixtures: +1,500 (NEW)
- GitHub examples: +1,500
- Query logs: +750
- **Total:** +5,750 examples
- **New total:** ~64,750 examples

### Phase 3 (Enhancements)
- Client examples: +750 (NEW)
- ECS expansion: +750
- Kibana expansion: +350
- Stack examples: +750
- **Total:** +2,600 examples
- **Final total:** ~67,350 examples

### Final Target: ~65,000-70,000 examples ✅

---

## Implementation Order

1. **Week 1:** Text-to-ES Bench + Fix Integrations + Expand Synthetic
2. **Week 2:** GitHub Examples + Documentation + Query Logs
3. **Week 3:** ECS Expansion + Kibana Expansion + Stack Examples

---

## Key Files

- **Analysis:** `docs/DATASET_EXPANSION_ANALYSIS.md` (detailed)
- **Script to fix:** `scripts/collect_integrations.py`
- **Script to expand:** `scripts/generate_dsl_examples.py`

