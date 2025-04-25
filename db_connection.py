import psycopg2
from psycopg2 import sql

def get_db_connection():
    """
    Establish a connection to the database.
    """
    try:
        return psycopg2.connect(
            dbname="karaoke",
            user="postgres",
            password="D@nth3man",  
            host="localhost"
        )
    except psycopg2.Error as e:
        raise Exception(f"Failed to connect to database: {e}")

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """
    Execute a database query with optional parameters.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, params or ())
        result = None
        if fetch_one:
            result = cur.fetchone()
        elif fetch_all:
            result = cur.fetchall()
        conn.commit()
        return result
    except psycopg2.Error as e:
        raise Exception(f"Database query failed: {e}")
    finally:
        cur.close()
        conn.close()

def migrate_schema():
    """
    Perform schema migration to update the singers table.
    """
    query_check_column = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'singers' AND column_name = 'song_id';
    """
    has_song_id = execute_query(query_check_column, fetch_one=True) is not None

    if has_song_id:
        print("Migrating singers table to use song_title...")
        execute_query("ALTER TABLE singers ADD COLUMN song_title VARCHAR(200);")
        execute_query("""
            UPDATE singers
            SET song_title = CASE
                WHEN song_id = 1 THEN 'Let It Be'
                WHEN song_id = 2 THEN 'Sweet Caroline'
                WHEN song_id = 3 THEN 'Imagine'
                ELSE 'Unknown'
            END;
        """)
        execute_query("ALTER TABLE singers ALTER COLUMN song_title SET NOT NULL;")
        execute_query("ALTER TABLE singers DROP COLUMN song_id;")
        print("Schema migration completed successfully.")
    else:
        print("Schema already up to date (song_title exists).")

def test_connection():
    """
    Test database connection and verify singers table schema.
    """
    query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'singers';
    """
    columns = [row[0] for row in execute_query(query, fetch_all=True)]
    expected_columns = {'id', 'name', 'song_title'}
    schema_ok = set(columns) == expected_columns
    return {
        "connection": "successful",
        "schema": "correct" if schema_ok else f"incorrect (columns: {columns})"
    }

def add_singer(name, song_title):
    """
    Add a new singer to the database.
    """
    query = "INSERT INTO singers (name, song_title) VALUES (%s, %s) RETURNING id;"
    return execute_query(query, params=(name, song_title), fetch_one=True)[0]

def update_song(name, new_song_title):
    """
    Update a singer's song in the database.
    """
    query = "UPDATE singers SET song_title = %s WHERE name = %s;"
    execute_query(query, params=(new_song_title, name))

def add_to_queue(singer_id):
    """
    Add a singer to the karaoke queue.
    """
    query_max_position = "SELECT MAX(position) FROM queue;"
    max_position = execute_query(query_max_position, fetch_one=True)[0] or 0
    new_position = max_position + 1
    query_insert = "INSERT INTO queue (singer_id, position) VALUES (%s, %s);"
    execute_query(query_insert, params=(singer_id, new_position))

def get_singer_names():
    """
    Fetch all singer names from the database.
    """
    query = "SELECT name FROM singers;"
    return [row[0] for row in execute_query(query, fetch_all=True)]

if __name__ == "__main__":
    print(test_connection())