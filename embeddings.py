import chromadb

from dotenv import load_dotenv
import os

from openai import OpenAI

from chunking import create_chunks


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

api_key = os.getenv(
    "OPENAI_API_KEY"
)

if not api_key:

    raise ValueError(
        "OPENAI_API_KEY not found in .env file"
    )


# ============================================================
# OPENAI CLIENT
# ============================================================

client = OpenAI(
    api_key=api_key
)


# ============================================================
# EMBEDDING FUNCTION
# ============================================================

def create_embedding(text):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


# ============================================================
# LOAD CHUNKS
# ============================================================

chunks = create_chunks()

print(
    f"Total chunks: {len(chunks)}"
)


# ============================================================
# CHROMADB
# ============================================================

chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)


# ============================================================
# DELETE OLD COLLECTION
# ============================================================

try:

    chroma_client.delete_collection(
        name="personal_knowledge"
    )

    print(
        "Deleted old ChromaDB collection."
    )

except Exception:

    print(
        "No existing collection to delete."
    )


# ============================================================
# CREATE NEW COLLECTION
# ============================================================

collection = chroma_client.create_collection(
    name="personal_knowledge"
)


# ============================================================
# GENERATE EMBEDDINGS
# ============================================================

ids = []
documents = []
embeddings = []
metadatas = []


for index, chunk in enumerate(chunks):

    embedding = create_embedding(
        chunk["content"]
    )

    ids.append(
        str(index)
    )

    documents.append(
        chunk["content"]
    )

    embeddings.append(
        embedding
    )

    metadatas.append(
        {
            "source": chunk["source"]
        }
    )

    print(
        f"Created embedding "
        f"{index + 1}/{len(chunks)}"
    )


# ============================================================
# STORE IN CHROMADB
# ============================================================

collection.add(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
)


# ============================================================
# VERIFY
# ============================================================

print()

print("=" * 60)

print(
    "OpenAI vector database rebuilt successfully."
)

print("=" * 60)

print(
    f"Total embeddings: {len(embeddings)}"
)

print(
    f"Embedding dimensions: "
    f"{len(embeddings[0])}"
)