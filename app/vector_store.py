import chromadb


CHROMA_PATH = "data/chroma_db"

COLLECTION_NAME = "qa_knowledge"


def get_collection():

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection