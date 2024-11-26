from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging

# Setup logging
logger = setup_logging()

# Create FastAPI app
app = FastAPI(
    title="AudioV4 API",
    description="AI-powered audiobook generation platform",
    version="4.0.0",
    debug=settings.DEBUG
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Import and include routers when created
# from app.api.routes import templates, questionnaires, outlines, audiobooks
# app.include_router(templates.router, prefix="/api/templates", tags=["templates"])

@app.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {"status": "healthy"}
