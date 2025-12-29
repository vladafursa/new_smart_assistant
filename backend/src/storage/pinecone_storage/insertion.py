import io
import logging
import os

from pinecone import AwsRegion, CloudProvider, Pinecone, ServerlessSpec

from src.config import settings
from src.ingestions import parse_file

from .preparation import prepare_chunks_for_indexing, split_texts

logger = logging.getLogger(__name__)
pc = Pinecone(api_key=settings.PINECONE_KEY)


def init_index():
    if settings.INDEX_NAME not in [idx["name"] for idx in pc.list_indexes()]:
        pc.create_index(
            name=settings.INDEX_NAME,
            dimension=settings.DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud=CloudProvider.AWS, region=AwsRegion.US_EAST_1),
        )
    return pc.Index(settings.INDEX_NAME)


def upsert_vectors(index, namespace, vectors):
    index.upsert(vectors=vectors, namespace=namespace)


def process_file(filename: str, content: bytes, index, namespace):
    try:
        texts = parse_file(filename, content)
        chunks = split_texts(texts)
        vectors = prepare_chunks_for_indexing(chunks, index)
        upsert_vectors(index, namespace, vectors)
        logger.info("Upserting %d vectors into %s", len(vectors), namespace)
    except Exception as e:
        logger.error("Error while processing: %s", e)
