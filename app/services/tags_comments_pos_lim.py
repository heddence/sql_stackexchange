from typing import List
import psycopg2.extras
import logging

from app.schemas.tags import CommentsPosLim, CommentsCount
from app.utils.sql import load_sql_query

# Initialize a logger for this module
logger = logging.getLogger("app.services.tags_comments_pos_lim")


def get_tags_comments_pos_lim_service(connection, tag_name: str, position: int, limit: int) -> List[CommentsPosLim]:
    """
    Business logic to retrieve a comment at a specific position within posts that are tagged with a given tag.

    Args:
        connection: The database connection object.
        tag_name (str): The name of the tag to analyze.
        position (int): The position of the comment in the post.
        limit (int): The maximum number of comments to return.

    Returns:
        List[CommentsPosLim]: A list of CommentsPosLim objects representing comments at a given position.
    """
    try:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Load the SQL query
        sql_query = load_sql_query("get_tags_comments_pos_lim.sql")
        logger.debug(f"Loaded SQL Query: {sql_query}")

        # Execute the query with the provided tag name
        logger.debug(f"Executing query for tag name: {tag_name} with comment's position: {position}")
        cursor.execute(sql_query, {"tagname": tag_name, "position": position, "limit": limit})
        rows = cursor.fetchall()

        logger.debug(f"Fetched {len(rows)} rows from the database")

        # Convert each row into a TagStats schema
        comments_stats = [CommentsPosLim(**dict(row)) for row in rows]
        return comments_stats

    except Exception as e:
        logger.error(f"Error in get_comments_pos_lim service: {e}")
        raise

    finally:
        cursor.close()
