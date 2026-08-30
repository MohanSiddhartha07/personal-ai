from chunking import create_chunks
from embeddings import create_embeddings
from vector_db import add_documents


print("Loading documents...")

chunks = create_chunks()

print(f"Created {len(chunks)} chunks.")


print("Creating embeddings...")

embeddings = create_embeddings(chunks)


print("Adding documents to ChromaDB...")

add_documents(embeddings)


print("Indexing complete!")