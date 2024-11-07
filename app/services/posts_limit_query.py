from typing import List
import psycopg2.extras
import logging

from app.schemas.posts import LimitQuery
from app.utils.sql import load_sql_query

# Initialize a logger for this module
logger = logging.getLogger("app.services.posts_limit_query")


def get_posts_limit_query_service(connection, query: str, limit: int) -> List[LimitQuery]:
    """
    Business logic to retrieve a list of posts with associated tags.

    Args:
        connection: The database connection object.
        query (str): The search query to filter posts by title or body.
        limit (int): The maximum number of posts to return.

    Returns:
        List[LimitQuery]: A list of posts with associated tags matching the criteria.
    """
    try:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Load the SQL query
        sql_query = load_sql_query("get_posts_limit_query.sql")
        logger.debug(f"Loaded SQL Query: {sql_query}")

        # Prepare the search pattern for ILIKE
        search_pattern = f"%{query}%"
        logger.debug(f"Search Pattern: {search_pattern}")

        # Execute the query with the provided parameters
        logger.debug(f"Executing query with limit: {limit}")
        cursor.execute(sql_query, {'limit': limit, 'query': search_pattern})
        rows = cursor.fetchall()

        logger.debug(f"Fetched {len(rows)} rows from the database")

        # Convert each row into a RecentResolvedPost schema
        posts = [LimitQuery(**dict(row)) for row in rows]
        return posts

    except Exception as e:
        logger.error(f"Error in get_posts_users_service: {e}")
        raise

    finally:
        cursor.close()
