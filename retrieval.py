import os

from dotenv import load_dotenv
from openai import OpenAI

from vector_db import search_documents


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

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
# RETRIEVAL
# ============================================================

def search(query, top_k=3):

    # Convert the user's question into an embedding
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    query_embedding = response.data[0].embedding

    # Search ChromaDB
    results = search_documents(
        query_embedding,
        top_k=top_k
    )

    return results