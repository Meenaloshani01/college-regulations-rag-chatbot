
import json
import re
from pathlib import Path

import fitz  # PyMuPDF


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_FOLDER = PROJECT_ROOT / "data" / "raw"
PROCESSED_FOLDER = PROJECT_ROOT / "data" / "processed"

CHUNK_SIZE = 700
CHUNK_OVERLAP = 100


def extract_text(file_path):
    """Extract text from a TXT or PDF file."""

    if file_path.suffix.lower() == ".txt":
        return file_path.read_text(encoding="utf-8")

    if file_path.suffix.lower() == ".pdf":
        text_parts = []

        with fitz.open(file_path) as pdf:
            for page in pdf:
                text_parts.append(page.get_text())

        return "\n".join(text_parts)

    return ""


def clean_text(text):
    """Normalize whitespace while preserving readable text."""

    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def split_into_chunks(text):
    """Split text into overlapping character-based chunks."""

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = end - CHUNK_OVERLAP

    return chunks


def process_documents():
    PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)

    all_chunks = []
    supported_extensions = {".txt", ".pdf"}

    for file_path in sorted(RAW_FOLDER.iterdir()):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in supported_extensions:
            continue

        raw_text = extract_text(file_path)
        cleaned_text = clean_text(raw_text)

        if not cleaned_text:
            print(f"WARNING: No text extracted from {file_path.name}")
            continue

        chunks = split_into_chunks(cleaned_text)

        for index, chunk in enumerate(chunks, start=1):
            all_chunks.append({
                "chunk_id": f"{file_path.stem}_{index}",
                "source": file_path.name,
                "text": chunk
            })

        print(f"Processed {file_path.name}: {len(chunks)} chunks")

    output_path = PROCESSED_FOLDER / "chunks.json"

    output_path.write_text(
        json.dumps(all_chunks, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"\nTotal chunks: {len(all_chunks)}")
    print(f"Output saved to: {output_path}")


if __name__ == "__main__":
    process_documents()
