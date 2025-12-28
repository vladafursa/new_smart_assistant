import io
import logging
from pathlib import Path

from .custom_ingestion_error import FileParsingError, UnsupportedFileTypeError
from .ingestion_csv import load_csv
from .ingestion_docx import load_docx
from .ingestion_pdf import load_pdf

logger = logging.getLogger(__name__)

LOADERS = {
    ".csv": load_csv,
    ".pdf": load_pdf,
    ".docx": load_docx,
}


def parse_file(filename: str, content: bytes) -> list[dict]:
    ext = Path(filename).suffix.lower()
    file = io.BytesIO(content)

    if ext not in LOADERS:
        raise UnsupportedFileTypeError(f"Unsupported file type: {ext}")
    loader = LOADERS[ext]

    try:
        return loader(file, filename)
    except Exception as e:
        logger.exception("Failed to parse file %s", filename)
        raise FileParsingError(f"Failed to parse file {filename}") from e
