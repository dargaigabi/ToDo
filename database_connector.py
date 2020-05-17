import psycopg2
import sys

def connect_to_db():
    try:
        conn = psycopg2.connect(dbname="budget", user="postgres", host="localhost", port="5432", password="almafa")
        conn.autocommit = True
        print("Connection successful")
    except psycopg2.Error:
        print("Connection failed")
        sys.exit(0)
    return conn

def close_db_connection(cursor, conn):
    if (conn):
        cursor.close()
        conn.close()