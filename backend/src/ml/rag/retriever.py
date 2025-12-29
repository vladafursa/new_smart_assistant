from src.ml import extract_entities, get_embeddings


def query_index(index, query, category=None, top_k=2):
    query_emb = get_embeddings([query])[0]
    namespace = category if category != "unknown" else None
    entities = extract_entities(query)

    print(f"Extracted entities: {entities}")
    filter = {"entities": {"$in": entities}} if entities else None
    results = index.query(
        vector=query_emb,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace,
        filter=filter,
    )
    if len(results["matches"]) < top_k:
        print("Not enough matches with filters, repeating without it")
        results = index.query(
            vector=query_emb, top_k=top_k, include_metadata=True, namespace=namespace
        )
    print(f"\n Top {top_k} results for query: {query}\n")
    context_chunks = []
    for match in results["matches"]:
        score = match["score"]
        meta = match["metadata"]
        chunk_data = {
            "text": meta.get("text", ""),
            "source": meta.get("source", ""),
            "category": namespace or "unknown",
            "entities": meta.get("entities", []),
        }
        context_chunks.append(chunk_data)
        print(f"• Score: {score:.3f}")
        print(f"  Text: {chunk_data['text'][:200]}...\n")

    return context_chunks
