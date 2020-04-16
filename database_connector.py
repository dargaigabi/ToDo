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

def insert_type(conn):
    cursor = conn.cursor()
    type_name = request.form['type']
    cursor.execute("""INSERT INTO type (type) values (%s);""", (type_name))

def fetch_types(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT * from type""")
    types = cursor.fetchall()
    return types

def insert_category(conn):
    cursor = conn.cursor()
    category_type = request.form['category_type']
    category = request.form['category']
    information = request.form['information']
    planned_amount = request.form['planned_amount']
    cursor.execute("""INSERT INTO category (category, planned_amount, type, information) values (%s, %s, %s, %s);""", (category, planned_amount, category_type, information))

def fetch_categories(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT * from category""")
    categories = cursor.fetchall()
    return categories