import psycopg2
from psycopg2 import sql, OperationalError

# Replace with your PostgreSQL connection parameters
DB_NAME = "karaoke"
DB_USER = "postgres"  # Replace with your PostgreSQL username
DB_PASSWORD = "D@nth3man"  # Replace with your PostgreSQL password
DB_HOST = "localhost"  # Replace with your database host, e.g., '127.0.0.1'
DB_PORT = "5432"  # Replace with your PostgreSQL port


def get_connection():
    """
    Establishes a connection to the PostgreSQL database.
    Returns the connection object.
    """
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return connection
    except OperationalError as e:
        raise RuntimeError(f"Error connecting to the database: {e}")


def add_singer(name, song_title):
    """
    Adds a singer to the PostgreSQL database.
    """
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Add the singer
        query = """
        INSERT INTO singers (name, song_title)
        VALUES (%s, %s)
        RETURNING id;
        """
        cursor.execute(query, (name, song_title))
        singer_id = cursor.fetchone()[0]

        connection.commit()
        return f"Singer {name} added successfully with ID {singer_id}!"
    except Exception as e:
        connection.rollback()
        raise RuntimeError(f"Error adding singer: {e}")
    finally:
        cursor.close()
        connection.close()


def add_to_queue(singer_id, position=None):
    """
    Adds a song to the queue for a specific singer.
    If position is not provided, it will auto-calculate the next available position.
    """
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # If position is not provided, calculate the next available position
        if position is None:
            cursor.execute("SELECT MAX(position) FROM queue;")
            max_position = cursor.fetchone()[0]
            position = (max_position or 0) + 1

        # Add the singer to the queue
        query = """
        INSERT INTO queue (singer_id, position)
        VALUES (%s, %s);
        """
        cursor.execute(query, (singer_id, position))

        connection.commit()
        return f"Singer with ID {singer_id} added to the queue at position {position}!"
    except Exception as e:
        connection.rollback()
        raise RuntimeError(f"Error adding to queue: {e}")
    finally:
        cursor.close()
        connection.close()

def update_song_title(singer_id, new_song_title):
    """
    Updates the song_title for a specific singer in the singers table.
    """
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
        UPDATE singers
        SET song_title = %s
        WHERE id = %s;
        """
        cursor.execute(query, (new_song_title, singer_id))

        connection.commit()
        return f"Singer's song updated successfully to '{new_song_title}'!"
    except Exception as e:
        connection.rollback()
        raise RuntimeError(f"Error updating song title: {e}")
    finally:
        cursor.close()
        connection.close()

def get_singer_names():
    """
    Retrieves all singer names from the database.
    """
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = "SELECT name FROM singers;"
        cursor.execute(query)
        singers = [row[0] for row in cursor.fetchall()]
        return singers
    except Exception as e:
        raise RuntimeError(f"Error retrieving singer names: {e}")
    finally:
        cursor.close()
        connection.close()


def migrate_schema():
    """
    Apply any necessary migrations to the database schema.
    """
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Example migration: Add a new column to the singers table
        query = """
        ALTER TABLE singers
        ADD COLUMN IF NOT EXISTS nickname TEXT DEFAULT NULL;
        """
        cursor.execute(query)

        connection.commit()
        return "Schema migration completed successfully!"
    except Exception as e:
        connection.rollback()
        raise RuntimeError(f"Error migrating schema: {e}")
    finally:
        cursor.close()
        connection.close()


def test_connection():
    """
    Tests the connection to the PostgreSQL database by executing a simple query.
    """
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        connection.close()
        if result:
            return "Database connection successful!"
        else:
            return "Database connection failed!"
    except Exception as e:
        return f"Database connection test failed: {e}"


# Example usage
if __name__ == "__main__":
    # Run the connection test
    print(test_connection())