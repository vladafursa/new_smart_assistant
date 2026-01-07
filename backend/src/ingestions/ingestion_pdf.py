import logging
import re
from typing import BinaryIO

import fitz

from .custom_ingestion_error import EmptyFileError, FileParsingError

logger = logging.getLogger(__name__)


def load_pdf(file: BinaryIO, filename: str) -> list[dict[str, str]]:
    """
    Loads a PDF file and converts it to a list of dictionaries for text processing.

    Args:
        file: Binary stream of PDF file
        filename: Source filename, preserved in 'source' field

    Returns:
        List of dictionaries where each element contains:
            - 'text': chunks of text
            - 'source': Source filename
    """
    try:
        # Attempt to open PDF
        doc = fitz.open(stream=file.read(), filetype="pdf")
    except Exception as e:
        logger.exception("Unexpected error parsing PDF %s", filename)
        raise FileParsingError(f"Could not load PDF file {filename}: {e}")
    try:
        all_text = "\n".join([page.get_text() for page in doc])

        cleaned = re.sub(r"\n{2,}", "\n", all_text).strip()
        if not cleaned:
            logger.warning("PDF %s is empty", filename)
            raise EmptyFileError(f"Empty PDF document {filename}")

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
    except Exception as e:
        logger.exception("Error processing text from PDF %s", filename)
        raise FileParsingError(f"Could not process PDF file {filename}: {e}")
