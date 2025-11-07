# Dataset Expansion Guide - Expert Elastic

Este documento lista datasets e estratégias para expandir o dataset atual (904 exemplos) para um tamanho mais adequado (10k-30k exemplos).

## Situação Atual

**Dataset atual:** 904 exemplos
- ECS: 20 exemplos
- Kibana Samples: 40 exemplos  
- Detection Rules: 224 exemplos (90 KQL + 134 EQL)
- Elastic Labs: 1,000 exemplos (sintéticos)
- Integrations: 0 exemplos (script não gerou)

**Meta:** 10k-30k exemplos (similar a Neo4j: 29k, SQL: 99k)

## Datasets Públicos Recomendados

### 1. Elasticsearch Official Examples

**Fonte:** GitHub Elastic
- **Repositório:** https://github.com/elastic/elasticsearch
- **Localização:** `docs/examples/`, `x-pack/plugin/src/test/resources/`
- **Conteúdo:** 
  - Exemplos de queries DSL oficiais
  - Mappings de índices
  - Aggregations complexas
  - Ingest pipelines
- **Estimativa:** 500-1,000 exemplos
- **Licença:** Apache 2.0
- **Script necessário:** `scripts/collect_elasticsearch_examples.py`

### 2. Elastic Stack Examples

**Fonte:** GitHub Elastic Stack Samples
- **Repositório:** https://github.com/elastic/examples
- **Conteúdo:**
  - Casos de uso reais
  - Queries de produção
  - Mappings de domínios específicos
- **Estimativa:** 200-500 exemplos
- **Licença:** Apache 2.0

### 3. Kibana Sample Data (Expandido)

**Fonte:** Kibana Built-in Samples
- **Atual:** 40 exemplos
- **Expansão:** Gerar mais variações de queries baseadas nos schemas conhecidos
- **Estratégia:** 
  - eCommerce: 50-100 queries adicionais
  - Flights: 50-100 queries adicionais
  - Web Logs: 50-100 queries adicionais
- **Estimativa:** +150-300 exemplos

### 4. Elastic Integrations (Corrigir Script)

**Fonte:** Elastic Package Registry
- **Atual:** 0 exemplos (script não funcionou)
- **Problema:** Script `collect_integrations.py` precisa ser corrigido
- **Potencial:** 10-15k exemplos (mappings + pipelines)
- **Prioridade:** ALTA - maior fonte potencial

**Integrações prioritárias:**
- nginx, apache (web servers)
- aws, gcp, azure (cloud)
- mysql, postgresql (databases)
- kubernetes, docker (containers)
- windows, linux (OS)

### 5. Stack Overflow Elasticsearch Questions

**Fonte:** Stack Overflow Data Dump
- **Conteúdo:** Perguntas e respostas com queries DSL
- **Estimativa:** 1,000-3,000 exemplos úteis
- **Licença:** CC BY-SA 4.0
- **Desafio:** Requer parsing e validação manual
- **Script necessário:** `scripts/collect_stackoverflow.py`

### 6. Elasticsearch Documentation Examples

**Fonte:** Elasticsearch Official Documentation
- **URL:** https://www.elastic.co/guide/en/elasticsearch/reference/current/
- **Conteúdo:** 
  - Exemplos de queries em cada página
  - Mappings de exemplo
  - Aggregations documentadas
- **Estimativa:** 500-1,000 exemplos
- **Script necessário:** `scripts/collect_documentation.py`

### 7. Elasticsearch Cookbook Examples

**Fonte:** Livros e tutoriais
- **Elasticsearch Cookbook** (Packt Publishing)
- **Elasticsearch: The Definitive Guide** (O'Reilly)
- **Estimativa:** 200-500 exemplos
- **Licença:** Verificar permissões

### 8. Synthetic Generation (Expandir Elastic Labs)

**Fonte:** Template-based generation
- **Atual:** 1,000 exemplos sintéticos
- **Expansão:** 
  - Mais padrões de queries DSL
  - Mais variações de aggregations
  - Mais exemplos de mappings ECS
  - Exemplos de pipelines (atualmente 0)
- **Estimativa:** +5,000-10,000 exemplos
- **Prioridade:** MÉDIA - fácil de gerar

### 9. Security Detection Rules (Expandir)

**Fonte:** Elastic Detection Rules
- **Atual:** 224 exemplos (90 KQL + 134 EQL)
- **Expansão:** 
  - Processar mais categorias
  - Incluir regras deprecadas (99 regras encontradas)
  - Gerar variações de queries similares
- **Estimativa:** +200-500 exemplos

### 10. ECS Field Definitions (Expandir)

**Fonte:** Elastic Common Schema
- **Atual:** 20 exemplos (apenas schemas principais)
- **Expansão:**
  - Processar TODOS os campos ECS (não apenas schemas principais)
  - Gerar mappings para combinações de campos
  - Criar exemplos de queries usando campos ECS
- **Estimativa:** +500-1,000 exemplos
- **Script necessário:** Melhorar `collect_ecs.py`

## Estratégias de Expansão por Prioridade

### Prioridade ALTA (Maior Impacto)

1. **Corrigir script de Integrations** ⭐⭐⭐
   - Potencial: 10-15k exemplos
   - Esforço: Médio
   - Impacto: Muito alto

2. **Expandir Elastic Labs (sintéticos)** ⭐⭐⭐
   - Potencial: +5k-10k exemplos
   - Esforço: Baixo
   - Impacto: Alto

3. **Coletar exemplos do Elasticsearch oficial** ⭐⭐
   - Potencial: 500-1k exemplos
   - Esforço: Médio
   - Impacto: Médio-Alto

### Prioridade MÉDIA

4. **Expandir ECS** ⭐⭐
   - Potencial: +500-1k exemplos
   - Esforço: Baixo-Médio
   - Impacto: Médio

5. **Expandir Kibana Samples** ⭐
   - Potencial: +150-300 exemplos
   - Esforço: Baixo
   - Impacto: Baixo-Médio

6. **Coletar documentação oficial** ⭐
   - Potencial: 500-1k exemplos
   - Esforço: Médio
   - Impacto: Médio

### Prioridade BAIXA

7. **Stack Overflow parsing** ⭐
   - Potencial: 1k-3k exemplos
   - Esforço: Alto (requer validação manual)
   - Impacto: Médio

8. **Expandir Detection Rules** ⭐
   - Potencial: +200-500 exemplos
   - Esforço: Baixo
   - Impacto: Baixo

## Plano de Ação Recomendado

### Fase 1: Quick Wins (1-2 dias)
1. Corrigir script `collect_integrations.py` → +10-15k exemplos
2. Expandir Elastic Labs → +5k exemplos
3. **Total esperado:** ~16k-20k exemplos

### Fase 2: Expansão ECS e Kibana (1 dia)
1. Melhorar `collect_ecs.py` → +500-1k exemplos
2. Expandir Kibana samples → +200 exemplos
3. **Total esperado:** +700-1.2k exemplos

### Fase 3: Fontes Externas (2-3 dias)
1. Coletar exemplos do Elasticsearch oficial → +500-1k exemplos
2. Coletar documentação → +500-1k exemplos
3. **Total esperado:** +1k-2k exemplos

### Resultado Final Esperado
- **Atual:** 904 exemplos
- **Fase 1:** +16k-20k = ~17k-21k exemplos
- **Fase 2:** +700-1.2k = ~18k-22k exemplos
- **Fase 3:** +1k-2k = ~19k-24k exemplos

**Meta alcançada:** 19k-24k exemplos (similar a Neo4j: 29k)

## Scripts a Criar/Corrigir

### Scripts Novos
1. `scripts/collect_elasticsearch_examples.py` - GitHub oficial
2. `scripts/collect_documentation.py` - Documentação oficial
3. `scripts/expand_kibana_samples.py` - Gerar mais queries

### Scripts a Corrigir
1. `scripts/collect_integrations.py` - Atualmente retorna 0 exemplos
2. `scripts/collect_ecs.py` - Expandir para todos os campos ECS
3. `scripts/collect_elastic_labs.py` - Adicionar mais templates

## Referências

- **Elasticsearch GitHub:** https://github.com/elastic/elasticsearch
- **Elastic Examples:** https://github.com/elastic/examples
- **Elastic Package Registry:** https://epr.elastic.co
- **Elastic Detection Rules:** https://github.com/elastic/detection-rules
- **ECS Repository:** https://github.com/elastic/ecs
- **Elasticsearch Documentation:** https://www.elastic.co/guide/en/elasticsearch/reference/current/

## Notas

- Todos os datasets devem ser validados (JSON syntax, DSL syntax)
- Manter formato ChatML para consistência
- Deduplicar por task+instruction
- Criar splits train/validation/test (80/10/10)

