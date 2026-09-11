from app.vector_search import search_vectors


def search(query, top_k=3):
    results = search_vectors(query, top_k=top_k)

    documents = results["documents"][0]
    distances = results["distances"][0]
    metadatas = results["metadatas"][0]

    formatted_results = []

    for index, document in enumerate(documents):
        metadata = metadatas[index]

        formatted_results.append({
            "source": metadata["source"],
            "chunk_id": metadata["chunk_id"],
            "text": document,
            "distance": distances[index]
        })

    return formatted_results