from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router

# Initialize the server
app = FastAPI(
    title="CV Analyzer API",
    description="AI-powered CV analysis engine for Phase 1/2 handoff.",
    version="1.0.0"
)

# Configure CORS so Team 2's frontend (React/Next.js) can talk to us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to the frontend's actual URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach our routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    """Simple endpoint to verify the server is running."""
    return {"status": "ok", "message": "CV Analyzer API is running."}