import os
import pickle

import requests
from scipy.spatial.distance import cosine

from src.config import HEADERS, settings

from .embedder import get_embeddings

project_root = os.path.dirname(os.path.dirname(__file__))
embeddings_path = os.path.join(project_root, "embeddings.pkl")

if os.path.exists(embeddings_path):
    with open(embeddings_path, "rb") as f:
        embeds = pickle.load(f)
else:
    from src.helper.classification_embeddings import (
        build_classification_base_embeddings,
    )

    build_classification_base_embeddings()
    with open(embeddings_path, "rb") as f:
        embeds = pickle.load(f)


tech_embeds = embeds["tech"]
cust_embeds = embeds["cust"]
small_embeds = embeds["talk"]


def query(payload):
    response = requests.post(
        settings.MULTILINGUAL_MINILM_L12_CLASSIFICATION_URL,
        headers=HEADERS,
        json=payload,
    )
    return response.json()


def classify(query, threshold=0.3):
    query_vec = get_embeddings([query])[0]

    scores = {
        "tech": min(cosine(query_vec, vec) for vec in tech_embeds),
        "customer": min(cosine(query_vec, vec) for vec in cust_embeds),
        "small_talk": min(cosine(query_vec, vec) for vec in small_embeds),
    }

    best_category = min(scores, key=scores.get)
    best_score = scores[best_category]

    return best_category if best_score < threshold else "unknown"
