from pathlib import Path


DATA_DIR = Path("data")


def load_documents():
    documents = []

    for file_path in DATA_DIR.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        documents.append({
            "source": file_path.name,
            "content": content
        })

    return documents


def chunk_text(text, chunk_size=800):
    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def create_chunks():
    documents = load_documents()

    chunks = []

    for document in documents:

        document_chunks = chunk_text(
            document["content"]
        )

        for chunk in document_chunks:

            chunks.append({
                "source": document["source"],
                "content": chunk
            })

    return chunks