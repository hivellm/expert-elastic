#!/usr/bin/env python3
"""
Elasticsearch Official Documentation Collector

Scrapes examples from Elasticsearch official documentation.
Extracts query DSL examples, mappings, aggregations, and pipelines.

Source: https://www.elastic.co/guide/en/elasticsearch/reference/current/
Output: ~1,000-2,000 examples
"""

import json
import requests
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse

OUTPUT_DIR = Path(__file__).parent.parent / "datasets" / "raw" / "documentation"
DOC_BASE_URL = "https://www.elastic.co/guide/en/elasticsearch/reference/current/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Key documentation pages with examples
DOC_PAGES = [
    "query-dsl.html",
    "query-dsl-term-query.html",
    "query-dsl-match-query.html",
    "query-dsl-bool-query.html",
    "query-dsl-range-query.html",
    "query-dsl-exists-query.html",
    "query-dsl-wildcard-query.html",
    "query-dsl-prefix-query.html",
    "query-dsl-multi-match-query.html",
    "query-dsl-nested-query.html",
    "mapping.html",
    "mapping-types.html",
    "mapping-params.html",
    "mapping-fields.html",
    "search-aggregations.html",
    "search-aggregations-bucket-terms-aggregation.html",
    "search-aggregations-bucket-datehistogram-aggregation.html",
    "search-aggregations-metrics-avg-aggregation.html",
    "search-aggregations-metrics-sum-aggregation.html",
    "search-aggregations-metrics-cardinality-aggregation.html",
    "ingest.html",
    "ingest-processors.html",
    "geoip-processor.html",
    "grok-processor.html",
    "date-processor.html",
    "rename-processor.html",
    "set-processor.html",
    "index-templates.html",
    "indices-templates.html",
]


def extract_json_from_code_block(code_block: str) -> Optional[Dict[str, Any]]:
    """Extract JSON from code block"""
    # Find the first opening brace
    start_idx = code_block.find('{')
    if start_idx == -1:
        return None
    
    # Find matching closing brace by counting braces
    brace_count = 0
    end_idx = start_idx
    
    for i in range(start_idx, len(code_block)):
        if code_block[i] == '{':
            brace_count += 1
        elif code_block[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx = i + 1
                break
    
    if brace_count != 0:
        return None
    
    json_text = code_block[start_idx:end_idx]
    
    # Try to parse as JSON
    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        # Try cleaning up common issues
        json_text = json_text.replace('\n', ' ').replace('\t', ' ')
        # Remove trailing commas before closing braces/brackets
        json_text = re.sub(r',\s*}', '}', json_text)
        json_text = re.sub(r',\s*]', ']', json_text)
        try:
            return json.loads(json_text)
        except:
            pass
    
    return None


def extract_query_examples(html_content: str, page_url: str) -> List[Dict[str, Any]]:
    """Extract query DSL examples from HTML"""
    examples = []
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all <pre> tags (Elasticsearch docs use <pre> for code blocks)
    pre_blocks = soup.find_all('pre')
    
    for pre_block in pre_blocks:
        code_text = pre_block.get_text().strip()
        
        # Skip if too short or doesn't look like JSON
        if len(code_text) < 20 or '{' not in code_text:
            continue
        
        # Remove HTTP method lines (GET, PUT, POST) and URLs
        lines = code_text.split('\n')
        json_lines = []
        skip_until_brace = False
        
        for line in lines:
            line = line.strip()
            # Skip HTTP method lines
            if line.startswith(('GET ', 'PUT ', 'POST ', 'DELETE ')):
                skip_until_brace = True
                continue
            # Skip URL lines
            if line.startswith('/') or line.startswith('http'):
                continue
            # Start collecting after first brace
            if '{' in line:
                skip_until_brace = False
            if not skip_until_brace:
                json_lines.append(line)
        
        json_text = '\n'.join(json_lines)
        
        # Try to extract JSON
        json_obj = extract_json_from_code_block(json_text)
        if json_obj and isinstance(json_obj, dict):
            # Check if it looks like a query, mapping, or pipeline
            if 'query' in json_obj or 'aggs' in json_obj or 'mappings' in json_obj or 'processors' in json_obj or 'index_patterns' in json_obj:
                # Try to find description from surrounding text
                description = ""
                parent = pre_block.find_parent()
                if parent:
                    # Look for heading or paragraph before code block
                    prev = parent.find_previous(['h1', 'h2', 'h3', 'h4', 'h5', 'p'])
                    if prev:
                        description = prev.get_text().strip()[:200]
                
                # Also try to get page title
                if not description:
                    title_tag = soup.find('title')
                    if title_tag:
                        description = title_tag.get_text().strip()
                
                if not description:
                    description = f"Example from {page_url}"
                
                examples.append({
                    "json": json_obj,
                    "description": description,
                    "source_url": page_url,
                    "raw_code": code_text[:500]
                })
    
    return examples


def fetch_documentation_page(page: str) -> Optional[str]:
    """Fetch a documentation page"""
    url = urljoin(DOC_BASE_URL, page)
    
    try:
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"  Error fetching {page}: {e}")
        return None


def generate_instruction_from_example(example: Dict[str, Any], page_url: str) -> str:
    """Generate natural language instruction from example"""
    json_obj = example["json"]
    description = example.get("description", "")
    
    # Try to extract meaningful instruction from description
    if description and len(description) > 20:
        # Clean up description
        instruction = re.sub(r'\s+', ' ', description)
        instruction = instruction.split('.')[0]  # Take first sentence
        if len(instruction) > 10:
            return instruction
    
    # Generate from JSON structure
    if 'query' in json_obj:
        query_type = list(json_obj['query'].keys())[0] if isinstance(json_obj['query'], dict) else 'query'
        return f"Create a {query_type} query"
    elif 'aggs' in json_obj:
        agg_type = list(json_obj['aggs'].keys())[0] if isinstance(json_obj['aggs'], dict) else 'aggregation'
        return f"Create an aggregation query with {agg_type}"
    elif 'mappings' in json_obj:
        return "Create an index mapping"
    elif 'processors' in json_obj:
        return "Create an ingest pipeline"
    
    return f"Example from Elasticsearch documentation"


def determine_task_type(json_obj: Dict[str, Any]) -> str:
    """Determine task type from JSON structure"""
    if 'mappings' in json_obj or 'index_patterns' in json_obj:
        return "mapping_create"
    elif 'processors' in json_obj:
        return "pipeline_create"
    elif 'query' in json_obj or 'aggs' in json_obj:
        return "query_dsl"
    else:
        return "query_dsl"  # Default


def collect_documentation():
    """Main collection function"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("="*70)
    print("Elasticsearch Official Documentation Collection")
    print("="*70)
    print(f"Base URL: {DOC_BASE_URL}")
    print(f"Pages to scrape: {len(DOC_PAGES)}")
    print("="*70)
    
    all_examples = []
    successful_pages = 0
    failed_pages = 0
    
    for i, page in enumerate(DOC_PAGES, 1):
        print(f"\n[{i}/{len(DOC_PAGES)}] Fetching {page}...", end=" ", flush=True)
        
        html_content = fetch_documentation_page(page)
        if not html_content:
            failed_pages += 1
            print("[FAILED]")
            continue
        
        examples = extract_query_examples(html_content, urljoin(DOC_BASE_URL, page))
        all_examples.extend(examples)
        successful_pages += 1
        print(f"[OK] Found {len(examples)} examples")
        
        # Rate limiting
        time.sleep(1)
    
    print(f"\n{'='*70}")
    print(f"Collection Summary:")
    print(f"  Successful pages: {successful_pages}/{len(DOC_PAGES)}")
    print(f"  Failed pages: {failed_pages}")
    print(f"  Total examples found: {len(all_examples)}")
    print(f"{'='*70}")
    
    # Convert to training format
    training_examples = []
    for example in all_examples:
        json_obj = example["json"]
        task_type = determine_task_type(json_obj)
        instruction = generate_instruction_from_example(example, example["source_url"])
        
        training_example = {
            "task": task_type,
            "domain": "elasticsearch/official-docs",
            "instruction": instruction,
            "output": json.dumps(json_obj, ensure_ascii=False, separators=(',', ':')),
            "source": "elasticsearch/documentation",
            "source_url": example["source_url"]
        }
        
        training_examples.append(training_example)
    
    # Save examples
    output_file = OUTPUT_DIR / "documentation_examples.jsonl"
    print(f"\nSaving {len(training_examples)} examples to {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in training_examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    # Save metadata
    metadata = {
        "source": "Elasticsearch Official Documentation",
        "base_url": DOC_BASE_URL,
        "pages_scraped": successful_pages,
        "pages_failed": failed_pages,
        "total_examples": len(training_examples),
        "task_distribution": {
            task: sum(1 for e in training_examples if e["task"] == task)
            for task in ["query_dsl", "mapping_create", "pipeline_create"]
        }
    }
    
    metadata_file = OUTPUT_DIR / "metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"[OK] Documentation collection complete!")
    print(f"     Total examples: {len(training_examples)}")
    print(f"     Output: {output_file}")
    print(f"{'='*70}")


if __name__ == "__main__":
    collect_documentation()

