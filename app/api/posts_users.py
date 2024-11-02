from fastapi import APIRouter, HTTPException, Path
from typing import List
import psycopg2.extras
import logging

from app.db.session import get_db_connection, release_db_connection
from app.schemas.posts import Users
from app.services.posts_users import get_posts_users_service


router = APIRouter(
    prefix="/v2",
    tags=["Posts"]
)

# Initialize a logger for this module
logger = logging.getLogger("app.api.posts_users")


@router.get("/posts/{post_id}/users", response_model=List[Users])
def get_discussants(post_id: int = Path(..., ge=1, description="The ID of the post")):
    """
    Retrieve a list of all discussants (users who have commented) on a specific post.

    The users are sorted by the time of their most recent comment on the post,
    starting with the newest and ending with the oldest.

    Args:
        post_id (int): The unique identifier of the post.

    Returns:
        List[Users]: A list of Users schemas representing the users.

    Raises:
        HTTPException:
            - 404 if the post does not exist or has no comments.
            - 500 if an internal server error occurs.
    """
    logger.info(f"Fetching friends for user ID: {post_id}.")
    connection = get_db_connection()
    try:
        # Execute the service function to get friends
        posts = get_posts_users_service(connection, post_id)
        if not posts:
            logger.warning(f"No users found for post ID: {post_id}")
            raise HTTPException(status_code=404, detail="No users found for post ID.")
        logger.info(f"Retrieved {len(posts)} users for post ID: {post_id}")
        return posts

    except psycopg2.Error as e:
        # Log the database error and raise a 500 Internal Server Error
        logger.error(f"Database error while fetching users for post ID {post_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    except FileNotFoundError as e:
        # Log the file not found error and raise a 500 Internal Server Error
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        # Ensure the connection is released back to the pool
        release_db_connection(connection)
