from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

from agent.controller import process_query

app = FastAPI(title="LeetCode Agent API")

# Allow CORS for the browser extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows extension requests from chrome-extension:// environments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Server Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"type": "error", "content": f"Internal Server Error: {str(exc)}"}
    )

@app.get("/")
def read_root():
    return {"status": "online", "service": "LeetCode Agent Backend"}

class AskRequest(BaseModel):
    problem_title: str
    problem_description: str
    user_query: str
    history: List[Dict[str, str]] = []

@app.post("/ask")
def ask_agent(request: AskRequest):
    response = process_query(
        problem_title=request.problem_title,
        problem_description=request.problem_description,
        user_query=request.user_query,
        history=request.history
    )
    return response

@app.get("/health")
def health_check():
    return {"status": "healthy"}
