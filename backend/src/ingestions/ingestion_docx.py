import logging

import docx

logger = logging.getLogger(__name__)


def load_docx(path: str) -> list[dict]:
    doc = docx.Document(path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    logger.info(f"Parsed {len(paragraphs)} paragraphs from DOCX: {path}")
    return [
        {
            "text": paragraph,
            "source": path.split("/")[-1],
        }
        for paragraph in paragraphs
    ]
