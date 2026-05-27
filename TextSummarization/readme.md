# README — Pipeline de Sumarização Longa com Azure OpenAI

## 🇧🇷 PT-BR

### Visão Geral

Este projeto implementa um pipeline completo para sumarização de documentos longos utilizando o Azure OpenAI.
O sistema:

* Divide textos grandes em chunks inteligentes
* Gera resumos parciais
* Consolida os resumos em um resumo final estruturado
* Mantém auditoria completa dos chunks e resumos
* Avalia a qualidade do resumo usando métricas NLP
* Exporta gráficos de avaliação em PDF

O objetivo é permitir sumarização auditável, escalável e mensurável para documentos extensos. 

---

# Funcionalidades

## ✅ Chunking Inteligente

O texto é dividido em blocos respeitando limites de tokens.

Características:

* Separação por parágrafos
* Controle de overlap entre chunks
* Compatível com modelos GPT
* Evita cortes bruscos de contexto

---

## ✅ Sumarização Hierárquica

Fluxo:

1. Divide o texto em chunks
2. Resume cada chunk individualmente
3. Consolida todos os resumos em um resumo final

Isso reduz perda de contexto em documentos muito grandes.

---

## ✅ Auditoria Completa

Cada chunk processado gera um registro contendo:

* Texto original do chunk
* Resumo gerado
* Quantidade de tokens
* Timestamp
* Número do chunk

Os dados são salvos em:

```bash
audit/summaries_audit.jsonl
```

Isso permite rastreabilidade e inspeção humana do pipeline.

---

## ✅ Avaliação Automática

Se existir um resumo de referência (`ref_summary.txt`), o sistema calcula:

* ROUGE-1
* ROUGE-2
* ROUGE-L
* METEOR

Os resultados são exportados em:

```bash
output/evaluation_scores.json
```

---

## ✅ Exportação de Gráfico PDF

O pipeline gera automaticamente um gráfico com os scores de avaliação.

Arquivo gerado:

```bash
output/evaluation_scores.pdf
```

---

# Estrutura do Projeto

```bash
.
├── long_doc.txt
├── ref_summary.txt
├── output/
│   ├── final_summary.md
│   ├── evaluation_scores.json
│   └── evaluation_scores.pdf
├── audit/
│   └── summaries_audit.jsonl
└── main.py
```

---

# Requisitos

## Python

Recomendado:

```bash
Python 3.11+
```

---

## Dependências

Instale com:

```bash
pip install openai python-dotenv tiktoken evaluate rouge-score absl-py nltk matplotlib
```

---

# Configuração

Crie um arquivo `.env`:

```env
AZURE_OPENAI_API_URL=https://SEU-ENDPOINT.openai.azure.com/
AZURE_OPENAI_API_KEY=SUA_CHAVE
AZURE_OPENAI_DEPLOYMENT=gpt-5.2
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

---

# Arquivos de Entrada

## Documento Principal

Arquivo:

```bash
long_doc.txt
```

Contém o texto que será resumido.

---

## Resumo de Referência (Opcional)

Arquivo:

```bash
ref_summary.txt
```

Usado para calcular métricas automáticas.

Se não existir, a etapa de avaliação será ignorada.

---

# Como Executar

```bash
python main.py
```

---

# Fluxo Interno

## 1. Carregamento

* Lê variáveis de ambiente
* Cria diretórios
* Carrega documento principal

---

## 2. Chunking

O texto é dividido considerando:

```python
CHUNK_MAX_TOKENS = 2000
CHUNK_OVERLAP_TOKENS = 200
```

O overlap preserva contexto entre chunks consecutivos.

---

## 3. Sumarização

Cada chunk é enviado ao Azure OpenAI.

Estrutura do resumo:

* Main points
* Important details
* Decisions or conclusions
* Risks or open questions

---

## 4. Consolidação

Os resumos parciais são combinados em um resumo final estruturado.

---

## 5. Auditoria

Cada etapa é registrada em JSONL.

Exemplo:

```json
{
  "chunk_number": 1,
  "chunk_tokens": 1980,
  "summary_tokens": 320
}
```

---

## 6. Avaliação

Caso exista referência:

* Calcula métricas NLP
* Salva JSON
* Gera gráfico PDF

---

# Métricas Utilizadas

## ROUGE

Mede similaridade lexical entre resumo gerado e referência.

Inclui:

* ROUGE-1
* ROUGE-2
* ROUGE-L

---

## METEOR

Métrica baseada em:

* precisão
* recall
* stemming
* alinhamento semântico

Geralmente mais robusta semanticamente que ROUGE.

---

# Principais Configurações

| Configuração               | Descrição                  |
| -------------------------- | -------------------------- |
| `CHUNK_MAX_TOKENS`         | Máximo de tokens por chunk |
| `CHUNK_OVERLAP_TOKENS`     | Sobreposição entre chunks  |
| `SUMMARY_MAX_TOKENS`       | Limite do resumo parcial   |
| `FINAL_SUMMARY_MAX_TOKENS` | Limite do resumo final     |

---

# Casos de Uso

* Sumarização de papers
* Documentos jurídicos
* Relatórios corporativos
* Logs extensos
* Auditoria documental
* Pipelines RAG
* Benchmark de modelos LLM

---

# Melhorias Futuras

Possíveis evoluções:

* Paralelização de chunks
* Cache de embeddings
* Resumo incremental
* Suporte multi-modelo
* Dashboard web
* Exportação DOCX/PPTX
* Vetorização semântica
* Rastreamento de hallucinations

---

# Licença

Uso educacional e experimental.

---

---

# 🇺🇸 EN-US

## Overview

This project implements a complete long-document summarization pipeline using Azure OpenAI.

The system:

* Splits large texts into intelligent chunks
* Generates partial summaries
* Consolidates summaries into a final structured summary
* Keeps full audit logs
* Evaluates summary quality using NLP metrics
* Exports evaluation charts as PDF

The goal is to provide scalable, auditable, and measurable summarization for large documents. 

---

# Features

## ✅ Intelligent Chunking

The text is split into chunks while respecting token limits.

Features:

* Paragraph-aware splitting
* Chunk overlap support
* GPT-compatible tokenization
* Context preservation

---

## ✅ Hierarchical Summarization

Pipeline flow:

1. Split text into chunks
2. Summarize each chunk
3. Consolidate all summaries

This approach reduces context loss for very large documents.

---

## ✅ Full Auditability

Each processed chunk generates an audit record containing:

* Original chunk text
* Generated summary
* Token counts
* Timestamp
* Chunk index

Saved at:

```bash
audit/summaries_audit.jsonl
```

This enables full traceability and human inspection.

---

## ✅ Automatic Evaluation

If a reference summary (`ref_summary.txt`) exists, the system computes:

* ROUGE-1
* ROUGE-2
* ROUGE-L
* METEOR

Results are exported to:

```bash
output/evaluation_scores.json
```

---

## ✅ PDF Chart Export

The pipeline automatically generates a PDF chart containing evaluation scores.

Generated file:

```bash
output/evaluation_scores.pdf
```

---

# Project Structure

```bash
.
├── long_doc.txt
├── ref_summary.txt
├── output/
│   ├── final_summary.md
│   ├── evaluation_scores.json
│   └── evaluation_scores.pdf
├── audit/
│   └── summaries_audit.jsonl
└── main.py
```

---

# Requirements

## Python

Recommended:

```bash
Python 3.11+
```

---

## Dependencies

Install with:

```bash
pip install openai python-dotenv tiktoken evaluate rouge-score absl-py nltk matplotlib
```

---

# Configuration

Create a `.env` file:

```env
AZURE_OPENAI_API_URL=https://YOUR-ENDPOINT.openai.azure.com/
AZURE_OPENAI_API_KEY=YOUR_KEY
AZURE_OPENAI_DEPLOYMENT=gpt-5.2
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

---

# Input Files

## Main Document

File:

```bash
long_doc.txt
```

Contains the document to summarize.

---

## Reference Summary (Optional)

File:

```bash
ref_summary.txt
```

Used for automatic evaluation metrics.

If absent, the evaluation step is skipped.

---

# Running

```bash
python main.py
```

---

# Internal Flow

## 1. Loading

* Loads environment variables
* Creates directories
* Loads main document

---

## 2. Chunking

The text is split according to:

```python
CHUNK_MAX_TOKENS = 2000
CHUNK_OVERLAP_TOKENS = 200
```

Overlap preserves context between consecutive chunks.

---

## 3. Summarization

Each chunk is sent to Azure OpenAI.

Summary structure:

* Main points
* Important details
* Decisions or conclusions
* Risks or open questions

---

## 4. Consolidation

Partial summaries are merged into a final structured summary.

---

## 5. Audit

Each step is stored as JSONL.

Example:

```json
{
  "chunk_number": 1,
  "chunk_tokens": 1980,
  "summary_tokens": 320
}
```

---

## 6. Evaluation

If a reference exists:

* Computes NLP metrics
* Saves JSON
* Generates PDF chart

---

# Metrics

## ROUGE

Measures lexical similarity between generated and reference summaries.

Includes:

* ROUGE-1
* ROUGE-2
* ROUGE-L

---

## METEOR

Metric based on:

* precision
* recall
* stemming
* semantic alignment

Usually more semantically robust than ROUGE.

---

# Main Configurations

| Configuration              | Description              |
| -------------------------- | ------------------------ |
| `CHUNK_MAX_TOKENS`         | Maximum tokens per chunk |
| `CHUNK_OVERLAP_TOKENS`     | Chunk overlap size       |
| `SUMMARY_MAX_TOKENS`       | Partial summary limit    |
| `FINAL_SUMMARY_MAX_TOKENS` | Final summary limit      |

---

# Use Cases

* Research paper summarization
* Legal documents
* Corporate reports
* Large logs
* Document auditing
* RAG pipelines
* LLM benchmarking

---

# Future Improvements

Possible future enhancements:

* Parallel chunk processing
* Embedding cache
* Incremental summarization
* Multi-model support
* Web dashboard
* DOCX/PPTX export
* Semantic vectorization
* Hallucination tracking

---

# License

Educational and experimental use only.
