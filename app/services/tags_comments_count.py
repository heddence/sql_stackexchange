from typing import List
import psycopg2.extras
import logging

from app.schemas.tags import CommentsCount
from app.utils.sql import load_sql_query

# Initialize a logger for this module
logger = logging.getLogger("app.services.tags_stats")


def get_tags_comments_count_service(connection, tag_name: str, comments_count: int) -> List[CommentsCount]:
    """
    Business logic to retrieve the response time statistics between comments on a specific post.

    Args:
        connection: The database connection object.
        tag_name (str): The name of the tag to analyze.
        comments_count (int): The number of comments to retrieve for each post.

    Returns:
        List[CommentsCount]: A list of CommentsCount objects representing time statistics.
    """
    try:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Load the SQL query
        sql_query = load_sql_query("get_tags_comments_count.sql")
        logger.debug(f"Loaded SQL Query: {sql_query}")

        # Execute the query with the provided tag name
        logger.debug(f"Executing query for tag name: {tag_name} with comments count: {comments_count}")
        cursor.execute(sql_query, {"tagname": tag_name, "comments_count": comments_count})
        rows = cursor.fetchall()

        logger.debug(f"Fetched {len(rows)} rows from the database")

        # Convert each row into a TagStats schema
        comments_stats = [CommentsCount(**dict(row)) for row in rows]
        return comments_stats

    except Exception as e:
        logger.error(f"Error in get_tags_comments_count service: {e}")
        raise

    finally:
        cursor.close()
