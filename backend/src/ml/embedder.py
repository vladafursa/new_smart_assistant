import logging

import requests
from requests.exceptions import HTTPError, RequestException

from src.config import HEADERS, MULTILINGUAL_E5_EMBEDDER_URL, TIMEOUT

logger = logging.getLogger(__name__)

_LOCAL_MODEL = None


def _get_local_model():
    global _LOCAL_MODEL
    if _LOCAL_MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer

            logger.info(
                "Loading local embedding model - intfloat/multilingual-e5-large ..."
            )
            _LOCAL_MODEL = SentenceTransformer("intfloat/multilingual-e5-large")
        except ImportError:
            logger.error(
                "sentence-transformers is not installed. Local fallback unavailable."
            )
            _LOCAL_MODEL = None
    return _LOCAL_MODEL


def get_embeddings(texts):
    if isinstance(texts, str):
        texts = [texts]

    payload = {"inputs": texts}

    # hugging face API trial
    try:
        response = requests.post(
            MULTILINGUAL_E5_EMBEDDER_URL, headers=HEADERS, json=payload, timeout=TIMEOUT
        )
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and "error" in data:
            raise ValueError(f"HF returned error: {data['error']}")

        if not isinstance(data, list):
            raise ValueError("Invalid HF response format")

        logger.debug("HF embeddings retrieved successfully.")
        return data

    except (HTTPError, RequestException, ValueError) as e:
        logger.warning("HF embeddings failed: %s", e)

    # fallback to local model
    model = _get_local_model()
    if model is None:
        raise RuntimeError(
            "Embedding service is unavailable and local model is not installed."
        )

    try:
        return model.encode(texts, normalize_embeddings=True).tolist()
    except Exception as local_error:
        logger.error("Local embedding model failed: %s", local_error)
        raise RuntimeError("Embedding service is unavailable")
