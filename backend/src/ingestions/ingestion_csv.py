import pandas as pd


def load_csv(path: str) -> list[dict]:
    df = pd.read_csv(path)
    print(f"Loaded {len(df)} rows from {path}")
    if {"Question", "Answer"}.issubset(df.columns):
        df["text"] = df["Question"].astype(str) + "\n" + df["Answer"].astype(str)
    else:
        df["text"] = df[df.columns[0]].astype(str)
    df["source"] = path.split("/")[-1]
    return df[["text", "source"]].to_dict(orient="records")
