import datetime
import os
from dotenv import load_dotenv
import psycopg2


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
user = os.getenv('PGUSER')
pwd = os.getenv('PGPASSWORD')
host = os.getenv('PGHOST')
port = os.getenv('PGPORT')
pdb_name = os.getenv('PGDATABASE')
PDB_URL = f'postgresql://{user}:{pwd}@{host}:{port}/postgres'
DB_NAME = os.getenv('PGDATABASE')

def init_db(db_name: str):
    try:
        conn = psycopg2.connect(PDB_URL)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS {db_name};")
            cur.execute(f"CREATE DATABASE {db_name};")
        conn.close()
    except Exception as err:
        print(err)
        print('Cannot Connect to DB')


def my_create_scheme(db_name: str):
    with psycopg2.connect(DATABASE_URL) as conn:
        conn.autocommit = True    
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE urls (id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY, name varchar(80), created_at timestamp);")
            cur.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s)", ('Number one', datetime.datetime.now()))


def scheme_from_file(db_name):
    with psycopg2.connect(DATABASE_URL) as conn:
        conn.autocommit = True    
        with conn.cursor() as cursor:
            cursor.execute(open("database.sql", "r").read())


init_db(DB_NAME)
scheme_from_file(DB_NAME)
