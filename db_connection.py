import psycopg2
from psycopg2 import sql, OperationalError
from models import Singer, QueueEntry
import json

DB_NAME = "karaoke"
DB_USER = "postgres"
DB_PASSWORD = "D@nth3man"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_connection():
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
    connection = get_connection()
    cursor = connection.cursor()
    try:
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
    connection = get_connection()
    cursor = connection.cursor()
    try:
        if position is None:
            cursor.execute("SELECT MAX(position) FROM queue;")
            max_position = cursor.fetchone()[0]
            position = (max_position or 0) + 1
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

def get_queue():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = """
        SELECT q.id, q.singer_id, q.position, s.id, s.name, s.song_title, s.nickname
        FROM queue q
        JOIN singers s ON q.singer_id = s.id
        ORDER BY q.position;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        queue = []
        for row in rows:
            queue_id, singer_id, position, s_id, name, song_title, nickname = row
            singer = Singer(s_id, name, song_title, nickname)
            queue_entry = QueueEntry(queue_id, singer_id, position)
            queue_entry.singer = singer
            queue.append(queue_entry)
        return queue
    except Exception as e:
        raise RuntimeError(f"Error retrieving queue: {e}")
    finally:
        cursor.close()
        connection.close()

def export_queue_to_json():
    """
    Exports the current queue to a JSON file named 'queue.json'.
    Returns a confirmation message.
    """
    try:
        queue = get_queue()
        if not queue:
            return "Queue is empty. Nothing to export."

        # Transform queue data into JSON
        queue_data = [
            {
                "position": entry.position,
                "singer_name": entry.singer.name,
                "song_title": entry.singer.song_title
            }
            for entry in queue
        ]

        # Write to queue.json
        with open("queue.json", "w") as f:
            json.dump(queue_data, f, indent=4)

        return f"Queue exported successfully to queue.json with {len(queue_data)} entries!"
    except Exception as e:
        raise RuntimeError(f"Error exporting queue to JSON: {e}")

def reorder_queue(queue_entry_id, new_position):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT position FROM queue WHERE id = %s;", (queue_entry_id,))
        current_position = cursor.fetchone()
        if not current_position:
            raise RuntimeError(f"Queue entry with ID {queue_entry_id} not found.")
        current_position = current_position[0]

        cursor.execute("SELECT MAX(position) FROM queue;")
        max_position = cursor.fetchone()[0] or 0

        if new_position < 1 or new_position > max_position:
            raise RuntimeError(f"New position must be between 1 and {max_position}.")

        if new_position < current_position:
            cursor.execute("""
                UPDATE queue
                SET position = position + 1
                WHERE position >= %s AND position < %s;
            """, (new_position, current_position))
        elif new_position > current_position:
            cursor.execute("""
                UPDATE queue
                SET position = position - 1
                WHERE position <= %s AND position > %s;
            """, (new_position, current_position))

        cursor.execute("""
            UPDATE queue
            SET position = %s
            WHERE id = %s;
        """, (new_position, queue_entry_id))

        connection.commit()
        return f"Queue entry {queue_entry_id} moved to position {new_position}!"
    except Exception as e:
        connection.rollback()
        raise RuntimeError(f"Error reordering queue: {e}")
    finally:
        cursor.close()
        connection.close()

def log_performance(singer_name, song_title):
    """
    Logs a performance in the performances table.
    """
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = """
        INSERT INTO performances (singer_name, song_title)
        VALUES (%s, %s)
        RETURNING id;
        """
        cursor.execute(query, (singer_name, song_title))
        performance_id = cursor.fetchone()[0]
        connection.commit()
        return f"Performance logged successfully with ID {performance_id}!"
    except Exception as e:
        connection.rollback()
        raise RuntimeError(f"Error logging performance: {e}")
    finally:
        cursor.close()
        connection.close()

def get_performance_log():
    """
    Retrieves the performance log from the performances table.
    Returns a list of dictionaries with performance details.
    """
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = """
        SELECT id, singer_name, song_title, timestamp
        FROM performances
        ORDER BY timestamp DESC;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        performances = [
            {
                "id": row[0],
                "singer_name": row[1],
                "song_title": row[2],
                "timestamp": row[3]
            }
            for row in rows
        ]
        return performances
    except Exception as e:
        raise RuntimeError(f"Error retrieving performance log: {e}")
    finally:
        cursor.close()
        connection.close()

def complete_performance():
    """
    Removes the singer at the front of the queue, logs their performance, and shifts the queue.
    Returns the singer's name and song title for confirmation.
    """
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Get the singer at position 1
        query = """
        SELECT q.id, s.name, s.song_title
        FROM queue q
        JOIN singers s ON q.singer_id = s.id
        WHERE q.position = 1;
        """
        cursor.execute(query)
        row = cursor.fetchone()
        if not row:
            raise RuntimeError("Queue is empty. No performance to complete.")

        queue_id, singer_name, song_title = row

        # Log the performance
        log_performance(singer_name, song_title)

        # Remove the singer from the queue
        cursor.execute("DELETE FROM queue WHERE id = %s;", (queue_id,))

        cursor.execute("""
            UPDATE queue
            SET position = position - 1
            WHERE position > 1;
        """)

        connection.commit()
        return singer_name, song_title
    except Exception as e:
        connection.rollback()
        raise RuntimeError(f"Error completing performance: {e}")
    finally:
        cursor.close()
        connection.close()

def migrate_schema():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = """
        ALTER TABLE singers
        ADD COLUMN IF NOT EXISTS nickname TEXT DEFAULT NULL;
        """
        cursor.execute(query)

        query = """
        CREATE TABLE IF NOT EXISTS performances (
            id SERIAL PRIMARY KEY,
            singer_name TEXT NOT NULL,
            song_title TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
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

if __name__ == "__main__":
    print(test_connection())