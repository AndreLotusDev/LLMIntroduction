import os
from dotenv import load_dotenv

from langchain_openai import AzureChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


PERSIST_DIR = "./hr_chroma_db"
API_VERSION = "2024-12-01-preview"


def load_config():
    load_dotenv()

    api_url = os.getenv("AZURE_OPENAI_API_URL")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")

    if not api_url:
        raise ValueError("Missing AZURE_OPENAI_API_URL")

    if not api_key:
        raise ValueError("Missing AZURE_OPENAI_API_KEY")

    return {
        "api_url": api_url,
        "api_key": api_key,
        "chat_deployment": os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-5.2"),
    }


def create_llm(config):
    return AzureChatOpenAI(
        azure_endpoint=config["api_url"],
        api_key=config["api_key"],
        api_version=API_VERSION,
        azure_deployment=config["chat_deployment"],
        temperature=0,
    )


def create_embeddings():
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={
            "device": "cpu"
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )


def load_vector_db(embeddings):
    if not os.path.exists(PERSIST_DIR):
        raise FileNotFoundError(
            f"Vector database not found at {PERSIST_DIR}. "
            "Run ingest.py first."
        )

    return Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings,
    )


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def create_qa_chain(retriever, llm):
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an HR assistant for Acme Corporation.

Answer employee questions using the HR policy context below.

Rules:
1. If the policy addresses the topic explicitly, answer directly.
2. If the exact item is not mentioned, reason from the closest relevant policy \
(e.g. Safety Policy, Workplace Conduct) to give a practical answer and cite that policy.
3. Only say "I don't know" when the question has absolutely no connection to any HR policy.

Context:
{context}

Question:
{question}

Answer:
"""
    )

    return (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )


def main():
    config = load_config()

    llm = create_llm(config)
    embeddings = create_embeddings()

    vectordb = load_vector_db(embeddings)

    retriever = vectordb.as_retriever(
        search_kwargs={"k": 4}
    )

    qa_chain = create_qa_chain(retriever, llm)

    query = input("Ask a question: ")

    response = qa_chain.invoke(query)

    print("\nQ:", query)
    print("A:", response)


if __name__ == "__main__":
    main()