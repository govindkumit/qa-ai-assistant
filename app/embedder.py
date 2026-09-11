import ollama


EMBEDDING_MODEL = "nomic-embed-text"


def create_embedding(text):
    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response["embeddings"][0]


if __name__ == "__main__":

    text = "An account is locked after 5 failed login attempts."

    embedding = create_embedding(text)

    print("Text:")
    print(text)

    print("\nEmbedding dimensions:")
    print(len(embedding))

    print("\nFirst 10 values:")
    print(embedding[:10])