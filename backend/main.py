import os
import secrets
from typing import Literal

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

load_dotenv()

API_KEY = os.getenv("API_KEY", "poke-tower-dev-key")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

app = FastAPI(
    title="Poké Tower AI API",
    description="API simples que recebe o contexto tático do jogo e consulta um modelo local Ollama.",
    version="1.0.0",
)

# Para a entrega local. Restrinja os origins se publicar o projeto.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key"],
)


class AnalysisRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=8000)
    model: str = Field(default=DEFAULT_MODEL, min_length=1, max_length=100)


class AnalysisResponse(BaseModel):
    response: str
    model: str
    provider: Literal["ollama"] = "ollama"


def check_api_key(x_api_key: str | None) -> None:
    if not x_api_key or not secrets.compare_digest(x_api_key, API_KEY):
        raise HTTPException(status_code=401, detail="API key ausente ou inválida")


@app.get("/")
def root():
    return {"message": "Poké Tower AI API", "docs": "/docs", "health": "/health"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze(payload: AnalysisRequest, x_api_key: str | None = Header(default=None)):
    check_api_key(x_api_key)
    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            ollama_response = await client.post(
                OLLAMA_URL,
                json={
                    "model": payload.model or DEFAULT_MODEL,
                    "prompt": payload.prompt,
                    "stream": False,
                    "options": {"temperature": 0.1},
                },
            )
            ollama_response.raise_for_status()
            data = ollama_response.json()
    except httpx.ConnectError as exc:
        raise HTTPException(
            status_code=503,
            detail="Não foi possível conectar ao Ollama. Verifique se ele está iniciado e se o modelo foi baixado.",
        ) from exc
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail="O Ollama demorou demais para responder.") from exc
    except (httpx.HTTPStatusError, ValueError) as exc:
        raise HTTPException(status_code=502, detail="O Ollama retornou uma resposta inválida.") from exc

    answer = (data.get("response") or "").strip()
    if not answer:
        raise HTTPException(status_code=502, detail="O Ollama retornou uma resposta vazia.")
    return AnalysisResponse(response=answer, model=payload.model or DEFAULT_MODEL)
