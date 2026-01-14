import logging
from typing import BinaryIO

import docx

from .custom_ingestion_error import EmptyFileError, FileParsingError

logger = logging.getLogger(__name__)


def load_docx(file: BinaryIO, filename: str) -> list[dict[str, str]]:
    """
    Loads a DOCX file and converts it to a list of dictionaries for text processing.

    Args:
        file: Binary stream of DOCX file
        filename: Source filename, preserved in 'source' field

    Returns:
        List of dictionaries where each element contains:
            - 'text': paragraphs of text
            - 'source': Source filename
    """
    try:
        doc = docx.Document(file)
    except Exception as e:
        logger.exception("Unexpected error parsing DOCX %s", filename)
        raise FileParsingError(f"Could not load DOCX file {filename}: {e}")

    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

    if not paragraphs:
        logger.warning("DOCX %s is empty", filename)
        raise EmptyFileError(f"Empty DOCX document {filename}")

    logger.info("Parsed %d paragraphs from DOCX: %s", len(paragraphs), filename)

    return [
        {
            "text": paragraph,
            "source": filename,
        }
        for paragraph in paragraphs
    ]
