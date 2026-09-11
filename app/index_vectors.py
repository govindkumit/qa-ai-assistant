import json
from pathlib import Path

from app.vector_store import get_collection


EMBEDDINGS_FILE = Path(
    "data/embeddings.json"
)


def load_embeddings():

    with EMBEDDINGS_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def get_document_type(source):

    extension = Path(
        source
    ).suffix.lower()

    types = {
        ".txt": "text",
        ".pdf": "pdf",
        ".docx": "word",
        ".xlsx": "excel"
    }

    return types.get(
        extension,
        "unknown"
    )


def get_category(source):

    source_lower = source.lower()

    categories = [
        "login",
        "registration",
        "checkout",
        "payment",
        "api",
        "security",
        "user",
        "order"
    ]

    for category in categories:

        if category in source_lower:
            return category

    return "general"


def index_embeddings():

    records = load_embeddings()

    collection = get_collection()

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for record in records:

        source = record["source"]

        chunk_id = record["chunk_id"]

        record_id = (
            f"{source}_{chunk_id}"
        )

        ids.append(record_id)

        documents.append(
            record["text"]
        )

        embeddings.append(
            record["embedding"]
        )

        metadata = {
            "source": source,
            "document_name": Path(
                source
            ).stem,
            "document_type": (
                get_document_type(source)
            ),
            "category": (
                get_category(source)
            ),
            "chunk_id": chunk_id
        }

        if "page_number" in record:

            metadata["page_number"] = (
                record["page_number"]
            )

        if "sheet_name" in record:

            metadata["sheet_name"] = (
                record["sheet_name"]
            )

        metadatas.append(metadata)

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(
        f"Indexed {len(records)} chunks."
    )

    print(
        f"Collection: "
        f"{collection.name}"
    )

    print(
        f"Total vectors: "
        f"{collection.count()}"
    )


if __name__ == "__main__":
    index_embeddings()