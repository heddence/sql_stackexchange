from typing import List
import psycopg2.extras
import logging

from app.schemas.posts import Users
from app.utils.sql import load_sql_query

# Initialize a logger for this module
logger = logging.getLogger("app.services.users_friends")


def get_posts_users_service(connection, post_id: int) -> List[Users]:
    """
    Business logic to retrieve a list of all discussants (users who have commented) on a specific post.

    The users are sorted by the time of their most recent comment on the post,
    starting with the newest and ending with the oldest.

    Args:
        connection: The database connection object.
        post_id (int): The unique identifier of the post.

    Returns:
        List[Users]: A list of Users schemas.
    """
    try:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Load the SQL query from the external file
        sql_query = load_sql_query("get_posts_users.sql")
        logger.debug(f"Loaded SQL Query: {sql_query}")

        # Execute the query with the provided user_id
        logger.debug(f"Executing query with post_id: {post_id}")
        cursor.execute(sql_query, {"postid": post_id})
        rows = cursor.fetchall()

        logger.debug(f"Fetched {len(rows)} rows from the database")

        # Convert each row into a Users schema
        users = [Users(**dict(row)) for row in rows]
        return users

    except Exception as e:
        logger.error(f"Error in get_posts_users_service: {e}")
        raise

    finally:
        cursor.close()
