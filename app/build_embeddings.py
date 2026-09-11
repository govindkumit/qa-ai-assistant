import json
from pathlib import Path

from app.chunker import (
    load_documents,
    chunk_document
)

from app.embedder import create_embedding


OUTPUT_FILE = Path(
    "data/embeddings.json"
)


def build_embeddings():

    documents = load_documents()

    records = []

    for document in documents:

        chunks = chunk_document(
            document["text"]
        )

        for index, chunk in enumerate(
            chunks,
            start=1
        ):

            print(
                f"Embedding "
                f"{document['source']} "
                f"chunk {index}..."
            )

            embedding = create_embedding(
                chunk
            )

            record = {
                "source": document["source"],
                "chunk_id": index,
                "text": chunk,
                "embedding": embedding
            }

            if "page_number" in document:

                record["page_number"] = (
                    document["page_number"]
                )

            if "sheet_name" in document:

                record["sheet_name"] = (
                    document["sheet_name"]
                )

            records.append(record)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            records,
            file,
            indent=2
        )

    print(
        f"\nCreated {len(records)} embeddings."
    )

    print(
        f"Saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    build_embeddings()