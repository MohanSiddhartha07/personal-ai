from retrieval import search


query = "What projects have I worked on using Azure?"


results = search(
    query,
    top_k=3
)


print("\nSEARCH RESULTS")
print("=" * 60)


for i, result in enumerate(results):

    print(f"\nResult {i + 1}")

    print(
        f"Source: {result['source']}"
    )

    print(
        f"Distance: {result['distance']:.4f}"
    )

    print("\nContent:")

    print(
        result["content"][:500]
    )