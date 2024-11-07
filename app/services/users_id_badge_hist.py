from typing import List
import psycopg2.extras
import logging

from app.schemas.users import IdBadgeHistory
from app.utils.sql import load_sql_query

# Initialize a logger for this module
logger = logging.getLogger("app.services.users_id_badge_hist")


def get_users_id_badge_hist(connection, user_id: int) -> List[IdBadgeHistory]:
    """
    Business logic to retrieve the badge history for the specific user with respective posts.

    Args:
        connection: The database connection object.
        user_id (int): The unique identifier of the user.

    Returns:
        List[IdBadgeHistory]: A list of IdBadgeHistory schemas.
    """
    try:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Load the SQL query from the external file
        sql_query = load_sql_query("get_users_id_badge_hist.sql")
        logger.debug(f"Loaded SQL Query: {sql_query}")

        # Execute the query with the provided user_id
        logger.debug(f"Executing query with user_id: {user_id}")
        cursor.execute(sql_query, {"userid": user_id})
        rows = cursor.fetchall()

        logger.debug(f"Fetched {len(rows)} rows from the database")

        # Convert each row into a Friends schema
        friends = [IdBadgeHistory(**dict(row)) for row in rows]
        return friends

    except Exception as e:
        logger.error(f"Error in get_user_friends_service: {e}")
        raise

    finally:
        cursor.close()
