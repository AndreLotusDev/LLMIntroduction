import os
import shutil

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


DOCUMENT_PATH = "hr_policy_long.txt"
PERSIST_DIR = "./hr_chroma_db"


def load_document():
    loader = TextLoader(
        DOCUMENT_PATH,
        encoding="utf-8"
    )

    return loader.load()


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    return splitter.split_documents(documents)


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


def create_vector_db(documents, embeddings):
    if os.path.exists(PERSIST_DIR):
        print("Removing old vector database...")
        shutil.rmtree(PERSIST_DIR)

    print("Creating vector database...")

    Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=PERSIST_DIR,
    )


def main():
    print("Loading document...")
    documents = load_document()

    print("Splitting document...")
    split_docs = split_documents(documents)

    print(f"Chunks created: {len(split_docs)}")

    print("Loading local embedding model...")
    embeddings = create_embeddings()

    print("Generating embeddings and storing vectors...")
    create_vector_db(split_docs, embeddings)

    print("Ingestion completed successfully.")


if __name__ == "__main__":
    main()