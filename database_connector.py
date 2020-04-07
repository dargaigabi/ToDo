from flask import request
import psycopg2
import sys

def connect_to_db():
    try:
        conn = psycopg2.connect(dbname="project_1", user="postgres", host="localhost", port="5432", password="almafa")
        conn.autocommit = True
        print("Connection successful")
    except psycopg2.Error:
        print("Connection failed")
        sys.exit(0)
    return conn

def insert_text(conn):
    cursor = conn.cursor()
    text = request.form['task']
    cursor.execute("""INSERT INTO tasks (task) values (%s);""", (text,))

def fetch_text(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT * from tasks""")
    records = cursor.fetchall()
    return records 