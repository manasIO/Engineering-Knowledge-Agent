from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.rag import answer_question

app = FastAPI(
    title="Engineering Knowledge Agent API", 
    version="0.1.0"
)

class AskRequest(BaseModel):
    question: str = Field(min_length=1)

class Source(BaseModel):
    id: int
    source: str
    section: str
    distance: float

class AskResponse(BaseModel):
    answer: str
    sources: list[Source]
    latency_ms:float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    try:   
        return answer_question(request.question)
    
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate answer"
        ) from exc