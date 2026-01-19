from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

from schemas import AnalysisRequest, AnalysisResult
import agent

app = FastAPI(
    title="Assumption Detector",
    description="Identifies hidden assumptions in text",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static/index.html"))


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisResult)
async def analyze_text(request: AnalysisRequest):
    result = await agent.analyze(request.text)
    return result
