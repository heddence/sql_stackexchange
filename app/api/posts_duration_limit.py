from fastapi import APIRouter, HTTPException, Query
from typing import List
import psycopg2.extras
import logging

from app.db.session import get_db_connection, release_db_connection
from app.schemas.posts import DurationLimit
from app.services.posts_duration_limit import get_posts_duration_limit_service


router = APIRouter(
    prefix="/v2",
    tags=["Posts"]
)

# Initialize a logger for this module
logger = logging.getLogger("app.api.posts")


@router.get("/posts/q1/", response_model=List[DurationLimit])
def get_posts_duration_limit(
    duration: float = Query(..., ge=0.0, description="Maximum duration in minutes a post was open"),
    limit: int = Query(..., ge=1, le=100, description="Number of posts to return")
):
    """
    Retrieve a list of the most recently resolved posts that were open for a maximum duration.

    The duration is calculated as the number of minutes between creation_date and closed_date.
    The results are limited by the specified number of posts and sorted by the most recently closed.

    Args:
        duration (float): Maximum duration in minutes a post was open.
        limit (int): Number of posts to return.

    Returns:
        List[DurationLimit]: A list of recently resolved posts matching the criteria.

    Raises:
        HTTPException:
            - 404: If no posts match the criteria.
            - 500: If an internal server error occurs.
    """
    logger.info(f"Fetching {limit} most recently resolved posts with duration <= {duration} minutes")
    connection = get_db_connection()
    try:
        # Fetch recent resolved posts using the service
        recent_posts = get_posts_duration_limit_service(connection, duration, limit)
        if not recent_posts:
            logger.warning(f"No resolved posts found with duration <= {duration} minutes")
            raise HTTPException(status_code=404, detail="No resolved posts found matching the criteria.")
        logger.info(f"Retrieved {len(recent_posts)} posts")
        return recent_posts

    except psycopg2.Error as e:
        # Log the database error and raise a 500 Internal Server Error
        logger.error(f"Database error while fetching recent resolved posts: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    except FileNotFoundError as e:
        # Log the file not found error and raise a 500 Internal Server Error
        logger.error(f"SQL query file not found: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        # Ensure the connection is released back to the pool
        release_db_connection(connection)
