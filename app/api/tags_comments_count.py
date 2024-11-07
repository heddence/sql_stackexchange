from fastapi import APIRouter, HTTPException, Path, Query
from typing import List
import psycopg2.extras
import logging

from app.db.session import get_db_connection, release_db_connection
from app.schemas.tags import CommentsCount
from app.services.tags_comments_count import get_tags_comments_count_service


router = APIRouter(
    prefix="/v2",
    tags=["Tags"]
)

# Initialize a logger for this module
logger = logging.getLogger("app.api.tags_comments_count")

@router.get("/tags/{tag_name}/comments/", response_model=List[CommentsCount])
def get_tags_stats(
        tag_name: str = Path(..., description="The name of the tag"),
        comments_count: int = Query(1, ge=1, le=100, description="Number of posts to return"),
):
    """
    Retrieve the response time statistics between comments on a specific post.

    Statistics include sequential comments made on a post, the time differences between
    consecutive comments, and the cumulative average response time as more
    comments are added.

    Args:
        tag_name (str): The name of the tag to analyze.
        comments_count (int): The number of posts to return.

    Returns:
        List[CommentsCount]: A list of TagStats objects representing each day of the week.

    Raises:
        HTTPException:
            - 404: If no statistics are found for the specified tag.
            - 500: If an internal server error occurs.
    """
    logger.info(f"Fetching post comments' statistics for tag: {tag_name} with more than {comments_count} comments.")
    connection = get_db_connection()
    try:
        # Fetch tag statistics using the service
        tag_stats = get_tags_comments_count_service(connection, tag_name, comments_count)
        if not tag_stats:
            logger.warning(f"No statistics found for the post with tag: {tag_name}"
                           f" with more than {comments_count} comments.")
            raise HTTPException(status_code=404, detail="No statistics found for the specified tag.")
        logger.info(f"Retrieved statistics for the post with tag: {tag_name}"
                    f" with more than {comments_count} comments.")
        return tag_stats

    except psycopg2.Error as e:
        # Log the database error and raise a 500 Internal Server Error
        logger.error(f"Database error while fetching stats for the post with tag '{tag_name}': {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    except FileNotFoundError as e:
        # Log the file not found error and raise a 500 Internal Server Error
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        # Ensure the connection is released back to the pool
        release_db_connection(connection)
