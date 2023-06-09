import psycopg2
import os
from random import randint
from dotenv import load_dotenv
from choices import df
import sys
sys.path.append('../../')
from ArtBay import db_cursor

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

        user_sql = """
        INSERT INTO Users(user_name, full_name, password)
        VALUES (%s, %s, %s)
        """

        cur.execute(user_sql, (
                "default",
                "default",
                "default"
            ))

        sql_art = """
        INSERT INTO Art(title, medium, price, descrip, picture)
        VALUES (%s, %s, %s, %s, %s) RETURNING pk
        """
        
        sql_sell = """
        INSERT INTO Sell(artist_pk, art_pk)
        VALUES (%s, %s)
        """
        
        MAX_NUM = 100
        counter = 0
        for index, row in df.iterrows():
            if counter < MAX_NUM:
                title = row['Title']
                descrip = row['Medium']

                cur.execute(sql_art, (
                    title,
                    'painting',
                    randint(1,100),
                    descrip,
                    '-',
                ))

                art_pk = cur.fetchone()[0]

                cur.execute(sql_sell, (
                    1,
                    art_pk
                ))

                conn.commit()
                counter+=1
            else:
                break

    conn.close()
