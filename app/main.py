from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.api.middleware import error_handler

# Create FastAPI app
app = FastAPI(
    title="AudioV4",
    description="AI-powered audiobook generation platform",
    version="0.1.0"
)

# Register the error handling middleware as a proper middleware class
class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        return await error_handler(request, call_next)

app.add_middleware(ErrorHandlerMiddleware)

# Import and include routers here when created
# from app.api.routes import router as api_router
# app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy"}
