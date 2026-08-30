import chromadb

from dotenv import load_dotenv
import os

from openai import OpenAI

from chunking import create_chunks


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY not found."
    )


# ============================================================
# OPENAI
# ============================================================

client = OpenAI(
    api_key=api_key
)


# ============================================================
# CHROMADB
# ============================================================

chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)


# ============================================================
# CHECK EXISTING COLLECTION
# ============================================================

try:

    collection = chroma_client.get_collection(
        name="personal_knowledge"
    )

    if collection.count() > 0:

        print(
            f"ChromaDB already contains "
            f"{collection.count()} documents."
        )

        print(
            "Skipping RAG setup."
        )

        exit()

except Exception:

    pass


# ============================================================
# CREATE COLLECTION
# ============================================================

try:

    chroma_client.delete_collection(
        name="personal_knowledge"
    )

except Exception:

    pass


collection = chroma_client.create_collection(
    name="personal_knowledge"
)


# ============================================================
# LOAD CHUNKS
# ============================================================

chunks = create_chunks()

print(
    f"Creating embeddings for "
    f"{len(chunks)} chunks..."
)


# ============================================================
# CREATE EMBEDDINGS
# ============================================================

for index, chunk in enumerate(chunks):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunk["content"]
    )

    embedding = response.data[0].embedding


    collection.add(

        ids=[
            str(index)
        ],

        documents=[
            chunk["content"]
        ],

        embeddings=[
            embedding
        ],

        metadatas=[
            {
                "source": chunk["source"]
            }
        ]
    )


    print(
        f"Added {index + 1}/{len(chunks)}"
    )


# ============================================================
# COMPLETE
# ============================================================

print()
print("=" * 60)
print("RAG setup complete.")
print("=" * 60)

print(
    f"Documents: {collection.count()}"
)