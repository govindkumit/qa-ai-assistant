import ollama

text = "An account is locked after 5 consecutive failed login attempts."

response = ollama.embed(
    model="nomic-embed-text",
    input=text
)

embedding = response["embeddings"][0]

print("Text:")
print(text)

print("\nEmbedding:")
print(embedding)

print("\nNumber of dimensions:")
print(len(embedding))