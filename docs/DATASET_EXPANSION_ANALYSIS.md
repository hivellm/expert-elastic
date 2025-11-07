# Dataset Expansion Analysis - Expert Elastic

## Current Status

**Dataset:** 9,562 processed examples (from 19,329 raw)
- Query DSL: 8,561 (89.5%)
- Mapping creation: 363 (3.8%)
- KQL: 196 (2.0%)
- EQL: 366 (3.8%)
- Pipeline creation: 76 (0.8%)

**Gaps Identified:**
- ⚠️ Integrations: 0 examples (script broken - HIGH PRIORITY)
- ⚠️ Pipeline examples: Only 76 (need more)
- ⚠️ KQL/EQL: Could use more examples
- ⚠️ Real-world production queries: Limited

## Recommended Datasets

### 1. The Stack Dataset (BigCode) ⭐⭐⭐⭐⭐ (HIGHEST PRIORITY - NEW)

**Source:** BigCode The Stack Dataset
- **URL:** https://huggingface.co/datasets/bigcode/the-stack
- **Script:** `scripts/collect_the_stack_elasticsearch.py` (NEW - created)
- **Paper:** https://arxiv.org/abs/2211.15533

**Content:**
- Real-world Elasticsearch code from production codebases
- Query DSL examples embedded in client code (Python, JavaScript, Java, etc.)
- Mapping definitions from actual projects
- Ingest pipeline configurations
- Aggregation queries from real applications

**Advantages:**
- ✅ **Real-world patterns** - Production code from actual projects
- ✅ **Massive scale** - ~3.1 TB of code, potentially 10k-25k Elasticsearch examples
- ✅ **Diverse use cases** - Different domains and applications
- ✅ **Multiple languages** - Python, JavaScript, TypeScript, Java, Go, Ruby
- ✅ **Production quality** - Real code used in production systems

**Integration:**
- Filter files mentioning Elasticsearch keywords
- Extract query DSL, mappings, pipelines from code
- Generate instructions from function/class names and comments
- Validate JSON/DSL syntax
- **Estimated usable:** 10,000-25,000 examples after deduplication

**Priority:** ⭐⭐⭐⭐⭐ CRITICAL - Real production code, massive scale

**Requirements:**
- HuggingFace token (accept terms at dataset page)
- `datasets` library: `pip install datasets`
- Set `HF_TOKEN` environment variable

---

### 2. Elasticsearch Official Documentation ⭐⭐⭐⭐⭐ (HIGHEST PRIORITY - NEW)

**Source:** Elasticsearch Official Documentation
- **URL:** https://www.elastic.co/guide/en/elasticsearch/reference/current/
- **Script:** `scripts/collect_documentation.py` (NEW - created)

**Content:**
- Query DSL examples from every documentation page
- Mapping examples and index templates
- Aggregation examples (terms, date_histogram, metrics)
- Ingest pipeline examples
- Code snippets with natural language descriptions

**Advantages:**
- ✅ **Official source** - Highest quality and accuracy
- ✅ **Comprehensive** - Covers all Elasticsearch features
- ✅ **Up-to-date** - Always current with latest version
- ✅ **Well-documented** - Examples have explanations
- ✅ **Diverse** - All query types, aggregations, mappings

**Integration:**
- Web scraping documentation pages
- Extract JSON code blocks
- Generate natural language from page context
- **Estimated usable:** 2,000-3,000 examples

**Priority:** ⭐⭐⭐⭐⭐ CRITICAL - Official source, comprehensive coverage

---

### 2. Text-to-ES Bench ⭐⭐⭐⭐⭐ (HIGHEST PRIORITY)

**Source:** ACL 2025 Paper - "Text-to-ES Bench: A Comprehensive Benchmark for Text-to-Elasticsearch Query Generation"
- **Paper:** https://aclanthology.org/2025.acl-long.971.pdf
- **GitHub:** Likely available (search for "Text-to-ES Bench" or "text-to-es-bench")

**Content:**
- **LED Dataset:** 26,207 text-to-ES query pairs
- **BirdES Dataset:** 10,962 text-to-ES query pairs (derived from BIRD SQL dataset)
- **Total:** ~37,000 high-quality examples

**Advantages:**
- ✅ Specifically designed for Elasticsearch query generation
- ✅ Large scale (37k examples)
- ✅ Academic benchmark quality
- ✅ Covers diverse query patterns
- ✅ Already formatted for text-to-query tasks

**Integration:**
- Convert format to ChatML
- Extract query DSL, KQL, EQL patterns
- Validate JSON syntax
- **Estimated usable:** 30,000+ examples after deduplication

**Priority:** ⭐⭐⭐⭐⭐ CRITICAL - Largest and most relevant dataset

---

### 2. Database Query Logs Comprehensive Dataset

**Source:** Hugging Face
- **URL:** https://huggingface.co/datasets/robworks-software/database-query-logs-comprehensive
- **Size:** 3,995 query log entries
- **Includes:** Elasticsearch queries (among other databases)

**Content:**
- Real and synthetic database query logs
- 10 major database engines including Elasticsearch
- Performance analysis queries
- Query optimization examples

**Advantages:**
- ✅ Real-world production queries
- ✅ Performance-focused patterns
- ✅ Already on Hugging Face (easy to download)

**Challenges:**
- ⚠️ Mixed database engines (need filtering)
- ⚠️ May need format conversion
- ⚠️ May include non-query logs

**Integration:**
- Filter for Elasticsearch queries only
- Extract text descriptions if available
- Convert to ChatML format
- **Estimated usable:** 500-1,000 Elasticsearch-specific examples

**Priority:** ⭐⭐⭐ MEDIUM - Good for real-world patterns

---

### 3. Elasticsearch Official GitHub Examples

**Source:** GitHub Elastic
- **Repository:** https://github.com/elastic/elasticsearch
- **Locations:**
  - `docs/examples/`
  - `x-pack/plugin/src/test/resources/`
  - `rest-api-spec/src/main/resources/rest-api-spec/api/`

**Content:**
- Official Query DSL examples
- Index mappings
- Complex aggregations
- Ingest pipelines
- Test fixtures

**Advantages:**
- ✅ Official Elastic source
- ✅ High quality, validated examples
- ✅ Covers all major features
- ✅ Apache 2.0 license

**Integration:**
- Parse REST API specs
- Extract examples from documentation
- Generate natural language descriptions
- **Estimated usable:** 1,000-2,000 examples

**Priority:** ⭐⭐⭐⭐ HIGH - Official source, high quality

---

### 4. Elastic Stack Examples Repository

**Source:** GitHub Elastic Examples
- **Repository:** https://github.com/elastic/examples
- **Content:** Real-world use cases and sample data

**Content:**
- Production query patterns
- Domain-specific mappings
- Use case examples (e-commerce, logging, metrics)
- Sample data with queries

**Advantages:**
- ✅ Real-world scenarios
- ✅ Complete examples (data + queries)
- ✅ Multiple domains
- ✅ Apache 2.0 license

**Integration:**
- Extract queries from examples
- Generate natural language descriptions
- **Estimated usable:** 500-1,000 examples

**Priority:** ⭐⭐⭐ MEDIUM - Good for domain diversity

---

### 5. Elastic Package Registry (Integrations) - FIX SCRIPT

**Source:** Elastic Package Registry
- **URL:** https://epr.elastic.co
- **Current Status:** Script broken (0 examples collected)

**Content:**
- Integration packages (nginx, apache, aws, gcp, azure, etc.)
- Fields.yml files → mappings
- Ingest pipelines
- Sample queries

**Potential:**
- **10,000-15,000 examples** (mappings + pipelines)
- **Highest potential** if script is fixed

**Priority:** ⭐⭐⭐⭐⭐ CRITICAL - Fix script immediately

**Top Integrations to Target:**
- nginx, apache (web servers)
- aws, gcp, azure (cloud providers)
- mysql, postgresql (databases)
- kubernetes, docker (containers)
- windows, linux (operating systems)
- security, audit (security domains)

---

### 6. Elasticsearch REST API Spec Examples ⭐⭐⭐⭐ (HIGH)

**Source:** Elasticsearch GitHub Repository
- **Repository:** https://github.com/elastic/elasticsearch
- **Location:** `rest-api-spec/src/main/resources/rest-api-spec/api/`
- **Content:** Official REST API specifications with examples

**Content:**
- Every API endpoint with example requests/responses
- Query DSL examples for each endpoint
- Mapping examples for index operations
- Aggregation examples for search endpoints
- Pipeline examples for ingest endpoints

**Advantages:**
- ✅ **Official API specs** - Guaranteed to work
- ✅ **Complete coverage** - All API endpoints
- ✅ **Structured format** - Easy to parse (YAML)
- ✅ **Request/response pairs** - Shows input/output

**Integration:**
- Clone elasticsearch repository
- Parse YAML API specs
- Extract example requests
- Generate natural language from endpoint names
- **Estimated usable:** 1,500-2,500 examples

**Priority:** ⭐⭐⭐⭐ HIGH - Official API specs, structured format

---

### 7. Elasticsearch Test Fixtures ⭐⭐⭐⭐ (HIGH)

**Source:** Elasticsearch GitHub Repository
- **Repository:** https://github.com/elastic/elasticsearch
- **Locations:**
  - `x-pack/plugin/src/test/resources/`
  - `server/src/test/resources/`
  - `modules/*/src/test/resources/`

**Content:**
- Test data with queries
- Example mappings from tests
- Aggregation test cases
- Pipeline test cases
- Real-world test scenarios

**Advantages:**
- ✅ **Tested examples** - Guaranteed to work
- ✅ **Edge cases** - Covers complex scenarios
- ✅ **Real scenarios** - Based on actual use cases
- ✅ **High quality** - Used in Elasticsearch tests

**Integration:**
- Clone elasticsearch repository
- Parse test resource files
- Extract queries and mappings
- Generate descriptions from test names
- **Estimated usable:** 1,000-2,000 examples

**Priority:** ⭐⭐⭐⭐ HIGH - Tested examples, edge cases

---

### 8. Elasticsearch Client Examples ⭐⭐⭐ (MEDIUM)

**Source:** Elasticsearch Client Libraries
- **Python:** https://github.com/elastic/elasticsearch-py
- **JavaScript:** https://github.com/elastic/elasticsearch-js
- **Java:** https://github.com/elastic/elasticsearch-java

**Content:**
- Client library examples
- Query DSL examples in code
- Mapping examples
- Real-world integration patterns

**Advantages:**
- ✅ **Practical examples** - Real integration patterns
- ✅ **Multiple languages** - Diverse perspectives
- ✅ **Well-documented** - Client library docs

**Integration:**
- Parse example files from client repos
- Extract query DSL from code
- **Estimated usable:** 500-1,000 examples

**Priority:** ⭐⭐⭐ MEDIUM - Practical but may overlap with docs

---

### 7. Kibana Sample Data (Expand)

**Current:** 40 examples
**Potential:** +200-500 examples

**Strategy:**
- Generate more query variations for:
  - eCommerce sample data (100+ queries)
  - Flights sample data (100+ queries)
  - Web Logs sample data (100+ queries)
- Use known schemas to generate diverse queries
- Focus on aggregations, filters, date ranges

**Priority:** ⭐⭐ MEDIUM - Easy to generate, moderate impact

---

### 8. ECS Field Definitions (Expand)

**Current:** 147 examples
**Potential:** +500-1,000 examples

**Strategy:**
- Process ALL ECS fields (not just main schemas)
- Generate mappings for field combinations
- Create queries using ECS fields
- Cover all ECS versions

**Priority:** ⭐⭐⭐ MEDIUM - Good for ECS compliance

---

### 9. Detection Rules (Expand)

**Current:** 224 examples (196 KQL + 366 EQL)
**Potential:** +200-500 examples

**Strategy:**
- Process more categories
- Include deprecated rules (99 found)
- Generate query variations
- Cover more MITRE tactics

**Priority:** ⭐⭐ LOW - Already well covered

---

### 10. Synthetic Generation (Expand Elastic Labs)

**Current:** 6,000 examples
**Potential:** +5,000-10,000 examples

**Strategy:**
- More Query DSL patterns
- More aggregation variations
- More mapping combinations
- More pipeline examples (currently low)
- Complex nested queries
- Multi-index queries

**Priority:** ⭐⭐⭐⭐ HIGH - Easy to generate, high impact

---

## Recommended Expansion Plan

### Phase 1: Critical Datasets (Week 1)

1. **The Stack Dataset** ⭐⭐⭐⭐⭐ (NEW - HIGHEST PRIORITY)
   - Run `collect_the_stack_elasticsearch.py` script
   - Extract Elasticsearch code from production codebases
   - Process Python, JavaScript, TypeScript, Java files
   - **Expected:** +10,000-25,000 examples
   - **Effort:** Medium-High (requires HuggingFace auth, complex extraction)

2. **Elasticsearch Official Documentation** ⭐⭐⭐⭐⭐ (NEW)
   - Run `collect_documentation.py` script
   - Scrape all documentation pages
   - Extract examples and convert to ChatML
   - **Expected:** +2,000-3,000 examples
   - **Effort:** Low-Medium (script ready)

3. **Text-to-ES Bench** ⭐⭐⭐⭐⭐
   - Download and integrate
   - Convert to ChatML format
   - **Expected:** +30,000 examples
   - **Effort:** Medium (format conversion)

3. **Fix Integrations Script** ⭐⭐⭐⭐⭐
   - Debug `collect_integrations.py`
   - Collect top 20 integrations
   - **Expected:** +10,000-15,000 examples
   - **Effort:** Medium-High (debugging)

4. **Expand Synthetic Generation** ⭐⭐⭐⭐
   - Add more templates
   - Focus on pipelines and complex queries
   - **Expected:** +5,000 examples
   - **Effort:** Low (scripting)

**Phase 1 Total:** +57,000-68,000 examples
**New Total:** ~66,500-77,500 examples

---

### Phase 2: Official Sources (Week 2)

5. **Elasticsearch REST API Specs** ⭐⭐⭐⭐ (NEW)
   - Clone elasticsearch repository
   - Parse REST API YAML specs
   - Extract example requests
   - **Expected:** +1,500-2,500 examples
   - **Effort:** Medium (YAML parsing)

6. **Elasticsearch Test Fixtures** ⭐⭐⭐⭐ (NEW)
   - Parse test resource files
   - Extract queries and mappings
   - **Expected:** +1,000-2,000 examples
   - **Effort:** Medium (file parsing)

7. **Elasticsearch GitHub Examples** ⭐⭐⭐⭐
   - Parse official examples
   - Extract queries and mappings
   - **Expected:** +1,000-2,000 examples
   - **Effort:** Medium (parsing)

8. **Database Query Logs Dataset** ⭐⭐⭐
   - Filter Elasticsearch queries
   - Convert format
   - **Expected:** +500-1,000 examples
   - **Effort:** Low-Medium (filtering)

**Phase 2 Total:** +4,000-7,500 examples
**New Total:** ~60,500-70,000 examples

---

### Phase 3: Enhancements (Week 3)

9. **Elasticsearch Client Examples** ⭐⭐⭐ (NEW)
   - Parse client library examples
   - Extract query DSL from code
   - **Expected:** +500-1,000 examples
   - **Effort:** Medium

10. **Expand ECS** ⭐⭐⭐
    - Process all ECS fields
    - Generate combinations
    - **Expected:** +500-1,000 examples
    - **Effort:** Low-Medium

11. **Expand Kibana Samples** ⭐⭐
    - Generate more variations
    - **Expected:** +200-500 examples
    - **Effort:** Low

12. **Elastic Stack Examples** ⭐⭐⭐
    - Extract from examples repo
    - **Expected:** +500-1,000 examples
    - **Effort:** Medium

**Phase 3 Total:** +1,700-3,500 examples
**Final Total:** ~62,200-73,500 examples

---

## Dataset Comparison

| Dataset | Examples | Quality | Effort | Priority | Status |
|---------|----------|---------|--------|----------|--------|
| **The Stack** | 10,000-25,000 | ⭐⭐⭐⭐ | Medium-High | ⭐⭐⭐⭐⭐ | ✅ Script ready |
| **Official Documentation** | 2,000-3,000 | ⭐⭐⭐⭐⭐ | Low-Medium | ⭐⭐⭐⭐⭐ | ✅ Script ready |
| Text-to-ES Bench | 30,000+ | ⭐⭐⭐⭐⭐ | Medium | ⭐⭐⭐⭐⭐ | 🔍 Need to find |
| Integrations (fix) | 10,000-15,000 | ⭐⭐⭐⭐ | Medium-High | ⭐⭐⭐⭐⭐ | ⚠️ Script broken |
| REST API Specs | 1,500-2,500 | ⭐⭐⭐⭐⭐ | Medium | ⭐⭐⭐⭐ | 📝 Need script |
| Test Fixtures | 1,000-2,000 | ⭐⭐⭐⭐⭐ | Medium | ⭐⭐⭐⭐ | 📝 Need script |
| Synthetic Expansion | 5,000-10,000 | ⭐⭐⭐ | Low | ⭐⭐⭐⭐ | ✅ Easy to expand |
| GitHub Examples | 1,000-2,000 | ⭐⭐⭐⭐⭐ | Medium | ⭐⭐⭐⭐ | ✅ Script exists |
| Client Examples | 500-1,000 | ⭐⭐⭐ | Medium | ⭐⭐⭐ | 📝 Need script |
| Query Logs | 500-1,000 | ⭐⭐⭐ | Low-Medium | ⭐⭐⭐ | 📥 Download ready |
| ECS Expansion | 500-1,000 | ⭐⭐⭐ | Low-Medium | ⭐⭐⭐ | ✅ Easy to expand |
| Kibana Expansion | 200-500 | ⭐⭐⭐ | Low | ⭐⭐ | ✅ Easy to expand |
| Stack Examples | 500-1,000 | ⭐⭐⭐ | Medium | ⭐⭐⭐ | 📝 Need script |

**Legend:**
- ✅ Ready/Working
- 🔍 Need to locate
- ⚠️ Needs fixing
- 📝 Need to create script
- 📥 Download available

---

## Implementation Checklist

### Immediate Actions

- [x] **Create `collect_the_stack_elasticsearch.py` script** ✅
  - Script created and ready to use
  - Extracts Elasticsearch code from The Stack dataset
  - Supports Python, JavaScript, TypeScript, Java, Go, Ruby
  - **Action:** Run script (requires HuggingFace token)

- [x] **Create `collect_documentation.py` script** ✅
  - Script created and ready to use
  - Scrapes official Elasticsearch documentation
  - Extracts examples from all pages
  - **Action:** Run script to collect examples

- [ ] **Run The Stack collection**
  - Accept terms at https://huggingface.co/datasets/bigcode/the-stack
  - Set HF_TOKEN environment variable
  - Execute: `python scripts/collect_the_stack_elasticsearch.py --limit 50000`
  - Expected: +10,000-25,000 examples

- [ ] **Run documentation collection**
  - Execute: `python scripts/collect_documentation.py`
  - Expected: +2,000-3,000 examples
  - Validate output format

- [ ] **Search for Text-to-ES Bench GitHub repository**
  - Check if dataset is publicly available
  - Download LED and BirdES datasets
  - Analyze format and structure

- [ ] **Fix `collect_integrations.py` script**
  - Debug why it returns 0 examples
  - Test with single integration first
  - Verify output format

- [ ] **Expand synthetic generation**
  - Add pipeline templates
  - Add complex query patterns
  - Increase iterations

### Short-term Actions

- [ ] **Create script for REST API specs**
  - Clone elasticsearch repository
  - Parse YAML API specs from `rest-api-spec/`
  - Extract example requests
  - Generate natural language from endpoint names

- [ ] **Create script for test fixtures**
  - Parse test resource files
  - Extract queries and mappings
  - Generate descriptions from test names

- [ ] **Create script for client examples**
  - Parse elasticsearch-py examples
  - Parse elasticsearch-js examples
  - Extract query DSL from code

- [ ] **Download Database Query Logs**
  - Filter for Elasticsearch
  - Convert format
  - Validate queries

### Long-term Actions

- [ ] **Expand ECS collection**
  - Process all fields
  - Generate combinations

- [ ] **Expand Kibana samples**
  - Generate more variations

- [ ] **Collect Stack Examples**
  - Extract from examples repo

---

## Expected Outcomes

### Before Expansion
- **Current:** 9,562 examples
- **Query DSL:** 8,561 (89.5%)
- **Mappings:** 363 (3.8%)
- **KQL:** 196 (2.0%)
- **EQL:** 366 (3.8%)
- **Pipelines:** 76 (0.8%)

### After Phase 1
- **Total:** ~54,000-59,000 examples
- **Query DSL:** ~45,000+ (80%+)
- **Mappings:** ~12,000+ (20%+)
- **KQL:** ~500+ (1%+)
- **EQL:** ~1,000+ (2%+)
- **Pipelines:** ~5,000+ (10%+)

### After All Phases
- **Total:** ~57,000-66,000 examples
- **Better balance** across all task types
- **Higher quality** from official sources
- **More real-world** patterns

---

## References

### Official Sources
- **Elasticsearch Documentation:** https://www.elastic.co/guide/en/elasticsearch/reference/current/
- **Elasticsearch GitHub:** https://github.com/elastic/elasticsearch
- **REST API Specs:** https://github.com/elastic/elasticsearch/tree/main/rest-api-spec/src/main/resources/rest-api-spec/api
- **Elastic Examples:** https://github.com/elastic/examples
- **Elastic Package Registry:** https://epr.elastic.co
- **Elasticsearch Python Client:** https://github.com/elastic/elasticsearch-py
- **Elasticsearch JavaScript Client:** https://github.com/elastic/elasticsearch-js

### Academic Datasets
- **Text-to-ES Bench Paper:** https://aclanthology.org/2025.acl-long.971.pdf
- **Text-to-ES Bench (search GitHub):** Look for "text-to-es-bench" or "Text-to-ES Bench"

### Public Datasets
- **The Stack (BigCode):** https://huggingface.co/datasets/bigcode/the-stack
- **The Stack Paper:** https://arxiv.org/abs/2211.15533
- **Database Query Logs:** https://huggingface.co/datasets/robworks-software/database-query-logs-comprehensive
- **Elastic Detection Rules:** https://github.com/elastic/detection-rules
- **ECS Repository:** https://github.com/elastic/ecs

---

## Notes

- All datasets should be validated (JSON syntax, DSL syntax)
- Maintain ChatML format for consistency
- Deduplicate by task+instruction hash
- Create train/validation/test splits (80/10/10)
- Focus on English-only examples
- Prioritize quality over quantity

