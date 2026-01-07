from fastapi import APIRouter, Request

from src.apis.rag_models import QueryRequest, QueryResponse
from src.ml import generate_answer, query_index
from src.ml.classification import classify

rag = APIRouter(prefix="/rag", tags=["rag"])


@rag.post("/rag", response_model=QueryResponse)
def rag_endpoint(request: Request, body: QueryRequest):
    index = request.app.state.index
    category = classify(body.question)
    context_chunks = query_index(index, body.question, category)
    context_text = "\n\n".join([chunk["text"] for chunk in context_chunks])
    answer = generate_answer(context_text, body.question)
    return QueryResponse(answer=answer, chunks=context_chunks)
