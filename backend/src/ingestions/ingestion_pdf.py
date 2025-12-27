import logging
import re

import fitz

logger = logging.getLogger(__name__)


def load_pdf(path: str) -> list[dict]:
    doc = fitz.open(path)
    all_text = "\n".join([page.get_text() for page in doc])

    cleaned = re.sub(r"\n{2,}", "\n", all_text).strip()

    chunks = re.split(r"\n?\s*\d+\.\s*", cleaned)
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

    logger.info(f" Parsed {len(chunks)} chunks from PDF: {path}")
    return [
        {
            "text": chunk,
            "source": path.split("/")[-1],
        }
        for chunk in chunks
    ]
