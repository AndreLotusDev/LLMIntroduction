# CompanySearch — Pesquisa de Empresas com Multi-Agentes

Sistema multi-agente construído com [CrewAI](https://crewai.com) que pesquisa uma empresa na internet e retorna um resumo curto sobre o que ela faz e suas últimas notícias.

---

## Visão Geral

O usuário informa o nome de uma empresa. O sistema dispara dois agentes em sequência:

1. **Company Researcher** — busca na internet informações sobre a empresa e suas notícias recentes
2. **Company Summarizer** — lê o resultado da pesquisa e gera um resumo conciso

O resultado final é salvo em `summary.md` e exibido no terminal.

---

## Fluxo de Execução

```
┌─────────────────────────────────────────────────┐
│                    Usuário                       │
│         digita o nome da empresa                 │
└───────────────────────┬─────────────────────────┘
                        │  company_name
                        ▼
┌─────────────────────────────────────────────────┐
│           Agente 1: Company Researcher           │
│                                                  │
│  Ferramentas: SerperDevTool (busca Google)       │
│                                                  │
│  Busca:                                          │
│  • O que a empresa faz (modelo de negócio,       │
│    produtos, setor)                              │
│  • Fatos principais (fundação, sede, tamanho)    │
│  • Últimas notícias (3-5 itens recentes)         │
│                                                  │
│  Saída: Company Overview + Latest News           │
└───────────────────────┬─────────────────────────┘
                        │  pesquisa estruturada
                        ▼
┌─────────────────────────────────────────────────┐
│           Agente 2: Company Summarizer           │
│                                                  │
│  Ferramentas: nenhuma (apenas raciocínio LLM)    │
│                                                  │
│  Sintetiza o resultado em:                       │
│  • 2-3 frases sobre o que a empresa faz          │
│  • Bullet points das notícias mais recentes      │
│                                                  │
│  Saída: summary.md                               │
└───────────────────────┬─────────────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │   summary.md    │
              │  (output final) │
              └─────────────────┘
```

---

## Agentes

### Company Researcher

| Campo      | Valor |
|------------|-------|
| **Role**   | Company Research Specialist |
| **Goal**   | Pesquisar informações abrangentes e atualizadas sobre a empresa, incluindo o que ela faz e as últimas notícias |
| **Tools**  | `SerperDevTool` |

Responsável por toda a coleta de dados. Faz múltiplas buscas na internet para cobrir tanto o perfil da empresa quanto suas novidades recentes.

### Company Summarizer

| Campo      | Valor |
|------------|-------|
| **Role**   | Business Intelligence Analyst |
| **Goal**   | Sintetizar os dados da pesquisa em um resumo curto e claro |
| **Tools**  | Nenhuma |

Recebe o resultado do Researcher como contexto e produz o resumo final. Não precisa de ferramentas externas — apenas raciocina sobre o conteúdo já coletado.

---

## Tarefas

### `research_task`

- **Agente:** `company_researcher`
- **Descrição:** Busca na internet o perfil da empresa (modelo de negócio, produtos, setor, fatos-chave) e suas notícias mais recentes (mínimo 3-5 itens com datas e fontes).
- **Saída esperada:** Relatório com duas seções — *Company Overview* e *Latest News*.

### `summary_task`

- **Agente:** `company_summarizer`
- **Contexto:** recebe a saída de `research_task`
- **Descrição:** Condensa a pesquisa em um resumo de leitura rápida (menos de 1 minuto).
- **Saída esperada:**

```markdown
**About <empresa>**
2-3 frases descrevendo o que a empresa faz.

**Latest News**
- [Data] Notícia 1
- [Data] Notícia 2
- [Data] Notícia 3
```

- **Arquivo de saída:** `summary.md`

---

## SerperDevTool

### O que é

`SerperDevTool` é uma ferramenta do pacote `crewai-tools` que permite aos agentes realizar buscas no Google de forma programática, usando a API do [Serper](https://serper.dev).

Ao chamar a ferramenta, o agente envia uma query de busca e recebe de volta os resultados orgânicos do Google — títulos, snippets, links e, em alguns casos, resultados de notícias (`news` endpoint).

### Como funciona internamente

```
Agente formula query
       ↓
SerperDevTool envia POST para https://google.serper.dev/search
com { q: "<query>", gl: "us", hl: "en" }
       ↓
Serper consulta o Google e retorna JSON estruturado
       ↓
A ferramenta converte o JSON em texto e entrega ao agente
       ↓
Agente interpreta e decide a próxima ação (ReAct loop)
```

### Por que usar

| Alternativa         | Limitação                                   |
|---------------------|---------------------------------------------|
| `DuckDuckGoSearchRun` | Resultados menos precisos, sem notícias    |
| `GoogleSearchAPIWrapper` | API mais cara e complexa de configurar  |
| `BrowserbaseTool`   | Mais pesada, voltada para scraping completo |
| **SerperDevTool**   | Leve, resultados do Google, plano grátis   |

O plano gratuito do Serper oferece **2.500 buscas/mês** — suficiente para uso em desenvolvimento e projetos pessoais.

### Como obter a chave

1. Acesse [serper.dev](https://serper.dev) e crie uma conta gratuita
2. No dashboard, copie sua **API Key**
3. Adicione no `.env`:

```env
SERPER_API_KEY=sua_chave_aqui
```

A `SerperDevTool` lê essa variável automaticamente via `os.environ`.

### Uso no código

```python
# crew.py
from crewai_tools import SerperDevTool

@agent
def company_researcher(self) -> Agent:
    return Agent(
        config=self.agents_config['company_researcher'],
        tools=[SerperDevTool()],  # ferramenta injetada aqui
        verbose=True
    )
```

O `company_summarizer` **não recebe a ferramenta** porque sua função é apenas sintetizar — não buscar dados novos.

---

## Configuração

### Pré-requisitos

- Python 3.10–3.13
- [uv](https://docs.astral.sh/uv/) (gerenciador de pacotes)

### Instalação

```bash
pip install uv
crewai install
```

### Variáveis de ambiente (`.env`)

```env
# Modelo LLM (Azure OpenAI)
MODEL=azure/gpt-4o
AZURE_API_KEY=sua_chave_azure
AZURE_API_BASE=https://seu-recurso.cognitiveservices.azure.com/
AZURE_API_VERSION=2024-12-01-preview

# Busca na internet
SERPER_API_KEY=sua_chave_serper
```

---

## Como Executar

```bash
crewai run
```

O sistema pedirá o nome da empresa:

```
Enter the company name to research: Nubank
```

Após a execução, o resumo é exibido no terminal e salvo em `summary.md`.

---

## Estrutura do Projeto

```
CompanySearch/
├── src/company_search/
│   ├── crew.py              # Orquestração: agentes, tarefas e crew
│   ├── main.py              # Ponto de entrada, lê input do usuário
│   ├── config/
│   │   ├── agents.yaml      # Definição dos agentes (role, goal, backstory)
│   │   └── tasks.yaml       # Definição das tarefas (description, expected_output)
│   └── tools/
│       └── custom_tool.py   # Template para ferramentas customizadas
├── .env                     # Chaves de API (não versionar)
├── summary.md               # Saída gerada a cada execução
└── pyproject.toml           # Dependências do projeto
```

---

## Dependências Principais

| Pacote         | Versão    | Função                            |
|----------------|-----------|-----------------------------------|
| `crewai`       | 1.14.5a2+ | Framework multi-agente            |
| `crewai-tools` | incluído  | Ferramentas prontas (SerperDevTool, etc.) |
| `litellm`      | incluído via `crewai[litellm]` | Camada de roteamento para Azure OpenAI |

---

## Configuração do LLM com Azure (`cognitiveservices.azure.com`)

### O problema

O CrewAI tem dois modos de chamar a Azure:

| Modo | SDK usado | Caminho da requisição |
|------|-----------|----------------------|
| Provider nativo (`azure/`) | `azure-ai-inference` | `/models/<deployment>/chat/completions` |
| LiteLLM (`is_litellm=True`) | `openai` (com config Azure) | `/openai/deployments/<deployment>/chat/completions` |

Recursos do tipo `cognitiveservices.azure.com` servem modelos Azure OpenAI pelo caminho `/openai/deployments/`. O provider nativo do CrewAI usa o caminho `/models/`, que é exclusivo de endpoints serverless do Azure AI Foundry. Com a configuração padrão (`MODEL=azure/gpt-5.4`), o CrewAI instanciava o provider nativo e as chamadas retornavam `404 Resource not found`.

### A correção em `crew.py`

O LLM é instanciado explicitamente com `is_litellm=True`, forçando o roteamento pelo LiteLLM → SDK do OpenAI → caminho correto:

```python
_llm = LLM(
    model=os.environ["MODEL"],
    is_litellm=True,
    api_base=os.environ["AZURE_API_BASE"],
    api_key=os.environ["AZURE_API_KEY"],
    api_version=os.environ["AZURE_API_VERSION"],
)
```

Esse objeto é passado explicitamente para cada agente via `llm=_llm`. Sem isso, o CrewAI leria o `MODEL` do ambiente e escolheria o provider nativo automaticamente.

### Dependência adicional

O LiteLLM não vem instalado por padrão. Execute uma vez:

```bash
uv add 'crewai[litellm]'
```
