from voyageai.client import Client
from django.conf import settings

_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = settings.VOYAGE_API_KEY
        if not api_key:
            raise ValueError(
                "VOYAGE_API_KEY is not set. Add it to your .env file."
            )
        _client = Client(api_key=api_key)
    return _client


def generate_embedding(text: str) -> list:
    """Generate a vector embedding for the given text using Voyage AI."""
    client = _get_client()
    result = client.embed(
        [text],
        model="voyage-finance-2",
        input_type="document",
    )
    return result.embeddings[0]


def generate_query_embedding(text: str) -> list:
    """Generate a query-optimised embedding for semantic search."""
    client = _get_client()
    result = client.embed(
        [text],
        model="voyage-finance-2",
        input_type="query",
    )
    return result.embeddings[0]
