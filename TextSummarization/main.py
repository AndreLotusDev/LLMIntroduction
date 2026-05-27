# pip install openai python-dotenv tiktoken evaluate rouge-score absl-py nltk matplotlib

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional, Dict

import evaluate
import matplotlib.pyplot as plt
import tiktoken
from dotenv import load_dotenv
from openai import AzureOpenAI


# =========================
# Config
# =========================

load_dotenv()

AZURE_OPENAI_API_URL = os.getenv("AZURE_OPENAI_API_URL")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5.2")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")

INPUT_FILE = Path("long_doc.txt")
REFERENCE_FILE = Path("ref_summary.txt")

OUTPUT_DIR = Path("output")
AUDIT_DIR = Path("audit")

FINAL_SUMMARY_FILE = OUTPUT_DIR / "final_summary.md"
SCORES_FILE = OUTPUT_DIR / "evaluation_scores.json"
SCORES_PDF_FILE = OUTPUT_DIR / "evaluation_scores.pdf"
AUDIT_FILE = AUDIT_DIR / "summaries_audit.jsonl"

CHUNK_MAX_TOKENS = 2000
CHUNK_OVERLAP_TOKENS = 200
SUMMARY_MAX_TOKENS = 1024
FINAL_SUMMARY_MAX_TOKENS = 1500
ENCODING_NAME = "cl100k_base"


# =========================
# Setup
# =========================

def ensure_dirs() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    AUDIT_DIR.mkdir(exist_ok=True)


def require_env_var(value: Optional[str], name: str) -> str:
    if not value:
        raise ValueError(f"Missing {name} in environment")
    return value


client = AzureOpenAI(
    azure_endpoint=require_env_var(AZURE_OPENAI_API_URL, "AZURE_OPENAI_API_URL"),
    api_key=require_env_var(AZURE_OPENAI_API_KEY, "AZURE_OPENAI_API_KEY"),
    api_version=AZURE_OPENAI_API_VERSION,
)


# =========================
# Tokenization / Chunking
# =========================

def get_encoding():
    return tiktoken.get_encoding(ENCODING_NAME)


def count_tokens(text: str) -> int:
    return len(get_encoding().encode(text))


def split_text_by_paragraphs(text: str) -> List[str]:
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def get_overlap_text(text: str, overlap_tokens: int) -> str:
    if overlap_tokens <= 0:
        return ""

    encoding = get_encoding()
    tokens = encoding.encode(text)
    return encoding.decode(tokens[-overlap_tokens:])


def chunk_text_by_tokens(
    text: str,
    max_tokens: int,
    overlap_tokens: int,
) -> Iterable[str]:
    encoding = get_encoding()
    tokens = encoding.encode(text)

    step = max_tokens - overlap_tokens

    for start in range(0, len(tokens), step):
        yield encoding.decode(tokens[start:start + max_tokens])


def chunk_text(
    text: str,
    max_tokens: int = CHUNK_MAX_TOKENS,
    overlap_tokens: int = CHUNK_OVERLAP_TOKENS,
) -> List[str]:
    if overlap_tokens >= max_tokens:
        raise ValueError("overlap_tokens must be smaller than max_tokens")

    encoding = get_encoding()
    paragraphs = split_text_by_paragraphs(text)

    chunks: List[str] = []
    current_chunk: List[str] = []
    current_token_count = 0

    for paragraph in paragraphs:
        paragraph_tokens = len(encoding.encode(paragraph))

        if paragraph_tokens > max_tokens:
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = []
                current_token_count = 0

            chunks.extend(
                chunk_text_by_tokens(
                    paragraph,
                    max_tokens=max_tokens,
                    overlap_tokens=overlap_tokens,
                )
            )
            continue

        if current_token_count + paragraph_tokens > max_tokens:
            chunk = "\n\n".join(current_chunk)
            chunks.append(chunk)

            overlap_text = get_overlap_text(chunk, overlap_tokens)
            current_chunk = [overlap_text, paragraph] if overlap_text else [paragraph]
            current_token_count = len(encoding.encode("\n\n".join(current_chunk)))
        else:
            current_chunk.append(paragraph)
            current_token_count += paragraph_tokens

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks


# =========================
# Azure OpenAI
# =========================

def call_llm(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
    temperature: float = 0.2,
) -> str:
    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_completion_tokens=max_tokens,
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("LLM returned empty response")

    return content.strip()


def summarize_chunk(chunk: str, chunk_number: int, total_chunks: int) -> str:
    system_prompt = (
        "You summarize documents accurately. "
        "Keep important facts, names, numbers, dates, requirements, risks, and conclusions. "
        "Do not add information that is not present in the text."
    )

    user_prompt = f"""
Summarize chunk {chunk_number} of {total_chunks}.

Use this structure:
- Main points
- Important details
- Decisions or conclusions
- Risks or open questions, if any

Text:
{chunk}
""".strip()

    return call_llm(system_prompt, user_prompt, SUMMARY_MAX_TOKENS)


def consolidate_summaries(summaries: List[str]) -> str:
    joined_summaries = "\n\n".join(
        f"Chunk {index + 1} summary:\n{summary}"
        for index, summary in enumerate(summaries)
    )

    system_prompt = (
        "You consolidate partial summaries into one final summary. "
        "Preserve key facts, names, numbers, dates, decisions, risks, and conclusions. "
        "Remove repetition. Do not invent information."
    )

    user_prompt = f"""
Create one final structured summary from the partial summaries below.

Use this structure:
# Summary
## Main points
## Important details
## Decisions or conclusions
## Risks or open questions

Partial summaries:
{joined_summaries}
""".strip()

    return call_llm(system_prompt, user_prompt, FINAL_SUMMARY_MAX_TOKENS)


# =========================
# Audit
# =========================

def append_chunk_audit(
    chunk_number: int,
    total_chunks: int,
    chunk_text_value: str,
    chunk_summary: str,
) -> None:
    audit_record = {
        "timestamp": datetime.now().isoformat(),
        "chunk_number": chunk_number,
        "total_chunks": total_chunks,
        "chunk_tokens": count_tokens(chunk_text_value),
        "summary_tokens": count_tokens(chunk_summary),
        "chunk_text": chunk_text_value,
        "chunk_summary": chunk_summary,
    }

    with AUDIT_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(audit_record, ensure_ascii=False) + "\n")


def reset_audit_file() -> None:
    AUDIT_FILE.write_text("", encoding="utf-8")


# =========================
# Summarization Pipeline
# =========================

def summarize_long_text(text: str) -> str:
    chunks = chunk_text(text)
    total_chunks = len(chunks)

    summaries: List[str] = []

    for index, chunk in enumerate(chunks, start=1):
        print(f"Summarizing chunk {index}/{total_chunks}...")

        summary = summarize_chunk(chunk, index, total_chunks)
        summaries.append(summary)

        append_chunk_audit(
            chunk_number=index,
            total_chunks=total_chunks,
            chunk_text_value=chunk,
            chunk_summary=summary,
        )

    if len(summaries) == 1:
        return summaries[0]

    return consolidate_summaries(summaries)


# =========================
# Evaluation
# =========================

def load_reference_summary(path: Path) -> Optional[str]:
    if not path.exists():
        return None

    return path.read_text(encoding="utf-8").strip()


def evaluate_summary(summary: str, reference_summary: str) -> Dict[str, float]:
    rouge = evaluate.load("rouge")
    meteor = evaluate.load("meteor")

    rouge_scores = rouge.compute(
        predictions=[summary],
        references=[reference_summary],
    )

    meteor_scores = meteor.compute(
        predictions=[summary],
        references=[reference_summary],
    )

    return {
        "rouge1": rouge_scores["rouge1"],
        "rouge2": rouge_scores["rouge2"],
        "rougeL": rouge_scores["rougeL"],
        "meteor": meteor_scores["meteor"],
    }


def save_scores(scores: Dict[str, float]) -> None:
    SCORES_FILE.write_text(
        json.dumps(scores, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def export_scores_chart_pdf(scores: Dict[str, float]) -> None:
    labels = list(scores.keys())
    values = list(scores.values())

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.ylim(0, 1)
    plt.title("Summary Evaluation Scores")
    plt.xlabel("Metric")
    plt.ylabel("Score")

    for index, value in enumerate(values):
        plt.text(index, value + 0.02, f"{value:.3f}", ha="center")

    plt.tight_layout()
    plt.savefig(SCORES_PDF_FILE, format="pdf")
    plt.close()


# =========================
# Main
# =========================

def main() -> None:
    ensure_dirs()
    reset_audit_file()

    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    text = INPUT_FILE.read_text(encoding="utf-8")
    reference_summary = load_reference_summary(REFERENCE_FILE)

    print("Summarizing...")
    print(f"Input tokens: {count_tokens(text)}")

    summary = summarize_long_text(text)

    FINAL_SUMMARY_FILE.write_text(summary, encoding="utf-8")

    print("\nSummary saved at:")
    print(FINAL_SUMMARY_FILE)

    print("\nChunk audit saved at:")
    print(AUDIT_FILE)

    if reference_summary:
        scores = evaluate_summary(summary, reference_summary)

        save_scores(scores)
        export_scores_chart_pdf(scores)

        print("\nEvaluation scores:")
        for metric, value in scores.items():
            print(f"{metric}: {value:.3f}")

        print("\nScores JSON saved at:")
        print(SCORES_FILE)

        print("\nScores chart PDF saved at:")
        print(SCORES_PDF_FILE)
    else:
        print("\nNo reference summary provided — metrics and chart skipped.")


if __name__ == "__main__":
    main()