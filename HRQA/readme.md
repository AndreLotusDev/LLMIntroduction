# HRQA — HR Policy Question & Answer System

---

## Português

### Visão Geral

O **HRQA** é um sistema de perguntas e respostas sobre políticas de RH construído com RAG (Retrieval-Augmented Generation). Ele permite que colaboradores consultem documentos de política de RH em linguagem natural, recebendo respostas precisas fundamentadas no conteúdo oficial da empresa — sem alucinações, sem respostas inventadas.

### Como Funciona

O pipeline é dividido em duas etapas:

**1. Ingestão (`ingestion.py`)**
- Carrega o documento de política de RH (`hr_policy_long.txt`)
- Divide o texto em chunks de 500 caracteres com sobreposição de 50
- Gera embeddings usando o modelo local `BAAI/bge-small-en-v1.5` (HuggingFace)
- Persiste os vetores em um banco de dados ChromaDB local (`hr_chroma_db/`)

**2. Consulta (`ask.py`)**
- Carrega o banco vetorial existente
- Recebe uma pergunta do usuário via terminal
- Recupera os 4 chunks mais relevantes (busca por similaridade)
- Envia contexto + pergunta para o Azure OpenAI (GPT) via LangChain
- Retorna a resposta fundamentada no documento

Se a resposta não estiver no documento, o sistema responde apenas: `"I don't know."` — evitando informações incorretas.

### Tecnologias

| Componente | Tecnologia |
|---|---|
| Orquestração | LangChain |
| LLM | Azure OpenAI (GPT) |
| Embeddings | HuggingFace `BAAI/bge-small-en-v1.5` |
| Banco vetorial | ChromaDB |
| Variáveis de ambiente | python-dotenv |

### Configuração

1. Instale as dependências:
   ```bash
   pip install langchain langchain-openai langchain-community langchain-text-splitters chromadb sentence-transformers python-dotenv
   ```

2. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
   ```env
   AZURE_OPENAI_API_URL=https://<seu-recurso>.openai.azure.com/
   AZURE_OPENAI_API_KEY=<sua-chave>
   AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o   # nome do seu deployment
   ```

3. Execute a ingestão (apenas na primeira vez ou quando o documento mudar):
   ```bash
   python ingestion.py
   ```

4. Faça perguntas:
   ```bash
   python ask.py
   ```

### Exemplo de Uso

```
Ask a question: How many vacation days do employees get after 5 years?

Q: How many vacation days do employees get after 5 years?
A: Employees with 5 or more years of service receive 15 vacation days per year.
```

---

## English

### Overview

**HRQA** is a HR policy question-and-answer system built with RAG (Retrieval-Augmented Generation). It allows employees to query HR policy documents in natural language, receiving accurate answers grounded in the company's official content — no hallucinations, no invented responses.

### How It Works

The pipeline is split into two stages:

**1. Ingestion (`ingestion.py`)**
- Loads the HR policy document (`hr_policy_long.txt`)
- Splits the text into 500-character chunks with 50-character overlap
- Generates embeddings using the local model `BAAI/bge-small-en-v1.5` (HuggingFace)
- Persists the vectors in a local ChromaDB database (`hr_chroma_db/`)

**2. Query (`ask.py`)**
- Loads the existing vector store
- Accepts a user question from the terminal
- Retrieves the 4 most relevant chunks (similarity search)
- Sends context + question to Azure OpenAI (GPT) via LangChain
- Returns the answer grounded in the document

If the answer is not in the document, the system responds only with: `"I don't know."` — preventing incorrect information from being surfaced.

### Tech Stack

| Component | Technology |
|---|---|
| Orchestration | LangChain |
| LLM | Azure OpenAI (GPT) |
| Embeddings | HuggingFace `BAAI/bge-small-en-v1.5` |
| Vector store | ChromaDB |
| Environment variables | python-dotenv |

### Setup

1. Install dependencies:
   ```bash
   pip install langchain langchain-openai langchain-community langchain-text-splitters chromadb sentence-transformers python-dotenv
   ```

2. Create a `.env` file in the project root with the following variables:
   ```env
   AZURE_OPENAI_API_URL=https://<your-resource>.openai.azure.com/
   AZURE_OPENAI_API_KEY=<your-key>
   AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o   # your deployment name
   ```

3. Run ingestion (only needed the first time or when the document changes):
   ```bash
   python ingestion.py
   ```

4. Ask questions:
   ```bash
   python ask.py
   ```

### Usage Example

```
Ask a question: How many vacation days do employees get after 5 years?

Q: How many vacation days do employees get after 5 years?
A: Employees with 5 or more years of service receive 15 vacation days per year.
```
