import logging
from typing import BinaryIO, Optional

import pandas as pd

from src.config import settings

from .custom_ingestion_error import EmptyFileError, FileParsingError

logger = logging.getLogger(__name__)


def find_columns(
    df: pd.DataFrame,
    question_aliases=settings.QUESTION_ALIASES,
    answer_aliases=settings.ANSWER_ALIASES,
) -> tuple[Optional[str], Optional[str]]:
    """
    Finds the actual column names for Question/Answer based on aliases.

    Args:
        df (pandas.DataFrame): The DataFrame to search from.
        question_aliases (set[str]): Set of acceptable names for the question column.
        answer_aliases (set[str]): Set of acceptable names for the answer column.

    Returns:
        tuple[str | None, str | None]: A tuple containing the resolved
        (question_column_name, answer_column_name), or (None, None) if not found."""

    # Normalize column names for case/whitespace-insensitive matching
    normalized_columns = [col.strip().lower() for col in df.columns]

    question_column = next(
        (
            alias.capitalize()
            for alias in question_aliases
            if alias.lower() in normalized_columns
        ),
        None,
    )
    answer_column = next(
        (
            alias.capitalize()
            for alias in answer_aliases
            if alias.lower() in normalized_columns
        ),
        None,
    )
    return question_column, answer_column


def load_csv(file: BinaryIO, filename: str) -> list[dict[str, str]]:
    """
    Loads a CSV file and converts it to a list of dictionaries for text processing.

    Automatically detects CSV structure:
    - If 'Question' and 'Answer' columns exist, combines them with '\n'
    - Otherwise uses the first column as text content

    Args:
        file: Binary stream of CSV file
        filename: Source filename, preserved in 'source' field

    Returns:
        List of dictionaries where each element contains:
            - 'text': Combined text from CSV
            - 'source': Source filename
    """
    try:
        df = pd.read_csv(file)
    except pd.errors.ParserError as e:
        raise FileParsingError(f"Malformed CSV {filename}: {e}")
    except UnicodeDecodeError as e:
        raise FileParsingError(f"Encoding issue in {filename}: {e}")
    except Exception as e:
        logger.exception("Unexpected error parsing CSV %s", filename)
        raise FileParsingError(f"Could not load CSV file {filename}: {e}")

    if df.empty:
        logger.warning("CSV %s is empty", filename)
        raise EmptyFileError(f"CSV {filename} is empty")

    df = df.fillna("")

    question_column_name, answer_column_name = find_columns(df)

    # Combine Q/A into single text field
    if question_column_name and answer_column_name:
        df["text"] = (
            df[question_column_name].astype(str)
            + "\n"
            + df[answer_column_name].astype(str)
        )
    else:
        # Fallback: use first column, but log a warning for visibility
        first_column = df.columns[0]
        logger.warning(
            "No Q/A columns found in %s, using first column '%s' as text",
            filename,
            first_column,
        )
        df["text"] = df[first_column].astype(str)

    df["source"] = filename
    logger.info("Loaded %d rows from %s", len(df), filename)

    return df[["text", "source"]].to_dict(orient="records")
