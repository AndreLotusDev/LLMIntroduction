import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

load_dotenv()

api_url = os.getenv("AZURE_OPENAI_API_URL")
api_key = os.getenv("AZURE_OPENAI_API_KEY")

if not api_url:
    raise ValueError("Missing AZURE_OPENAI_API_URL in environment")

if not api_key:
    raise ValueError("Missing AZURE_OPENAI_API_KEY in environment")

llm = AzureChatOpenAI(
    azure_endpoint=api_url,
    api_key=api_key,
    api_version="2024-12-01-preview",
    azure_deployment="gpt-5.2",
    temperature=0,
)

prompt = PromptTemplate(
    input_variables=["text"],
    template=(
        'Classify the sentiment of the following text '
        'as positive, neutral, or negative:\n\n"{text}"'
    ),
)

chain = prompt | llm  # LCEL RunnableSequence

def analyze_sentiment(text: str) -> str:
    result = chain.invoke({"text": text})
    return result.content.strip()

if __name__ == "__main__":
    samples = [
        "I absolutely love this product!",
        "It's okay, could be better.",
        "Worst experience ever."
    ]

    for s in samples:
        print(f"Text: {s}\nSentiment: {analyze_sentiment(s)}\n")