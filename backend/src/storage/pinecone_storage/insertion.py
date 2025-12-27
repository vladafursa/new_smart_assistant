import os

from pinecone import AwsRegion, CloudProvider, Pinecone, ServerlessSpec

from src.config import DIMENSION, INDEX_NAME, PINECONE_KEY
from src.ingestions import parse_file

from .preparation import prepare_chunks_for_indexing, split_texts

pc = Pinecone(api_key=PINECONE_KEY)


def init_index():
    if INDEX_NAME not in [idx["name"] for idx in pc.list_indexes()]:
        pc.create_index(
            name=INDEX_NAME,
            dimension=DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud=CloudProvider.AWS, region=AwsRegion.US_EAST_1),
        )
    return pc.Index(INDEX_NAME)


def upsert_vectors(index, namespace, vectors):
    index.upsert(vectors=vectors, namespace=namespace)


def process_all_files(data_dir, index, namespace):
    for filename in os.listdir(data_dir):
        path = os.path.join(data_dir, filename)

        if filename.startswith(".") or not os.path.isfile(path):
            continue

        try:
            print(f"\n Processing file: {filename}")
            texts = parse_file(path)
            chunks = split_texts(texts)
            vectors = prepare_chunks_for_indexing(chunks, index)
            upsert_vectors(index, namespace, vectors)
            print(f"Uploaded {len(vectors)} new vectors from {filename}")
        except Exception as e:
            print(f"Error while processing {filename}: {e}")
