import logging
from typing import BinaryIO

import docx

logger = logging.getLogger(__name__)


def load_docx(file: BinaryIO, filename: str) -> list[dict]:
    doc = docx.Document(file)

    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

    logger.info("Parsed %d paragraphs from DOCX: %s", len(paragraphs), filename)

    return [
        {
            "text": paragraph,
            "source": filename,
        }
        for paragraph in paragraphs
    ]
