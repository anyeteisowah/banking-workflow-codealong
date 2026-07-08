from pymongo import MongoClient
from django.conf import settings

_client = None


def _get_collection():
    global _client
    if _client is None:
        db_config = settings.DATABASES["default"]
        uri = db_config.get("HOST")
        _client = MongoClient(uri) if uri else MongoClient()
    db_name = settings.DATABASES["default"]["NAME"]
    return _client[db_name]["banking_bankingdocument"]


def semantic_search(
    query_embedding: list[float],
    limit: int = 5,
    document_type: str | None = None,
) -> list[dict]:
    """
    Run a MongoDB Atlas Vector Search against the banking documents collection.

    Returns a list of dicts with document fields plus a 'score' key.
    """
    collection = _get_collection()

    pipeline = [
        {
            "$vectorSearch": {
                "index": "banking_embedding_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": limit * 10,
                "limit": limit,
            }
        },
        {
            "$project": {
                "_id": 1,
                "title": 1,
                "content": 1,
                "document_type": 1,
                "status": 1,
                "customer_name": 1,
                "customer_id": 1,
                "score": {"$meta": "vectorSearchScore"},
            }
        },
    ]

    if document_type:
        pipeline.insert(1, {"$match": {"document_type": document_type}})

    results = list(collection.aggregate(pipeline))

    # Convert ObjectId to string for template rendering
    for doc in results:
        doc["id"] = str(doc.pop("_id"))

    return results
