# README — Análise de Sentimento com LangChain + Azure OpenAI

## 🇧🇷 PT-BR

### Visão Geral

Este projeto implementa uma pipeline simples de análise de sentimento utilizando:

* LangChain
* Azure OpenAI
* Prompt Engineering
* GPT via Azure Foundry/OpenAI

O sistema classifica textos em:

* Positive
* Neutral
* Negative

A solução utiliza o modelo GPT através do `AzureChatOpenAI` integrado ao LangChain. 

---

# Funcionalidades

## ✅ Integração com Azure OpenAI

Conecta diretamente ao Azure OpenAI utilizando:

* Endpoint customizado
* API Key
* Deployment específico
* API Version

---

## ✅ Pipeline com LangChain

O fluxo usa o operador LCEL (`|`) do LangChain:

```python id="xql6pj"
chain = prompt | llm
```

Isso cria uma pipeline declarativa simples e reutilizável.

---

## ✅ Prompt Engineering

O prompt instrui explicitamente o modelo a retornar apenas:

* positive
* neutral
* negative

Estrutura:

```python id="u0ttn0"
Classify the sentiment of the following text
as positive, neutral, or negative
```

---

## ✅ Fácil Extensão

O projeto pode ser facilmente expandido para:

* classificação multi-classe
* emotion detection
* toxicity analysis
* intent detection
* multilingual sentiment analysis

---

# Estrutura do Projeto

```bash id="7is0k7"
.
├── .env
├── main.py
└── requirements.txt
```

---

# Requisitos

## Python

Recomendado:

```bash id="gw1ja0"
Python 3.11+
```

---

# Dependências

Instale com:

```bash id="x9v3ej"
pip install langchain langchain-openai python-dotenv openai
```

---

# Configuração

Crie um arquivo `.env`:

```env id="3a9r2n"
AZURE_OPENAI_API_URL=https://SEU-ENDPOINT.openai.azure.com/
AZURE_OPENAI_API_KEY=SUA_CHAVE
```

---

# Como Funciona

## 1. Carregamento das Variáveis

O sistema carrega:

* endpoint Azure
* API key

Usando:

```python id="9xdkv8"
load_dotenv()
```

---

## 2. Inicialização do Modelo

O modelo é configurado via:

```python id="eg4p8j"
AzureChatOpenAI(...)
```

Configurações utilizadas:

| Configuração | Valor                |
| ------------ | -------------------- |
| API Version  | `2024-12-01-preview` |
| Deployment   | `gpt-5.2`            |
| Temperature  | `0`                  |

---

## 3. Construção do Prompt

O LangChain utiliza `PromptTemplate` para parametrizar o texto de entrada.

Variável dinâmica:

```python id="t4a1qb"
{text}
```

---

## 4. Execução da Chain

A execução acontece via:

```python id="78f42h"
chain.invoke({"text": text})
```

---

# Função Principal

## analyze_sentiment

Responsável por:

* receber o texto
* enviar ao modelo
* retornar o sentimento classificado

Implementação:

```python id="u7av39"
def analyze_sentiment(text: str) -> str:
    result = chain.invoke({"text": text})
    return result.content.strip()
```

---

# Exemplos de Uso

## Entrada

```text id="qlu7ji"
I absolutely love this product!
```

## Saída

```text id="16rcl5"
positive
```

---

## Entrada

```text id="vbphki"
It's okay, could be better.
```

## Saída

```text id="dqqd8v"
neutral
```

---

## Entrada

```text id="44i9dn"
Worst experience ever.
```

## Saída

```text id="5ldp8n"
negative
```

---

# Como Executar

```bash id="mybs6r"
python main.py
```

---

# Fluxo Interno

```text id="zpdjpi"
Texto
   ↓
PromptTemplate
   ↓
AzureChatOpenAI
   ↓
LangChain Chain
   ↓
Classificação
```

---

# Casos de Uso

* análise de reviews
* classificação de feedbacks
* monitoramento de redes sociais
* SAC/Customer Support
* análise de tickets
* análise de comentários
* NLP educacional

---

# Possíveis Melhorias

## 🔹 Structured Output

Retornar JSON estruturado:

```json id="n8aq8r"
{
  "sentiment": "positive",
  "confidence": 0.95
}
```

---

## 🔹 Few-Shot Prompting

Adicionar exemplos no prompt para melhorar consistência.

---

## 🔹 Batch Processing

Processar múltiplos textos simultaneamente.

---

## 🔹 Streaming

Adicionar respostas em tempo real.

---

## 🔹 Observabilidade

Integrar:

* LangSmith
* OpenTelemetry
* Logging
* Token tracking

---

## 🔹 Fine-Grained Sentiment

Expandir para:

* very positive
* slightly positive
* mixed
* sarcastic

---

# Segurança

Nunca exponha:

* API keys
* endpoints privados
* variáveis `.env`

Adicione `.env` ao `.gitignore`.

---

# Exemplo de .gitignore

```gitignore id="xy66ml"
.env
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

This project implements a simple sentiment analysis pipeline using:

* LangChain
* Azure OpenAI
* Prompt Engineering
* GPT through Azure Foundry/OpenAI

The system classifies text as:

* Positive
* Neutral
* Negative

The solution uses `AzureChatOpenAI` integrated with LangChain. 

---

# Features

## ✅ Azure OpenAI Integration

Direct integration with Azure OpenAI using:

* Custom endpoint
* API key
* Deployment name
* API version

---

## ✅ LangChain Pipeline

The flow uses LangChain LCEL (`|`) operator:

```python id="jlwmh5"
chain = prompt | llm
```

This creates a simple and reusable declarative pipeline.

---

## ✅ Prompt Engineering

The prompt explicitly instructs the model to return:

* positive
* neutral
* negative

Structure:

```python id="bm9dr4"
Classify the sentiment of the following text
as positive, neutral, or negative
```

---

## ✅ Easy Extensibility

The project can easily be expanded to support:

* multi-class classification
* emotion detection
* toxicity analysis
* intent detection
* multilingual sentiment analysis

---

# Project Structure

```bash id="vjlwm2"
.
├── .env
├── main.py
└── requirements.txt
```

---

# Requirements

## Python

Recommended:

```bash id="ahjlwm"
Python 3.11+
```

---

# Dependencies

Install with:

```bash id="bjlwm5"
pip install langchain langchain-openai python-dotenv openai
```

---

# Configuration

Create a `.env` file:

```env id="cjlwm8"
AZURE_OPENAI_API_URL=https://YOUR-ENDPOINT.openai.azure.com/
AZURE_OPENAI_API_KEY=YOUR_KEY
```

---

# How It Works

## 1. Environment Loading

The system loads:

* Azure endpoint
* API key

Using:

```python id="djlwm1"
load_dotenv()
```

---

## 2. Model Initialization

The model is configured through:

```python id="ejlwm4"
AzureChatOpenAI(...)
```

Used settings:

| Configuration | Value                |
| ------------- | -------------------- |
| API Version   | `2024-12-01-preview` |
| Deployment    | `gpt-5.2`            |
| Temperature   | `0`                  |

---

## 3. Prompt Construction

LangChain uses `PromptTemplate` for parameterized input.

Dynamic variable:

```python id="fjlwm7"
{text}
```

---

## 4. Chain Execution

Execution happens through:

```python id="gjlwm0"
chain.invoke({"text": text})
```

---

# Main Function

## analyze_sentiment

Responsible for:

* receiving text
* sending it to the model
* returning classified sentiment

Implementation:

```python id="hjlwm3"
def analyze_sentiment(text: str) -> str:
    result = chain.invoke({"text": text})
    return result.content.strip()
```

---

# Usage Examples

## Input

```text id="ijlwm6"
I absolutely love this product!
```

## Output

```text id="jjlwm9"
positive
```

---

## Input

```text id="kjlwm2"
It's okay, could be better.
```

## Output

```text id="ljlwm5"
neutral
```

---

## Input

```text id="mjlwm8"
Worst experience ever.
```

## Output

```text id="njlwm1"
negative
```

---

# Running

```bash id="ojlwm4"
python main.py
```

---

# Internal Flow

```text id="pjlwm7"
Text
   ↓
PromptTemplate
   ↓
AzureChatOpenAI
   ↓
LangChain Chain
   ↓
Classification
```

---

# Use Cases

* review analysis
* customer feedback classification
* social media monitoring
* customer support
* ticket analysis
* comment moderation
* educational NLP

---

# Possible Improvements

## 🔹 Structured Output

Return structured JSON:

```json id="qjlwm0"
{
  "sentiment": "positive",
  "confidence": 0.95
}
```

---

## 🔹 Few-Shot Prompting

Add prompt examples for better consistency.

---

## 🔹 Batch Processing

Process multiple texts simultaneously.

---

## 🔹 Streaming

Add real-time response streaming.

---

## 🔹 Observability

Integrate:

* LangSmith
* OpenTelemetry
* Logging
* Token tracking

---

## 🔹 Fine-Grained Sentiment

Expand to:

* very positive
* slightly positive
* mixed
* sarcastic

---

# Security

Never expose:

* API keys
* private endpoints
* `.env` variables

Add `.env` to `.gitignore`.

---

# Example .gitignore

```gitignore id="rjlwm3"
.env
__pycache__/
*.pyc
```

---

# License

Educational and experimental use only.
