from fastapi import FastAPI
import logging

# Import routers
from app.api import (
    posts_users, users_friends, tags_stats
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more detailed logs during development
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Initialize the FastAPI application
app = FastAPI(
    title="Stack Exchange API",
    description="API for accessing Stack Exchange Superuser data",
    version="1.0.0",
)

# Include routers from different modules
app.include_router(posts_users.router)
app.include_router(users_friends.router)
app.include_router(tags_stats.router)

# Root endpoint for basic health check
@app.get("/", tags=["Health"])
def read_root():
    """
    Root endpoint to verify that the API is running.
    """
    return {"message": "Welcome to the Stack Exchange Superuser API!"}
