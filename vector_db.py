import chromadb


# ============================================================
# CHROMADB CLIENT
# ============================================================

client = chromadb.PersistentClient(
    path="chroma_db"
)


# ============================================================
# COLLECTION
# ============================================================

collection = client.get_or_create_collection(
    name="personal_knowledge"
)


# ============================================================
# GET COLLECTION
# ============================================================

def get_collection():

    return collection


# ============================================================
# SEARCH DOCUMENTS
# ============================================================

def search_documents(
    query_embedding,
    top_k=3
):

    # Handle an empty collection gracefully
    if collection.count() == 0:

        return []


    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=min(
            top_k,
            collection.count()
        )
    )


    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]


    output = []


    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        output.append(
            {
                "content": document,
                "source": metadata.get(
                    "source",
                    "unknown"
                ),
                "distance": distance
            }
        )


    return output