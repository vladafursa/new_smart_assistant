from .ingestion_csv import load_csv
from .ingestion_docx import load_docx
from .ingestion_pdf import load_pdf


def parse_file(path: str) -> list[str]:
    if path.endswith(".csv"):
        return load_csv(path)
    elif path.endswith(".pdf"):
        return load_pdf(path)
    elif path.endswith(".docx"):
        return load_docx(path)
    else:
        raise ValueError(f"Unsupported file type: {path}")
