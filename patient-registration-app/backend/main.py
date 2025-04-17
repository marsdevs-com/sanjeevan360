"""
Patient Registration API - Main Application Entry Point

This module initializes the FastAPI application, configures middleware,
registers routers, and sets up database connections. It serves as the
main entry point for the Patient Registration API.

The API provides endpoints for registering and retrieving patient information,
with data stored in both PostgreSQL (for relational data) and MongoDB
(for document-based storage).
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.routes.patient_routes import router as patient_router
from app.database.postgres_db import init_postgres
from app.database.mongo_db import init_mongodb

# Initialize FastAPI application with metadata
app = FastAPI(
    title="Patient Registration API",
    description="API for registering and managing patient information",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(patient_router, prefix="/api", tags=["patients"])

@app.on_event("startup")
async def startup_db_client():
    """
    Initialize database connections when the application starts.
    This function is automatically called by FastAPI during startup.
    """
    # Initialize PostgreSQL connection
    await init_postgres()
    # Initialize MongoDB connection
    await init_mongodb()

@app.get("/")
async def root():
    """
    Root endpoint to verify the API is running.

    Returns:
        dict: A simple message indicating the API is running
    """
    return {"message": "Patient Registration API is running"}

if __name__ == "__main__":
    # Run the application using Uvicorn server when executed directly
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
