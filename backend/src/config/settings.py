from dotenv import load_dotenv
import os

load_dotenv()
BUCKET_NAME = "files"
SUPABASE_TABLE = "documents"
PINECONE_KEY = os.getenv("PINECONE_KEY")
HUGGINGFACE_KEY = os.getenv("HUGGINGFACE_KEY")
LLM_KEY = os.getenv("LLM_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

INDEX_NAME = "smart_support"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
