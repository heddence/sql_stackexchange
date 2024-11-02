import os
import psycopg2
import logging

from psycopg2 import pool
from dotenv import load_dotenv

# Initialize logger
logger = logging.getLogger("app.database")

# Load environment variables from .env
load_dotenv()

# Fetch database credentials from environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Verify that all required environment variables are set
missing_vars = []
for var in ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]:
    if not os.getenv(var):
        missing_vars.append(var)

if missing_vars:
    logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
    raise EnvironmentError(f"Missing environment variables: {', '.join(missing_vars)}")

# Configure database connection pool
try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=20,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )
    if connection_pool:
        logger.info("Connection pool created successfully")
except (Exception, psycopg2.DatabaseError) as error:
    logger.error(f"Error creating connection pool: {error}")
    raise


def get_db_connection() -> psycopg2.extensions.connection:
    """
    Retrieves a connection from the connection pool.

    Returns:
        connection (psycopg2.extensions.connection): A database connection object.

    Raises:
        Exception: If unable to retrieve a connection from the pool.
    """
    try:
        conn = connection_pool.getconn()
        if conn:
            logger.debug("Successfully received connection from pool")
            return conn
    except (Exception, psycopg2.DatabaseError) as e:
        logger.error(f"Error getting connection from pool: {e}")
        raise


def release_db_connection(conn) -> None:
    """
    Releases a connection back to the connection pool.

    Args:
        conn (psycopg2.extensions.connection): The database connection to release.

    Raises:
        Exception: If unable to release the connection back to the pool.
    """
    try:
        connection_pool.putconn(conn)
        logger.debug("Connection returned to pool")
    except (Exception, psycopg2.DatabaseError) as e:
        logger.error(f"Error returning connection to pool: {e}")
