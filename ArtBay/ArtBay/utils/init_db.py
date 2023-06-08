import psycopg2
import os

from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    conn = psycopg2.connect(
        host="localhost",
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD')
    )
    with conn.cursor() as cur:
        # Run users.sql
        with open('users.sql') as db_file:
            cur.execute(db_file.read())
        with open('art.sql') as db_file:
            cur.execute(db_file.read())

        conn.commit()

    conn.close()
