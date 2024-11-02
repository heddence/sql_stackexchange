from fastapi import APIRouter, HTTPException, Path
from typing import List
import psycopg2.extras
import logging

from app.db.session import get_db_connection, release_db_connection
from app.schemas.users import Friends
from app.services.users_friends import get_users_friends_service

# Initialize the APIRouter with a prefix and tags
router = APIRouter(
    prefix="/v2",
    tags=["Users"]
)

# Initialize a logger for this module
logger = logging.getLogger("app.api.users_friends")

@router.get("/users/{user_id}/friends", response_model=List[Friends])
def get_user_friends(
    user_id: int = Path(..., ge=1, description="The ID of the user"),
):
    """
    Retrieve a paginated list of friends for a specific user.

    Friends are defined as users who have commented on posts that the specified user has created or commented on.
    The list is sorted by the friends' most recent comment dates in descending order.

    Args:
        user_id (int): The unique identifier of the user for whom to retrieve friends.

    Returns:
        List[Friend]: A list of Friend schemas representing the friends.

    Raises:
        HTTPException:
            - 404: If no friends are found for the specified user.
            - 500: If an internal server error occurs during the process.
    """
    logger.info(f"Fetching friends for user ID: {user_id}.")
    connection = get_db_connection()
    try:
        # Execute the service function to get friends
        friends = get_users_friends_service(connection, user_id)
        if not friends:
            logger.warning(f"No friends found for user ID: {user_id}")
            raise HTTPException(status_code=404, detail="No friends found for the specified user.")
        logger.info(f"Retrieved {len(friends)} friends for user ID: {user_id}")
        return friends

    except psycopg2.Error as e:
        # Log the database error and raise a 500 Internal Server Error
        logger.error(f"Database error while fetching friends for user ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    except FileNotFoundError as e:
        # Log the file not found error and raise a 500 Internal Server Error
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        # Ensure the connection is released back to the pool
        release_db_connection(connection)
