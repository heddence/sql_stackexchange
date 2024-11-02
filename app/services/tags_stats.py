from typing import List
import psycopg2.extras
import logging

from app.schemas.tags import Stats
from app.utils.sql import load_sql_query

# Initialize a logger for this module
logger = logging.getLogger("app.services.tags_stats")


def get_tags_stats_service(connection, tag_name: str) -> List[Stats]:
    """
    Business logic to retrieve tag statistics for a specific tag.

    Args:
        connection: The database connection object.
        tag_name (str): The name of the tag to analyze.

    Returns:
        List[Stats]: A list of Stats objects representing each day of the week.
    """
    try:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Load the SQL query
        sql_query = load_sql_query("get_tags_stats.sql")
        logger.debug(f"Loaded SQL Query: {sql_query}")

        # Execute the query with the provided tag name
        logger.debug(f"Executing query for tag name: {tag_name}")
        cursor.execute(sql_query, {"tagname": tag_name})
        rows = cursor.fetchall()

        logger.debug(f"Fetched {len(rows)} rows from the database")

        # Convert each row into a TagStats schema
        tag_stats = [Stats(**dict(row)) for row in rows]
        return tag_stats

    except Exception as e:
        logger.error(f"Error in get_tags_stats_service: {e}")
        raise

    finally:
        cursor.close()
