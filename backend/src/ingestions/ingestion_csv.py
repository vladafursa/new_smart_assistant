import logging
from typing import BinaryIO

import pandas as pd

logger = logging.getLogger(__name__)


def load_csv(file: BinaryIO, filename: str) -> list[dict]:
    df = pd.read_csv(file)
    logger.info("Loaded %d rows from %s", len(df), filename)

    if df.empty:
        logger.warning("CSV %s is empty", filename)
        return []

    if {"Question", "Answer"}.issubset(df.columns):
        df["text"] = df["Question"].astype(str) + "\n" + df["Answer"].astype(str)
    else:
        df["text"] = df[df.columns[0]].astype(str)
    df["source"] = filename
    return df[["text", "source"]].to_dict(orient="records")
