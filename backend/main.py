"""FastAPI main application for engagement message generator."""

import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

from backend.services.message_generator import EngagementMessageGenerator

# Load environment variables
load_dotenv()

app = FastAPI(title="Engagement Message Generator API")

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize message generator
try:
    generator = EngagementMessageGenerator()
except ValueError as e:
    generator = None
    print(f"Warning: Message generator not initialized: {e}")


# Request/Response models
class GenerateRequest(BaseModel):
    theme: str = "random"


class GenerateResponse(BaseModel):
    content: str
    theme_used: str


class ErrorResponse(BaseModel):
    error: str


# Health check endpoint (before static files mount)
@app.get("/health")
async def health():
    """Health check endpoint for Fly.io."""
    return {"status": "healthy"}


# Generate endpoint
@app.post("/api/generate", response_model=GenerateResponse)
async def generate_message(request: GenerateRequest):
    """Generate an engagement message with the specified theme."""
    if generator is None:
        raise HTTPException(
            status_code=500,
            detail="Message generator not initialized. Check CLAUDE_API_KEY environment variable.",
        )

    try:
        result = generator.generate_with_theme(request.theme)
        return GenerateResponse(
            content=result["content"], theme_used=result["theme_used"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Serve static files from Next.js build (for production)
# This must be last as it's a catch-all
static_dir = Path(__file__).parent.parent / "frontend" / "out"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
