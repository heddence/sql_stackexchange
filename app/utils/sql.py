import os

def load_sql_query(filename: str) -> str:
    """
    Load an SQL query from a file.

    Args:
        filename (str): The name of the SQL file to load.

    Returns:
        str: The SQL query as a string.

    Raises:
        FileNotFoundError: If the SQL file does not exist.
    """
    current_dir = os.path.dirname(__file__)
    sql_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'sql_queries', filename)
    try:
        with open(sql_path, 'r') as file:
            sql_query = file.read()
        return sql_query
    except FileNotFoundError:
        raise FileNotFoundError(f"SQL file '{filename}' not found in 'sql_queries' directory.")
