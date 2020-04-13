from flask import request
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

def insert_transaction(conn):
    cursor = conn.cursor()
    transaction_category = request.form['transaction_category']
    transaction_date = request.form['transaction_date']
    transaction_details = request.form['transaction_details']
    transaction_amount = request.form['transaction_amount']
    cursor.execute("""INSERT INTO transaction (category, date, details, amount) values (%s, %s, %s, %s);""", (transaction_category, transaction_date, transaction_details, transaction_amount))

def fetch_transactions(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT * from transaction""")
    transactions = cursor.fetchall()
    return transactions 