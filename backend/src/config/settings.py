import os

from dotenv import load_dotenv

load_dotenv()

# constants
# str
BUCKET_NAME = "files"
INDEX_NAME = "smart_support"
SUPABASE_TABLE = "documents"
# int
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# keys
HUGGINGFACE_KEY = os.getenv("HUGGINGFACE_KEY")
LLM_KEY = os.getenv("LLM_KEY")
PINECONE_KEY = os.getenv("PINECONE_KEY")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
