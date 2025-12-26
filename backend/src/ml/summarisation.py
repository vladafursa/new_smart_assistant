import logging

import requests
from requests.exceptions import HTTPError, RequestException

from src.config import CHAT_COMPLETIONS_URL, HUGGINGFACE_KEY

logger = logging.getLogger(__name__)

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_KEY}",
    "Content-Type": "application/json",
}

_LOCAL_MODEL = None


def _get_local_model():
    """Lazy-load a local summarization model."""
    global _LOCAL_MODEL
    if _LOCAL_MODEL is None:
        try:
            from transformers import pipeline

            logger.info(
                "Loading local summarization model - facebook/bart-large-cnn ..."
            )
            _LOCAL_MODEL = pipeline("summarization", model="facebook/bart-large-cnn")
        except ImportError:
            logger.error("transformers is not installed. Local fallback unavailable.")
            _LOCAL_MODEL = None
    return _LOCAL_MODEL


def summarize_question(question):
    system_prompt = (
        "You are a support assistant who briefly summarizes the essence of a question "
        "while preserving its key meaning."
        "When rewriting, avoid first-person language —"
        "replace 'I' with 'the client' or a neutral third-person form. "
        "The result should be formal and concise."
    )

    user_prompt = (
        "Summarize and rephrase the following question formally,"
        f"avoiding first-person language:\n\n{question}"
    )

    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.5,
        "max_tokens": 128,
        "top_p": 0.9,
    }

    # try Hugging Face API
    try:
        response = requests.post("", headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except (HTTPError, RequestException, KeyError, IndexError, ValueError) as e:
        logger.warning("HF summarization failed: %s", e)

    # fallback to local model
    model = _get_local_model()
    if model is None:
        raise RuntimeError(
            "Summarization service unavailable and local model not installed."
        )

    try:
        result = model(question, max_length=60, min_length=10, do_sample=False)
        return result[0]["summary_text"]
    except Exception as local_error:
        logger.error("Local summarization model failed: %s", local_error)
        raise RuntimeError("Summarization service unavailable")
