from fastapi import APIRouter, HTTPException, Path, Query
from typing import List
import psycopg2.extras
import logging

from app.db.session import get_db_connection, release_db_connection
from app.schemas.posts import IdLimit
from app.services.posts_id_limit import get_posts_id_limit_service


router = APIRouter(
    prefix="/v2",
    tags=["Posts"]
)

# Initialize a logger for this module
logger = logging.getLogger("app.api.posts")


@router.get("/posts/{post_id}", response_model=List[IdLimit])
def get_posts(
        post_id: int = Path(..., description="Starting thread post id"),
        limit: int = Query(1, ge=1, le=100, description="Number of posts to return"),
):
    """
    Retrieve a post within a thread, starting from a specific post and including all its descendant posts.

    The details of each post in the thread, including its hierarchical level for reconstructing the thread structure.

    Args:
        post_id (int): The post id starting the thread.
        limit (int): Maximum number of posts to return.

    Returns:
        List[IdLimit]: A thread of posts.

    Raises:
        HTTPException:
            - 404: If no thread exists.
            - 500: If an internal server error occurs.
    """
    logger.info(f"Fetching post with {post_id}")
    connection = get_db_connection()
    try:
        # Fetch posts with tags using the service function
        posts = get_posts_id_limit_service(connection, post_id, limit)
        if not posts:
            logger.warning(f"No thread found matching starting post id '{post_id}'.")
            raise HTTPException(status_code=404, detail="No thread found.")
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
