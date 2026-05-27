# README — Download de Dataset PubMed para Benchmark de Sumarização

## 🇧🇷 PT-BR

### Visão Geral

Este projeto realiza o download automático de um exemplo do dataset PubMed Summarization utilizando a biblioteca Hugging Face Datasets.

O script:

* Baixa o dataset `ccdv/pubmed-summarization`
* Seleciona um exemplo do conjunto de treino
* Extrai:

  * artigo científico completo
  * resumo de referência
* Exporta os arquivos para uso em pipelines de sumarização e benchmark

O objetivo principal é gerar automaticamente:

* `long_doc.txt`
* `ref_summary.txt`

para alimentar sistemas de avaliação de LLMs e sumarização. 

---

# Funcionalidades

## ✅ Download Automático do Dataset

O script utiliza:

```python id="9th7oi"
load_dataset("ccdv/pubmed-summarization")
```

para baixar automaticamente o dataset da Hugging Face.

---

## ✅ Extração de Artigo Científico

Cada amostra contém:

* artigo completo (`article`)
* abstract/resumo (`abstract`)

---

## ✅ Geração de Arquivos para Benchmark

Os dados são exportados como:

| Arquivo           | Conteúdo                    |
| ----------------- | --------------------------- |
| `long_doc.txt`    | Documento completo          |
| `ref_summary.txt` | Resumo humano de referência |

---

## ✅ Integração com Pipelines de Sumarização

Os arquivos gerados podem ser utilizados diretamente em:

* pipelines de summarization
* cálculo de ROUGE
* cálculo de METEOR
* benchmark de LLMs
* RAG pipelines
* avaliação de qualidade

---

# Estrutura do Projeto

```bash id="n67fsh"
.
├── main.py
└── output/
    ├── long_doc.txt
    └── ref_summary.txt
```

---

# Requisitos

## Python

Recomendado:

```bash id="skz8kh"
Python 3.11+
```

---

# Dependências

Instale com:

```bash id="3h4rk6"
pip install datasets
```

---

# Como Funciona

## 1. Download do Dataset

O script baixa o dataset:

```python id="r2ozrq"
dataset = load_dataset("ccdv/pubmed-summarization")
```

O Hugging Face armazena os arquivos localmente em cache automaticamente.

---

## 2. Seleção de Exemplo

O primeiro item do dataset de treino é carregado:

```python id="fxzjlwm"
sample = dataset["train"][0]
```

---

## 3. Extração dos Campos

Os campos extraídos são:

```python id="bjlwmn"
article = sample["article"]
abstract = sample["abstract"]
```

---

## 4. Criação da Pasta de Saída

A pasta `output/` é criada automaticamente:

```python id="jlwmk2"
output_dir.mkdir(exist_ok=True)
```

---

## 5. Exportação dos Arquivos

Os arquivos são salvos em UTF-8:

```python id="jlwmt9"
article_file.write_text(article, encoding="utf-8")
summary_file.write_text(abstract, encoding="utf-8")
```

---

# Como Executar

```bash id="jlwmq4"
python main.py
```

---

# Saída Esperada

```bash id="jlwmw7"
Article saved at: output/long_doc.txt
Reference summary saved at: output/ref_summary.txt
```

---

# Estrutura do Dataset

Cada entrada do dataset contém:

| Campo      | Descrição                           |
| ---------- | ----------------------------------- |
| `article`  | Texto completo do artigo científico |
| `abstract` | Resumo humano do artigo             |

---

# Dataset Utilizado

## PubMed Summarization Dataset

Dataset:

```text id="jlwmc1"
ccdv/pubmed-summarization
```

Baseado em artigos científicos biomédicos do PubMed.

Muito utilizado em:

* NLP research
* benchmark de summarization
* avaliação de LLMs
* pesquisa acadêmica

---

# Casos de Uso

## ✅ Benchmark de Modelos

Comparar:

* GPT
* Claude
* Gemini
* Llama
* Mistral

---

## ✅ Avaliação de Métricas

Gerar:

* ROUGE
* METEOR
* BLEU
* BERTScore

---

## ✅ Pipelines de Sumarização

Utilizar os arquivos como entrada para:

* chunking
* hierarchical summarization
* RAG
* retrieval pipelines

---

## ✅ Estudos Acadêmicos

Ideal para:

* NLP
* Information Retrieval
* Summarization Research
* LLM Evaluation

---

# Possíveis Melhorias

## 🔹 Seleção Aleatória

Escolher exemplos aleatórios:

```python id="jlwmj5"
import random
sample = random.choice(dataset["train"])
```

---

## 🔹 Exportar Múltiplos Exemplos

Salvar vários artigos automaticamente.

---

## 🔹 Batch Dataset Generation

Gerar datasets completos para benchmark.

---

## 🔹 Metadata Export

Salvar também:

* título
* autores
* categorias
* tamanho do artigo

---

## 🔹 Integração com Pandas

Exportar datasets tabulares.

---

# Segurança e Performance

## Cache Automático

O Hugging Face Datasets utiliza cache local automaticamente.

Isso evita downloads repetidos.

---

## Espaço em Disco

Datasets científicos podem ocupar bastante armazenamento dependendo da quantidade baixada.

---

# Fluxo Interno

```text id="jlwmm8"
Hugging Face Dataset
        ↓
Load Dataset
        ↓
Select Sample
        ↓
Extract Article + Abstract
        ↓
Export TXT Files
```

---

# Exemplo de .gitignore

```gitignore id="jlwmr3"
output/
__pycache__/
*.pyc
```

---

# Licença

Uso educacional e experimental.

---

---

# 🇺🇸 EN-US

## Overview

This project automatically downloads a sample from the PubMed Summarization dataset using Hugging Face Datasets.

The script:

* Downloads the `ccdv/pubmed-summarization` dataset
* Selects one training sample
* Extracts:

  * full scientific article
  * reference abstract
* Exports files for summarization and benchmarking pipelines

The main goal is to automatically generate:

* `long_doc.txt`
* `ref_summary.txt`

to feed LLM evaluation and summarization systems. 

---

# Features

## ✅ Automatic Dataset Download

The script uses:

```python id="enjlwm1"
load_dataset("ccdv/pubmed-summarization")
```

to automatically download the dataset from Hugging Face.

---

## ✅ Scientific Article Extraction

Each sample contains:

* full article (`article`)
* human-written abstract (`abstract`)

---

## ✅ Benchmark File Generation

The exported files are:

| File              | Content                 |
| ----------------- | ----------------------- |
| `long_doc.txt`    | Full document           |
| `ref_summary.txt` | Human reference summary |

---

## ✅ Summarization Pipeline Integration

Generated files can directly feed:

* summarization pipelines
* ROUGE evaluation
* METEOR evaluation
* LLM benchmarks
* RAG pipelines
* quality evaluation systems

---

# Project Structure

```bash id="enjlwm4"
.
├── main.py
└── output/
    ├── long_doc.txt
    └── ref_summary.txt
```

---

# Requirements

## Python

Recommended:

```bash id="enjlwm7"
Python 3.11+
```

---

# Dependencies

Install with:

```bash id="enjlwm0"
pip install datasets
```

---

# How It Works

## 1. Dataset Download

The script downloads:

```python id="enjlwm3"
dataset = load_dataset("ccdv/pubmed-summarization")
```

Hugging Face automatically caches the dataset locally.

---

## 2. Sample Selection

The first training sample is loaded:

```python id="enjlwm6"
sample = dataset["train"][0]
```

---

## 3. Field Extraction

Extracted fields:

```python id="enjlwm9"
article = sample["article"]
abstract = sample["abstract"]
```

---

## 4. Output Directory Creation

The `output/` directory is automatically created:

```python id="enjlwm2"
output_dir.mkdir(exist_ok=True)
```

---

## 5. File Export

Files are saved using UTF-8 encoding:

```python id="enjlwm5"
article_file.write_text(article, encoding="utf-8")
summary_file.write_text(abstract, encoding="utf-8")
```

---

# Running

```bash id="enjlwm8"
python main.py
```

---

# Expected Output

```bash id="enjlwmz"
Article saved at: output/long_doc.txt
Reference summary saved at: output/ref_summary.txt
```

---

# Dataset Structure

Each dataset entry contains:

| Field      | Description                  |
| ---------- | ---------------------------- |
| `article`  | Full scientific article text |
| `abstract` | Human-written summary        |

---

# Dataset Used

## PubMed Summarization Dataset

Dataset:

```text id="enjlwmx"
ccdv/pubmed-summarization
```

Based on biomedical scientific articles from PubMed.

Widely used in:

* NLP research
* summarization benchmarks
* LLM evaluation
* academic research

---

# Use Cases

## ✅ Model Benchmarking

Compare:

* GPT
* Claude
* Gemini
* Llama
* Mistral

---

## ✅ Metric Evaluation

Generate:

* ROUGE
* METEOR
* BLEU
* BERTScore

---

## ✅ Summarization Pipelines

Use generated files for:

* chunking
* hierarchical summarization
* RAG
* retrieval pipelines

---

## ✅ Academic Studies

Ideal for:

* NLP
* Information Retrieval
* Summarization Research
* LLM Evaluation

---

# Possible Improvements

## 🔹 Random Sample Selection

Choose random samples:

```python id="enjlwmv"
import random
sample = random.choice(dataset["train"])
```

---

## 🔹 Multiple Sample Export

Automatically save multiple articles.

---

## 🔹 Batch Dataset Generation

Generate complete benchmark datasets.

---

## 🔹 Metadata Export

Also export:

* title
* authors
* categories
* article size

---

## 🔹 Pandas Integration

Export structured tabular datasets.

---

# Security and Performance

## Automatic Cache

Hugging Face Datasets automatically uses local cache.

This avoids repeated downloads.

---

## Disk Space

Scientific datasets may consume significant disk space depending on dataset size.

---

# Internal Flow

```text id="enjlwmu"
Hugging Face Dataset
        ↓
Load Dataset
        ↓
Select Sample
        ↓
Extract Article + Abstract
        ↓
Export TXT Files
```

---

# Example .gitignore

```gitignore id="enjlwmt"
output/
__pycache__/
*.pyc
```

---

# License

Educational and experimental use only.
