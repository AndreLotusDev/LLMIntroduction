from datasets import load_dataset
from pathlib import Path

# Load dataset
dataset = load_dataset("ccdv/pubmed-summarization")

# Get one sample
sample = dataset["train"][0]

article = sample["article"]
abstract = sample["abstract"]

# Output paths
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

article_file = output_dir / "long_doc.txt"
summary_file = output_dir / "ref_summary.txt"

# Save files
article_file.write_text(article, encoding="utf-8")
summary_file.write_text(abstract, encoding="utf-8")

print(f"Article saved at: {article_file}")
print(f"Reference summary saved at: {summary_file}")