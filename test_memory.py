from memory_extractor import extract_memory


message = (
    "I want to become stronger in RAG and "
    "move towards AI engineering."
)


print("=" * 60)

print("USER:")

print(message)

print("\nEXTRACTED MEMORY:")

print(
    extract_memory(message)
)