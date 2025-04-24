import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname="karaoke",
        user="postgres",
        password="D@nth3man", 
        host="localhost"
    )

def test_connection():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM singers;")
    singers = cur.fetchall()
    cur.close()
    conn.close()
    return singers

if __name__ == "__main__":
    print(test_connection())