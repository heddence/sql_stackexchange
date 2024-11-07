from fastapi import APIRouter, HTTPException, Path, Query
from typing import List
import psycopg2.extras
import logging

from app.db.session import get_db_connection, release_db_connection
from app.schemas.tags import CommentsPosLim
from app.services.tags_comments_count import get_tags_comments_count_service
from app.services.tags_comments_pos_lim import get_tags_comments_pos_lim_service

router = APIRouter(
    prefix="/v2",
    tags=["Tags"]
)

# Initialize a logger for this module
logger = logging.getLogger("app.api.tags_comments_pos_lim")

@router.get("/tags/{tag_name}/comments/{position}", response_model=List[CommentsPosLim])
def get_tags_comments_pos_lim(
        tag_name: str = Path(..., description="The name of the tag"),
        position: int = Path(..., description="Position of the comment"),
        limit: int = Query(1, ge=1, le=100, description="Number of comments"),
):
    """
    Retrieve the comment at a specific position within posts that are tagged with a given tag.

    Comments from posts associated with a specific tag, where each comment is at
    a specified position in the sequence of comments for its post.

    Args:
        tag_name (str): The name of the tag to analyze.
        position (int): The position of the comment.
        limit (int): The maximum number of comments to return.

    Returns:
        List[CommentsPosLim]: A list of CommentsPosLim objects representing comments.

    Raises:
        HTTPException:
            - 404: If no comments are found for the specified tag.
            - 500: If an internal server error occurs.
    """
    logger.info(f"Fetching comments for tag: {tag_name} at the position {position}.")
    connection = get_db_connection()
    try:
        # Fetch tag statistics using the service
        comments = get_tags_comments_pos_lim_service(connection, tag_name, position, limit)
        if not comments:
            logger.warning(f"No comments with tag: {tag_name} at the position {position}.")
            raise HTTPException(status_code=404, detail="No comments found for the specified tag.")
        logger.info(f"Retrieved comments with tag: {tag_name} at the position {position}.")
        return comments

    except psycopg2.Error as e:
        # Log the database error and raise a 500 Internal Server Error
        logger.error(f"Database error while fetching comments with tag '{tag_name}': {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    except FileNotFoundError as e:
        # Log the file not found error and raise a 500 Internal Server Error
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        # Ensure the connection is released back to the pool
        release_db_connection(connection)
