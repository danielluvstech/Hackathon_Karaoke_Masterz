import psycopg2
from psycopg2 import sql

def get_db_connection():
    try:
        return psycopg2.connect(
            dbname="karaoke",
            user="postgres",
            password="D@nth3man",  
            host="localhost"
        )
    except psycopg2.Error as e:
        raise Exception(f"Failed to connect to database: {e}")

def migrate_schema():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if song_id column exists in singers table
        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'singers' AND column_name = 'song_id';
        """)
        has_song_id = cur.fetchone() is not None
        
        if has_song_id:
            print("Migrating singers table to use song_title...")
            
            # Step 1: Add song_title column
            cur.execute("ALTER TABLE singers ADD COLUMN song_title VARCHAR(200);")
            
            # Step 2: Populate song_title based on song_id
            cur.execute("""
                UPDATE singers
                SET song_title = CASE
                    WHEN song_id = 1 THEN 'Let It Be'
                    WHEN song_id = 2 THEN 'Sweet Caroline'
                    WHEN song_id = 3 THEN 'Imagine'
                    ELSE 'Unknown'
                END;
            """)
            
            # Step 3: Make song_title NOT NULL
            cur.execute("ALTER TABLE singers ALTER COLUMN song_title SET NOT NULL;")
            
            # Step 4: Drop song_id column
            cur.execute("ALTER TABLE singers DROP COLUMN song_id;")
            
            print("Schema migration completed successfully.")
        else:
            print("Schema already up to date (song_title exists).")
        
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error during schema migration: {e}")
        raise

def test_connection():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Verify singers table schema
        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'singers';
        """)
        columns = [row[0] for row in cur.fetchall()]
        expected_columns = {'id', 'name', 'song_title'}
        schema_ok = set(columns) == expected_columns
        cur.close()
        conn.close()
        return {
            "connection": "successful",
            "schema": "correct" if schema_ok else f"incorrect (columns: {columns})"
        }
    except psycopg2.Error as e:
        return {"connection": f"failed: {e}", "schema": "not checked"}

def add_singer(name, song_title):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO singers (name, song_title) VALUES (%s, %s) RETURNING id;",
            (name, song_title)
        )
        singer_id = cur.fetchone()[0]
        conn.commit()
        return singer_id
    except psycopg2.Error as e:
        raise Exception(f"Error adding singer: {e}")
    finally:
        cur.close()
        conn.close()

def update_song(name, new_song_title):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE singers SET song_title = %s WHERE name = %s;",
            (new_song_title, name)
        )
        conn.commit()
    except psycopg2.Error as e:
        raise Exception(f"Error updating song: {e}")
    finally:
        cur.close()
        conn.close()

def add_to_queue(singer_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT MAX(position) FROM queue;")
        max_position = cur.fetchone()[0] or 0
        new_position = max_position + 1
        cur.execute(
            "INSERT INTO queue (singer_id, position) VALUES (%s, %s);",
            (singer_id, new_position)
        )
        conn.commit()
    except psycopg2.Error as e:
        raise Exception(f"Error adding to queue: {e}")
    finally:
        cur.close()
        conn.close()

def get_singer_names():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name FROM singers;")
        names = [row[0] for row in cur.fetchall()]
        return names
    except psycopg2.Error as e:
        raise Exception(f"Error fetching singer names: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    print(test_connection())