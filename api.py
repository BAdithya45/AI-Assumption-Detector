from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from schemas import AnalysisRequest, AnalysisResult
import agent

basedir = os.path.dirname(os.path.abspath(__file__))

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

app.mount("/static", StaticFiles(directory=os.path.join(basedir, "static")), name="static")


@app.get("/")
async def root():
    return FileResponse(os.path.join(basedir, "static/index.html"))


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisResult)
async def analyze_text(request: AnalysisRequest):
    result = await agent.analyze(request.text)
    return result
