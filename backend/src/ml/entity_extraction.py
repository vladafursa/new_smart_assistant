import logging

import requests
from requests.exceptions import HTTPError, RequestException

from src.config import CHAT_COMPLETIONS_URL, HUGGINGFACE_KEY

logger = logging.getLogger(__name__)

_LOCAL_MODEL = None

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_KEY}",
    "Content-Type": "application/json",
}


def _get_local_model():
    """Lazy-load a local spaCy NER model."""
    global _LOCAL_MODEL
    if _LOCAL_MODEL is None:
        try:
            import spacy

            logger.info("Loading local spaCy NER model - en_core_web_sm ...")
            _LOCAL_MODEL = spacy.load("en_core_web_sm")
        except ImportError:
            logger.error("spaCy is not installed. Local fallback unavailable.")
            _LOCAL_MODEL = None
        except OSError:
            logger.error(
                "spaCy model 'en_core_web_sm' not downloaded."
                "Run: python -m spacy download en_core_web_sm"
            )
            _LOCAL_MODEL = None
    return _LOCAL_MODEL


def extract_entities(question):
    system_prompt = (
        "You are a support assistant who extracts key entities from text."
        "Entities include people, organizations, places,"
        "dates, technologies, and other important elements."
        "Return only the raw entity names as a plain list."
        "Do not include explanations, categories, types, or any text in parentheses."
    )

    user_prompt = (
        f"Extract key entities from the following question:\n\n{question}\n\n"
        "Format: plain list of entity names only."
        "No parentheses, no descriptions, no types."
    )

    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 256,
    }

    # try Hugging Face API
    try:
        response = requests.post(
            CHAT_COMPLETIONS_URL, headers=headers, json=payload, timeout=30
        )
        response.raise_for_status()
        raw = response.json()["choices"][0]["message"]["content"].strip()

        try:
            import json

            entities = json.loads(raw)
            if isinstance(entities, list):
                return [e.strip() for e in entities if isinstance(e, str)]
        except Exception:
            # fallback: strip bullets manually
            return [
                line.lstrip("-•* ").strip() for line in raw.split("\n") if line.strip()
            ]

    except (HTTPError, RequestException, KeyError, IndexError, ValueError) as e:
        logger.warning("HF entity extraction failed: %s", e)

    # fallback to local spaCy model
    model = _get_local_model()
    if model is None:
        raise RuntimeError(
            "Entity extraction service unavailable and local model not installed."
        )

    try:
        doc = model(question)
        entities = [ent.text for ent in doc.ents]
        # If none found, fall back to noun chunks
        if not entities:
            entities = [chunk.text for chunk in doc.noun_chunks]
        return entities
    except Exception as local_error:
        logger.error("Local entity extraction model failed: %s", local_error)
        raise RuntimeError("Entity extraction service unavailable")
