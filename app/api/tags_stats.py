from fastapi import APIRouter, HTTPException, Path
from typing import List
import psycopg2.extras
import logging

from app.db.session import get_db_connection, release_db_connection
from app.schemas.tags import Stats
from app.services.tags_stats import get_tags_stats_service


router = APIRouter(
    prefix="/v2",
    tags=["Tags"]
)

# Initialize a logger for this module
logger = logging.getLogger("app.api.tags_stats")

@router.get("/tags/{tag_name}/stats", response_model=List[Stats])
def get_tag_stats(tag_name: str = Path(..., description="The name of the tag")):
    """
    Retrieve the percentage of posts with a particular tag for each day of the week.

    The percentage is calculated as the number of posts with the specified tag divided by the total number of posts
    published on each day of the week, presented on a scale of 0 - 100 and rounded to two decimal places.

    Args:
        tag_name (str): The name of the tag to analyze.

    Returns:
        List[Stats]: A list of TagStats objects representing each day of the week.

    Raises:
        HTTPException:
            - 404: If no statistics are found for the specified tag.
            - 500: If an internal server error occurs.
    """
    logger.info(f"Fetching tag statistics for tag: {tag_name}")
    connection = get_db_connection()
    try:
        # Fetch tag statistics using the service
        tag_stats = get_tags_stats_service(connection, tag_name)
        if not tag_stats:
            logger.warning(f"No statistics found for tag: {tag_name}")
            raise HTTPException(status_code=404, detail="No statistics found for the specified tag.")
        logger.info(f"Retrieved statistics for tag: {tag_name}")
        return tag_stats

    except psycopg2.Error as e:
        # Log the database error and raise a 500 Internal Server Error
        logger.error(f"Database error while fetching stats for tag '{tag_name}': {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    except FileNotFoundError as e:
        # Log the file not found error and raise a 500 Internal Server Error
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        # Ensure the connection is released back to the pool
        release_db_connection(connection)
