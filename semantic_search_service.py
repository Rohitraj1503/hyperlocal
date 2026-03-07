"""
Semantic Search Service
-----------------------
Ranks products against a query using sentence-transformer embeddings
and cosine similarity.

Model: all-MiniLM-L6-v2  (fast, lightweight, good quality)
Run standalone: python semantic_search_service.py
"""

from sentence_transformers import SentenceTransformer, util
from typing import List

# Load model once at module level so it's reused across calls
_MODEL_NAME = "all-MiniLM-L6-v2"
_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    """Lazy-load the embedding model (downloads on first use)."""
    global _model
    if _model is None:
        print(f"[semantic_search] Loading model '{_MODEL_NAME}'...")
        _model = SentenceTransformer(_MODEL_NAME)
    return _model


def semantic_search(query: str, product_list: List[str], top_k: int = 5) -> List[dict]:
    """
    Rank products by semantic similarity to a query.

    Args:
        query:        Natural language search string, e.g. "cold drink"
        product_list: List of product name strings to search within.
        top_k:        Maximum number of results to return.

    Returns:
        List of dicts sorted by score descending:
        [{"product": str, "score": float}, ...]
    """
    if not product_list:
        return []

    model = _get_model()

    # Encode query and all product names
    query_embedding = model.encode(query, convert_to_tensor=True)
    product_embeddings = model.encode(product_list, convert_to_tensor=True)

    # Cosine similarity between query and every product
    scores = util.cos_sim(query_embedding, product_embeddings)[0]

    # Build result list and sort by score
    results = [
        {"product": product_list[i], "score": round(float(scores[i]), 4)}
        for i in range(len(product_list))
    ]
    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:top_k]


# ── Standalone test ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    query = "cold drink"
    products = ["Coca Cola", "Pepsi", "Sprite", "Amul Milk", "Orange Juice", "Water Bottle"]

    print(f"Query: '{query}'")
    print(f"Products: {products}\n")

    matches = semantic_search(query, products)
    print("Ranked results:")
    for rank, item in enumerate(matches, 1):
        print(f"  {rank}. {item['product']}  (score: {item['score']})")
