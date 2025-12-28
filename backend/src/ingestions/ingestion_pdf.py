import logging
import re
from typing import BinaryIO

import fitz

logger = logging.getLogger(__name__)


def load_pdf(file: BinaryIO, filename: str) -> list[dict]:
    doc = fitz.open(stream=file.read(), filetype="pdf")

    all_text = "\n".join([page.get_text() for page in doc])

    cleaned = re.sub(r"\n{2,}", "\n", all_text).strip()

    chunks = re.split(r"\n?\s*\d+\.\s*", cleaned)
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

    logger.info("Parsed %d chunks from PDF: %s", len(chunks), filename)
    return [
        {
            "text": chunk,
            "source": filename,
        }
        for chunk in chunks
    ]
