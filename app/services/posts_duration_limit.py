from typing import List
import psycopg2.extras
import logging

from app.schemas.posts import DurationLimit
from app.utils.sql import load_sql_query

# Initialize a logger for this module
logger = logging.getLogger("app.services.posts_duration_limit")


def get_posts_duration_limit_service(connection, duration_in_minutes: float, limit: int) -> List[DurationLimit]:
    """
    Business logic to retrieve the most recently resolved posts that were open for a maximum duration.

    Args:
        connection: The database connection object.
        duration_in_minutes (float): The maximum duration in minutes a post was open.
        limit (int): The maximum number of posts to retrieve.

    Returns:
        List[DurationLimit]: A list of recently resolved posts matching the criteria.
    """
    try:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Load the SQL query
        sql_query = load_sql_query("get_posts_duration_limit.sql")
        logger.debug(f"Loaded SQL Query: {sql_query}")

        # Execute the query with the provided parameters
        logger.debug(f"Executing query with duration_in_minutes: {duration_in_minutes}, limit: {limit}")
        cursor.execute(sql_query, {'duration_in_minutes': duration_in_minutes, 'limit': limit})
        rows = cursor.fetchall()

        logger.debug(f"Fetched {len(rows)} rows from the database")

        # Convert each row into a RecentResolvedPost schema
        recent_posts = [DurationLimit(**dict(row)) for row in rows]
        return recent_posts

    except Exception as e:
        logger.error(f"Error in get_recent_resolved_posts_service: {e}")
        raise

    finally:
        cursor.close()
