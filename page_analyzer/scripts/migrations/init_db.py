import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
user = os.getenv('PGUSER')
pwd = os.getenv('PGPASSWORD')
host = os.getenv('PGHOST')
port = os.getenv('PGPORT')
PDB_URL = os.getenv('SERVICEDB_URL')
DB_NAME = os.getenv('PGDATABASE')


def init_db(db_name: str):
    try:
        conn = psycopg2.connect(PDB_URL)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(f'DROP DATABASE IF EXISTS {db_name};')
            cur.execute(f'CREATE DATABASE {db_name};')
        conn.close()
    except Exception as err:
        print(err)
        print('Cannot Connect to DB')


def scheme_from_file():
    with psycopg2.connect(DATABASE_URL) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(open('database.sql', 'r').read())


def main():
    init_db(DB_NAME)
    scheme_from_file()


if __name__ == '__main__':
    main()
