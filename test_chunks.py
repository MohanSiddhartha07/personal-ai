from chunking import create_chunks


chunks = create_chunks()

print(f"Total chunks: {len(chunks)}")

for i, chunk in enumerate(chunks):

    print("\n" + "=" * 60)

    print(f"Chunk {i + 1}")
    print(f"Source: {chunk['source']}")

    print(chunk["content"][:300])