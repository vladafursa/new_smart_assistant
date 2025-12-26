import hashlib

from langchain_text_splitters import RecursiveCharacterTextSplitter
from tqdm import tqdm

from src.config import CHUNK_OVERLAP, CHUNK_SIZE
from src.ml import extract_entities, get_embeddings


def split_texts(text_records):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = []
    for i, record in enumerate(text_records):
        text = record["text"]
        source = record["source"]
        for chunk_idx, chunk in enumerate(splitter.split_text(text)):
            entities_raw = extract_entities(chunk)
            chunks.append(
                {
                    "text": chunk,
                    "metadata": {
                        "source_index": i,
                        "chunk_index": chunk_idx,
                        "source": source,
                        "entities": entities_raw,
                    },
                }
            )
    return chunks


def hash_text(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def prepare_chunks_for_indexing(chunks, index):
    vectors = []

    chunk_ids = [hash_text(chunk["text"]) for chunk in chunks]
    existing = index.fetch(ids=chunk_ids)
    existing_ids = set(existing.vectors.keys())

    for chunk in tqdm(chunks):
        chunk_id = hash_text(chunk["text"])
        if chunk_id in existing_ids:
            continue

        emb = get_embeddings([chunk["text"]])[0]
        vectors.append(
            {
                "id": chunk_id,
                "values": emb,
                "metadata": {**chunk["metadata"], "text": chunk["text"]},
            }
        )

    return vectors
