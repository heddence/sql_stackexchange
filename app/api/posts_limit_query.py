from fastapi import APIRouter, HTTPException, Query
from typing import List
import psycopg2.extras
import logging

from app.db.session import get_db_connection, release_db_connection
from app.schemas.posts import LimitQuery
from app.services.posts_limit_query import get_posts_limit_query_service


router = APIRouter(
    prefix="/v2",
    tags=["Posts"]
)

# Initialize a logger for this module
logger = logging.getLogger("app.api.posts")


@router.get("/posts/q2/", response_model=List[LimitQuery])
def get_posts(
    limit: int = Query(10, ge=1, le=100, description="Number of posts to return"),
    query: str = Query("", description="Search query for filtering posts by title or body")
):
    """
    Retrieve a list of posts ordered from newest to oldest, including associated tags.

    Args:
        limit (int): Number of posts to return (1-100).
        query (str): Search query to filter posts by title or body.

    Returns:
        List[PostWithTags]: A list of posts with associated tags matching the criteria.

    Raises:
        HTTPException:
            - 404: If no posts match the criteria.
            - 500: If an internal server error occurs.
    """
    logger.info(f"Fetching {limit} most recent posts with query '{query}'")
    connection = get_db_connection()
    try:
        # Fetch posts with tags using the service function
        posts = get_posts_limit_query_service(connection, query, limit)
        if not posts:
            logger.warning(f"No posts found matching query '{query}' with limit {limit}")
            raise HTTPException(status_code=404, detail="No posts found matching the criteria.")
        logger.info(f"Retrieved {len(posts)} posts")
        return posts

    except psycopg2.Error as e:
        # Log the database error and raise a 500 Internal Server Error
        logger.error(f"Database error while fetching posts: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    except FileNotFoundError as e:
        # Log the file not found error and raise a 500 Internal Server Error
        logger.error(f"SQL query file not found: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        # Ensure the connection is released back to the pool
        release_db_connection(connection)
