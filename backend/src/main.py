import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.apis.rag_api import rag
from src.apis.storage_api import storage
from src.config import settings
from src.storage import init_index

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
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

# FastAPI app setup
app = FastAPI()


# Startup event for index initialization
@app.on_event("startup")
async def startup_event():
    app.state.index = init_index()
    logging.info("Index initialized successfully.")


# Routers
app.include_router(storage)
app.include_router(rag)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
