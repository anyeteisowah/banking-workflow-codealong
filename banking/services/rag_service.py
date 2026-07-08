from .embedding_service import generate_query_embedding
from .vector_search_service import semantic_search


def answer_query(
    question: str,
    document_type: str | None = None,
    limit: int = 5,
) -> dict:
    """
        Retrieval pipeline:
      1. Embed the question with Voyage AI
      2. Retrieve relevant documents via Atlas Vector Search
            3. Return the most relevant document context

    Returns:
        {"answer": str, "sources": list[dict]}
    """
    # 1. Retrieve relevant documents
    query_embedding = generate_query_embedding(question)
    sources = semantic_search(query_embedding, limit=limit, document_type=document_type)

    if not sources:
        return {
            "answer": "No relevant documents were found for your query.",
            "sources": [],
        }

    # 2. Build retrieval context
    context_parts = []
    for i, doc in enumerate(sources, 1):
        context_parts.append(
            f"[Document {i}] {doc['title']} ({doc['document_type']})\n"
            f"Customer: {doc['customer_name']} ({doc['customer_id']})\n"
            f"Status: {doc['status']}\n"
            f"Similarity score: {doc.get('score', 0):.4f}\n"
            f"Content:\n{doc['content'][:800]}"
        )
    context = "\n\n---\n\n".join(context_parts)

    answer = (
        "Here are the most relevant documents found for your question. "
        "Review the retrieved context and sources below for the answer.\n\n"
        f"Question: {question}\n\n"
        f"{context}"
    )

    return {"answer": answer, "sources": sources}
