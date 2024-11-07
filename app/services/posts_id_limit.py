from typing import List
import psycopg2.extras
import logging

from app.schemas.posts import IdLimit
from app.utils.sql import load_sql_query

# Initialize a logger for this module
logger = logging.getLogger("app.services.posts_id_limit")


def get_posts_id_limit_service(connection, post_id: int, limit: int) -> List[IdLimit]:
    """
    Business logic to retrieve a post within a thread, starting from a specific post
    and including all its descendant posts.

    Args:
        connection: The database connection object.
        post_id (str): The id of the post.
        limit (int): The maximum number of posts to return.

    Returns:
        List[IdLimit]: A list of thread of posts.
    """
    try:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Load the SQL query
        sql_query = load_sql_query("get_posts_id_limit.sql")
        logger.debug(f"Loaded SQL Query: {sql_query}")

        # Execute the query with the provided parameters
        logger.debug(f"Executing query with post_id: {post_id}")
        cursor.execute(sql_query, {'postid': post_id, 'limit': limit})
        rows = cursor.fetchall()

        logger.debug(f"Fetched {len(rows)} rows from the database")

        # Convert each row into a RecentResolvedPost schema
        posts = [IdLimit(**dict(row)) for row in rows]
        return posts

    except Exception as e:
        logger.error(f"Error in get_posts_id_limit_service: {e}")
        raise

    finally:
        cursor.close()
