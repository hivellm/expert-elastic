#!/usr/bin/env python3
"""
Synthetic KQL/EQL/Pipeline Generator

Generates synthetic examples for KQL, EQL, and ingest pipelines to increase coverage.

Output: ~2k KQL + ~1k EQL + ~2k Pipeline examples
"""

import json
from pathlib import Path
from typing import Dict, List, Any
import random

OUTPUT_DIR = Path("../datasets/raw/synthetic_kql_eql_pipelines")

# KQL Templates
KQL_TEMPLATES = [
    {
        "instruction_pt": "Detectar processos executando {process_name}.",
        "instruction_en": "Detect processes running {process_name}.",
        "kql": "process.name: \"{process_name}\" and event.category: process"
    },
    {
        "instruction_pt": "Encontrar eventos onde {field} contém {value}.",
        "instruction_en": "Find events where {field} contains {value}.",
        "kql": "{field}: *{value}*"
    },
    {
        "instruction_pt": "Buscar logs de erro do serviço {service}.",
        "instruction_en": "Search error logs from service {service}.",
        "kql": "service.name: \"{service}\" and log.level: error"
    },
    {
        "instruction_pt": "Detectar conexões de rede para porta {port}.",
        "instruction_en": "Detect network connections to port {port}.",
        "kql": "destination.port: {port} and event.category: network"
    },
    {
        "instruction_pt": "Encontrar eventos de autenticação falhada.",
        "instruction_en": "Find failed authentication events.",
        "kql": "event.category: authentication and event.outcome: failure"
    },
    {
        "instruction_pt": "Buscar arquivos modificados nos últimos {hours} horas.",
        "instruction_en": "Search files modified in the last {hours} hours.",
        "kql": "event.category: file and event.action: modification and @timestamp >= now-{hours}h"
    },
    {
        "instruction_pt": "Detectar processos criados por usuário {user}.",
        "instruction_en": "Detect processes created by user {user}.",
        "kql": "process.name: * and user.name: \"{user}\" and event.type: start"
    },
    {
        "instruction_pt": "Encontrar requisições HTTP com status {status}.",
        "instruction_en": "Find HTTP requests with status {status}.",
        "kql": "http.response.status_code: {status} and event.category: web"
    },
    {
        "instruction_pt": "Buscar eventos de segurança com risco alto.",
        "instruction_en": "Search security events with high risk.",
        "kql": "event.category: security and risk.score: >= 70"
    },
    {
        "instruction_pt": "Detectar downloads de arquivos executáveis.",
        "instruction_en": "Detect downloads of executable files.",
        "kql": "event.action: file_download and file.extension: (\"exe\" or \"dll\" or \"bat\")"
    },
    {
        "instruction_pt": "Encontrar conexões de IPs suspeitos.",
        "instruction_en": "Find connections from suspicious IPs.",
        "kql": "source.ip: ({ip1} or {ip2} or {ip3}) and event.category: network"
    },
    {
        "instruction_pt": "Buscar eventos de sistema no host {host}.",
        "instruction_en": "Search system events on host {host}.",
        "kql": "host.name: \"{host}\" and event.category: (process or file or network)"
    },
    {
        "instruction_pt": "Detectar alterações em arquivos de configuração.",
        "instruction_en": "Detect changes to configuration files.",
        "kql": "file.path: (*config* or *.conf or *.ini) and event.action: modification"
    },
    {
        "instruction_pt": "Encontrar processos com argumentos suspeitos.",
        "instruction_en": "Find processes with suspicious arguments.",
        "kql": "process.args: (*powershell* or *cmd* or *wscript*) and event.type: start"
    },
    {
        "instruction_pt": "Buscar eventos de DNS para domínio {domain}.",
        "instruction_en": "Search DNS events for domain {domain}.",
        "kql": "dns.question.name: *{domain}* and event.category: network"
    }
]

# EQL Templates
EQL_TEMPLATES = [
    {
        "instruction_pt": "Detectar processo criado após download de arquivo pelo mesmo usuário.",
        "instruction_en": "Detect process created after file download by same user.",
        "eql": "sequence by user.name with maxspan=5m\n  [file where event.action == \"file_download\"]\n  [process where event.type == \"start\"]"
    },
    {
        "instruction_pt": "Encontrar sequência de autenticação falhada seguida de sucesso.",
        "instruction_en": "Find sequence of failed authentication followed by success.",
        "eql": "sequence by user.name with maxspan=10m\n  [authentication where event.outcome == \"failure\"]\n  [authentication where event.outcome == \"success\"]"
    },
    {
        "instruction_pt": "Detectar múltiplas tentativas de login falhadas.",
        "instruction_en": "Detect multiple failed login attempts.",
        "eql": "sequence by user.name with maxspan=5m\n  [authentication where event.outcome == \"failure\"]\n  [authentication where event.outcome == \"failure\"]\n  [authentication where event.outcome == \"failure\"]"
    },
    {
        "instruction_pt": "Encontrar conexão de rede seguida de processo criado.",
        "instruction_en": "Find network connection followed by process creation.",
        "eql": "sequence by process.entity_id with maxspan=2m\n  [network where event.type == \"connection_started\"]\n  [process where event.type == \"start\"]"
    },
    {
        "instruction_pt": "Detectar arquivo criado e depois executado.",
        "instruction_en": "Detect file created and then executed.",
        "eql": "sequence by file.path with maxspan=10m\n  [file where event.action == \"file_created\"]\n  [process where process.executable == file.path]"
    },
    {
        "instruction_pt": "Encontrar processo que cria arquivo e depois se conecta à rede.",
        "instruction_en": "Find process that creates file then connects to network.",
        "eql": "sequence by process.entity_id with maxspan=5m\n  [file where event.action == \"file_created\"]\n  [network where event.type == \"connection_started\"]"
    },
    {
        "instruction_pt": "Detectar múltiplos processos criados rapidamente pelo mesmo usuário.",
        "instruction_en": "Detect multiple processes created quickly by same user.",
        "eql": "sequence by user.name with maxspan=1m\n  [process where event.type == \"start\"]\n  [process where event.type == \"start\"]\n  [process where event.type == \"start\"]"
    },
    {
        "instruction_pt": "Encontrar download seguido de execução de arquivo.",
        "instruction_en": "Find download followed by file execution.",
        "eql": "sequence by file.path with maxspan=5m\n  [file where event.action == \"file_download\"]\n  [process where process.executable == file.path]"
    }
]

# Pipeline Templates (Expanded)
PIPELINE_TEMPLATES = [
    {
        "instruction_pt": "Crie um pipeline para adicionar geoip ao campo {field}.",
        "instruction_en": "Create a pipeline to add geoip to field {field}.",
        "pipeline": {
            "processors": [
                {"geoip": {"field": "{field}", "target_field": "{field}.geo"}}
            ]
        }
    },
    {
        "instruction_pt": "Defina um pipeline para renomear {old_field} para {new_field}.",
        "instruction_en": "Define a pipeline to rename {old_field} to {new_field}.",
        "pipeline": {
            "processors": [
                {"rename": {"field": "{old_field}", "target_field": "{new_field}"}}
            ]
        }
    },
    {
        "instruction_pt": "Crie um pipeline para fazer parse de grok no campo message.",
        "instruction_en": "Create a pipeline to parse grok on message field.",
        "pipeline": {
            "processors": [
                {"grok": {"field": "message", "patterns": ["%{COMMONAPACHELOG}"]}}
            ]
        }
    },
    {
        "instruction_pt": "Defina um pipeline para adicionar timestamp atual.",
        "instruction_en": "Define a pipeline to add current timestamp.",
        "pipeline": {
            "processors": [
                {"set": {"field": "@timestamp", "value": "{{_ingest.timestamp}}"}}
            ]
        }
    },
    {
        "instruction_pt": "Crie um pipeline para converter string para número no campo {field}.",
        "instruction_en": "Create a pipeline to convert string to number in field {field}.",
        "pipeline": {
            "processors": [
                {"convert": {"field": "{field}", "type": "long"}}
            ]
        }
    },
    {
        "instruction_pt": "Defina um pipeline para remover campos desnecessários.",
        "instruction_en": "Define a pipeline to remove unnecessary fields.",
        "pipeline": {
            "processors": [
                {"remove": {"field": ["temp", "debug", "test"]}}
            ]
        }
    },
    {
        "instruction_pt": "Crie um pipeline para fazer uppercase no campo {field}.",
        "instruction_en": "Create a pipeline to uppercase field {field}.",
        "pipeline": {
            "processors": [
                {"uppercase": {"field": "{field}"}}
            ]
        }
    },
    {
        "instruction_pt": "Defina um pipeline para fazer lowercase no campo {field}.",
        "instruction_en": "Define a pipeline to lowercase field {field}.",
        "pipeline": {
            "processors": [
                {"lowercase": {"field": "{field}"}}
            ]
        }
    },
    {
        "instruction_pt": "Crie um pipeline para fazer trim de espaços no campo {field}.",
        "instruction_en": "Create a pipeline to trim spaces in field {field}.",
        "pipeline": {
            "processors": [
                {"trim": {"field": "{field}"}}
            ]
        }
    },
    {
        "instruction_pt": "Defina um pipeline para fazer parse de user agent.",
        "instruction_en": "Define a pipeline to parse user agent.",
        "pipeline": {
            "processors": [
                {"user_agent": {"field": "user_agent", "target_field": "user_agent.parsed"}}
            ]
        }
    },
    {
        "instruction_pt": "Crie um pipeline para fazer parse de data no formato {format}.",
        "instruction_en": "Create a pipeline to parse date in format {format}.",
        "pipeline": {
            "processors": [
                {"date": {"field": "timestamp", "formats": ["{format}"], "target_field": "@timestamp"}}
            ]
        }
    },
    {
        "instruction_pt": "Defina um pipeline para adicionar campo calculado.",
        "instruction_en": "Define a pipeline to add calculated field.",
        "pipeline": {
            "processors": [
                {"set": {"field": "total", "value": "{{bytes_sent + bytes_received}}"}}
            ]
        }
    },
    {
        "instruction_pt": "Crie um pipeline para fazer split de campo delimitado por vírgula.",
        "instruction_en": "Create a pipeline to split comma-delimited field.",
        "pipeline": {
            "processors": [
                {"split": {"field": "{field}", "separator": ","}}
            ]
        }
    },
    {
        "instruction_pt": "Defina um pipeline para adicionar geoip e user agent parsing.",
        "instruction_en": "Define a pipeline to add geoip and user agent parsing.",
        "pipeline": {
            "processors": [
                {"geoip": {"field": "source.ip", "target_field": "source.geo"}},
                {"user_agent": {"field": "user_agent", "target_field": "user_agent.parsed"}}
            ]
        }
    },
    {
        "instruction_pt": "Crie um pipeline para renomear e converter tipos.",
        "instruction_en": "Create a pipeline to rename and convert types.",
        "pipeline": {
            "processors": [
                {"rename": {"field": "old_name", "target_field": "new_name"}},
                {"convert": {"field": "new_name", "type": "long"}}
            ]
        }
    },
    {
        "instruction_pt": "Defina um pipeline para fazer parse de log Apache.",
        "instruction_en": "Define a pipeline to parse Apache log.",
        "pipeline": {
            "processors": [
                {"grok": {"field": "message", "patterns": ["%{COMMONAPACHELOG}"]}},
                {"date": {"field": "timestamp", "formats": ["dd/MMM/yyyy:HH:mm:ss Z"], "target_field": "@timestamp"}}
            ]
        }
    },
    {
        "instruction_pt": "Crie um pipeline para enriquecer com dados de lookup.",
        "instruction_en": "Create a pipeline to enrich with lookup data.",
        "pipeline": {
            "processors": [
                {"set": {"field": "user.role", "value": "{{lookup('user_roles', user.id)}}"}}
            ]
        }
    },
    {
        "instruction_pt": "Defina um pipeline para fazer parse de JSON aninhado.",
        "instruction_en": "Define a pipeline to parse nested JSON.",
        "pipeline": {
            "processors": [
                {"json": {"field": "data", "target_field": "parsed"}}
            ]
        }
    },
    {
        "instruction_pt": "Crie um pipeline para adicionar tags baseado em condições.",
        "instruction_en": "Create a pipeline to add tags based on conditions.",
        "pipeline": {
            "processors": [
                {"set": {"field": "tags", "value": ["production"], "if": "ctx.environment == 'prod'"}}
            ]
        }
    },
    {
        "instruction_pt": "Defina um pipeline completo para logs de web server.",
        "instruction_en": "Define a complete pipeline for web server logs.",
        "pipeline": {
            "processors": [
                {"grok": {"field": "message", "patterns": ["%{COMMONAPACHELOG}"]}},
                {"geoip": {"field": "client.ip", "target_field": "client.geo"}},
                {"user_agent": {"field": "user_agent", "target_field": "user_agent.parsed"}},
                {"date": {"field": "timestamp", "formats": ["dd/MMM/yyyy:HH:mm:ss Z"], "target_field": "@timestamp"}}
            ]
        }
    }
]

# Sample values
PROCESS_NAMES = ["powershell.exe", "cmd.exe", "regsvr32.exe", "wscript.exe", "mshta.exe", "rundll32.exe", "svchost.exe", "explorer.exe"]
SERVICES = ["nginx", "apache", "mysql", "postgresql", "redis", "elasticsearch", "kibana"]
PORTS = [80, 443, 22, 21, 25, 53, 3306, 5432, 6379, 9200]
USERS = ["admin", "root", "system", "service", "user", "guest"]
STATUS_CODES = [200, 301, 302, 400, 401, 403, 404, 500, 502, 503]
IPS = ["192.168.1.1", "10.0.0.1", "172.16.0.1", "203.0.113.1", "198.51.100.1"]
HOSTS = ["web-server-01", "db-server-01", "app-server-01", "proxy-01"]
DOMAINS = ["example.com", "malicious.com", "suspicious.net", "phishing.org"]
DATE_FORMATS = ["yyyy-MM-dd HH:mm:ss", "dd/MMM/yyyy:HH:mm:ss Z", "ISO8601", "UNIX", "UNIX_MS"]


def generate_kql_examples() -> List[Dict[str, Any]]:
    """Generate KQL examples"""
    examples = []
    
    for template in KQL_TEMPLATES:
        # Generate 50 variations of each template
        for _ in range(50):
            kql = template["kql"]
            instruction = template["instruction_en"]
            
            # Replace placeholders
            kql = kql.replace("{process_name}", random.choice(PROCESS_NAMES))
            kql = kql.replace("{service}", random.choice(SERVICES))
            kql = kql.replace("{port}", str(random.choice(PORTS)))
            kql = kql.replace("{user}", random.choice(USERS))
            kql = kql.replace("{status}", str(random.choice(STATUS_CODES)))
            kql = kql.replace("{host}", random.choice(HOSTS))
            kql = kql.replace("{domain}", random.choice(DOMAINS))
            kql = kql.replace("{hours}", str(random.choice([1, 2, 6, 12, 24])))
            
            if "{field}" in kql:
                fields = ["message", "event.action", "file.name", "process.name", "user.name"]
                values = ["error", "failed", "suspicious", "unauthorized"]
                kql = kql.replace("{field}", random.choice(fields))
                kql = kql.replace("{value}", random.choice(values))
            
            if "{ip1}" in kql:
                kql = kql.replace("{ip1}", random.choice(IPS))
                kql = kql.replace("{ip2}", random.choice(IPS))
                kql = kql.replace("{ip3}", random.choice(IPS))
            
            instruction = instruction.replace("{process_name}", random.choice(PROCESS_NAMES))
            instruction = instruction.replace("{service}", random.choice(SERVICES))
            instruction = instruction.replace("{port}", str(random.choice(PORTS)))
            instruction = instruction.replace("{user}", random.choice(USERS))
            instruction = instruction.replace("{status}", str(random.choice(STATUS_CODES)))
            instruction = instruction.replace("{host}", random.choice(HOSTS))
            instruction = instruction.replace("{domain}", random.choice(DOMAINS))
            instruction = instruction.replace("{hours}", str(random.choice([1, 2, 6, 12, 24])))
            
            if "{field}" in instruction:
                instruction = instruction.replace("{field}", random.choice(["message", "event.action", "file.name"]))
                instruction = instruction.replace("{value}", random.choice(["error", "failed", "suspicious"]))
            
            examples.append({
                "task": "kql",
                "domain": "security",
                "instruction": instruction,
                "output": kql,
                "source": "synthetic/kql"
            })
    
    return examples


def generate_eql_examples() -> List[Dict[str, Any]]:
    """Generate EQL examples"""
    examples = []
    
    for template in EQL_TEMPLATES:
        # Generate 30 variations of each template
        for _ in range(30):
            eql = template["eql"]
            instruction = template["instruction_en"]
            
            # EQL queries are mostly static, but we can vary maxspan
            if "maxspan=" in eql:
                spans = ["1m", "2m", "5m", "10m", "30m", "1h"]
                old_span = [s for s in spans if s in eql][0] if any(s in eql for s in spans) else "5m"
                new_span = random.choice(spans)
                eql = eql.replace(f"maxspan={old_span}", f"maxspan={new_span}")
            
            examples.append({
                "task": "eql",
                "domain": "security",
                "instruction": instruction,
                "output": eql,
                "source": "synthetic/eql"
            })
    
    return examples


def generate_pipeline_examples() -> List[Dict[str, Any]]:
    """Generate pipeline examples"""
    examples = []
    
    ip_fields = ["source.ip", "destination.ip", "client.ip", "server.ip", "remote.ip"]
    old_new_pairs = [
        ("message", "log.message"),
        ("timestamp", "@timestamp"),
        ("host", "host.name"),
        ("service", "service.name"),
        ("user", "user.name"),
        ("ip", "source.ip")
    ]
    fields_to_convert = ["status_code", "port", "count", "duration", "bytes"]
    fields_to_transform = ["message", "user.name", "service.name", "host.name"]
    
    for template in PIPELINE_TEMPLATES:
        # Generate 50 variations of each template
        for _ in range(50):
            pipeline_str = json.dumps(template["pipeline"], ensure_ascii=False)
            instruction = template["instruction_en"]
            
            # Replace placeholders
            if "{field}" in pipeline_str:
                field = random.choice(ip_fields + fields_to_transform)
                pipeline_str = pipeline_str.replace("{field}", field)
                instruction = instruction.replace("{field}", field)
            
            if "{old_field}" in pipeline_str:
                old_field, new_field = random.choice(old_new_pairs)
                pipeline_str = pipeline_str.replace("{old_field}", old_field)
                pipeline_str = pipeline_str.replace("{new_field}", new_field)
                instruction = instruction.replace("{old_field}", old_field)
                instruction = instruction.replace("{new_field}", new_field)
            
            if "{format}" in pipeline_str:
                fmt = random.choice(DATE_FORMATS)
                pipeline_str = pipeline_str.replace("{format}", fmt)
                instruction = instruction.replace("{format}", fmt)
            
            try:
                pipeline = json.loads(pipeline_str)
                examples.append({
                    "task": "pipeline_create",
                    "domain": "general",
                    "instruction": instruction,
                    "output": json.dumps(pipeline, ensure_ascii=False, separators=(',', ':')),
                    "source": "synthetic/pipelines"
                })
            except:
                pass
    
    return examples


def generate_all():
    """Generate all synthetic examples"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("="*70)
    print("Synthetic KQL/EQL/Pipeline Generation")
    print("="*70)
    
    # Generate KQL
    print("\nGenerating KQL examples...")
    kql_examples = generate_kql_examples()
    print(f"  Generated {len(kql_examples)} KQL examples")
    
    # Generate EQL
    print("\nGenerating EQL examples...")
    eql_examples = generate_eql_examples()
    print(f"  Generated {len(eql_examples)} EQL examples")
    
    # Generate Pipelines
    print("\nGenerating pipeline examples...")
    pipeline_examples = generate_pipeline_examples()
    print(f"  Generated {len(pipeline_examples)} pipeline examples")
    
    # Save all examples
    all_examples = kql_examples + eql_examples + pipeline_examples
    
    output_file = OUTPUT_DIR / "synthetic_kql_eql_pipelines.jsonl"
    print(f"\nSaving {len(all_examples)} examples to {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in all_examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    # Save metadata
    metadata = {
        "source": "Synthetic Generation",
        "kql_examples": len(kql_examples),
        "eql_examples": len(eql_examples),
        "pipeline_examples": len(pipeline_examples),
        "total_examples": len(all_examples)
    }
    
    metadata_file = OUTPUT_DIR / "metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"[OK] Synthetic generation complete!")
    print(f"     KQL: {len(kql_examples)}")
    print(f"     EQL: {len(eql_examples)}")
    print(f"     Pipelines: {len(pipeline_examples)}")
    print(f"     Total: {len(all_examples)}")
    print(f"{'='*70}")


if __name__ == "__main__":
    generate_all()

