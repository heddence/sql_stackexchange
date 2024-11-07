from fastapi import APIRouter, HTTPException, Path
from typing import List
import psycopg2.extras
import logging

from app.db.session import get_db_connection, release_db_connection
from app.schemas.users import IdBadgeHistory
from app.services.users_id_badge_hist import get_users_id_badge_hist

# Initialize the APIRouter with a prefix and tags
router = APIRouter(
    prefix="/v2",
    tags=["Users"]
)

# Initialize a logger for this module
logger = logging.getLogger("app.api.users_id_badge_hist")

@router.get("/users/{user_id}/badge_history", response_model=List[IdBadgeHistory])
def get_users_friends(
    user_id: int = Path(..., ge=1, description="The ID of the user"),
):
    """
    Retrieve a paginated list of the badge history for the specific user with respective posts.

    Friends are defined as users who have commented on posts that the specified user has created or commented on.
    The list is sorted by the friends' most recent comment dates in descending order.

    Badge history for a user are defined as name of the badge and its id, and
    the associated post made before earning the badge, and the body of that post.

    Args:
        user_id (int): The unique identifier of the user for whom to retrieve badge history.

    Returns:
        List[IdBadgeHistory]: A list of IdBadgeHistory schemas representing the badge history.

    Raises:
        HTTPException:
            - 404: If no badge history are found for the specified user.
            - 500: If an internal server error occurs during the process.
    """
    logger.info(f"Fetching badge history for user ID: {user_id}.")
    connection = get_db_connection()
    try:
        # Execute the service function to get friends
        badge_hist = get_users_id_badge_hist(connection, user_id)
        if not badge_hist:
            logger.warning(f"No badge history found for user ID: {user_id}")
            raise HTTPException(status_code=404, detail="No badge history found for the specified user.")
        logger.info(f"Retrieved {len(badge_hist)} badges for user ID: {user_id}")
        return badge_hist

    except psycopg2.Error as e:
        # Log the database error and raise a 500 Internal Server Error
        logger.error(f"Database error while fetching badge history for user ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    except FileNotFoundError as e:
        # Log the file not found error and raise a 500 Internal Server Error
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        # Ensure the connection is released back to the pool
        release_db_connection(connection)
