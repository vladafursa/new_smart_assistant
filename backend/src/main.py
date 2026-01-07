import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.apis.rag_api import rag
from src.apis.storage_api import storage
from src.storage import init_index

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)

NOISY_LIBS = [
    "httpx",
    "httpcore",
    "hpack",
    "urllib3",
    "asyncio",
    "uvicorn.error",
    "uvicorn.access",
]

for lib in NOISY_LIBS:
    logging.getLogger(lib).setLevel(logging.WARNING)


app = FastAPI()
app.state.index = init_index()
app.include_router(storage)
app.include_router(rag)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
