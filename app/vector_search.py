import ollama

from app.vector_store import get_collection


EMBEDDING_MODEL = "nomic-embed-text"


def create_query_embedding(query):

    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=query
    )

    return response["embeddings"][0]


def search_vectors(
    query,
    top_k=5,
    category=None,
    document_type=None
):

    query_embedding = (
        create_query_embedding(query)
    )

    collection = get_collection()

    query_parameters = {
        "query_embeddings": [
            query_embedding
        ],
        "n_results": top_k
    }

    filters = []

    if category:

        filters.append(
            {
                "category": category
            }
        )

    if document_type:

        filters.append(
            {
                "document_type": document_type
            }
        )

    if len(filters) == 1:

        query_parameters["where"] = (
            filters[0]
        )

    elif len(filters) > 1:

        query_parameters["where"] = {
            "$and": filters
        }

    results = collection.query(
        **query_parameters
    )

    return results


if __name__ == "__main__":

    query = (
        "What are the requirements "
        "for registering a new user?"
    )

    print(
        f"Question:\n{query}"
    )

    print(
        "\nSearching vector database...\n"
    )

    results = search_vectors(
        query,
        top_k=5
    )

    documents = results["documents"][0]

    distances = results["distances"][0]

    metadatas = results["metadatas"][0]

    for index, document in enumerate(
        documents
    ):

        metadata = metadatas[index]

        print(
            f"Result {index + 1}"
        )

        print(
            f"Distance: "
            f"{distances[index]:.4f}"
        )

        print(
            f"Source: "
            f"{metadata['source']}"
        )

        print(
            f"Type: "
            f"{metadata['document_type']}"
        )

        print(
            f"Category: "
            f"{metadata['category']}"
        )

        print(
            f"Chunk: "
            f"{metadata['chunk_id']}"
        )

        if "page_number" in metadata:

            print(
                f"Page: "
                f"{metadata['page_number']}"
            )

        if "sheet_name" in metadata:

            print(
                f"Sheet: "
                f"{metadata['sheet_name']}"
            )

        print(
            f"Text: {document}"
        )

        print(
            "\n" + "-" * 60
        )