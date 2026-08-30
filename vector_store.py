import json
from pathlib import Path


VECTOR_STORE = Path("vector_store.json")


def save_embeddings(embeddings):

    with open(VECTOR_STORE, "w", encoding="utf-8") as file:
        json.dump(embeddings, file)


def load_embeddings():

    if not VECTOR_STORE.exists():
        return []

    with open(VECTOR_STORE, "r", encoding="utf-8") as file:
        return json.load(file)