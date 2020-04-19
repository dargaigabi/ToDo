from flask import request
import psycopg2
import sys
from datetime import datetime

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
    type_name = request.form['type_name']
    cursor.execute("""INSERT INTO type (name) values (%s);""", (type_name,))

def fetch_types(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT * from type""")
    types = cursor.fetchall()
    return types

def insert_category(conn):
    cursor = conn.cursor()
    category_type = request.form['category_type']
    category_name = request.form['category_name']
    category_information = request.form['category_information']
    cursor.execute("""INSERT INTO category (name, information, type) values (%s, %s, %s);""", (category_name, category_information, category_type))

def fetch_categories(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM category""")
    categories = cursor.fetchall()
    return categories

def insert_plan(conn):
    cursor = conn.cursor()
    category_list=fetch_categories(conn)
    for item in category_list:
        category_id=item[0]
        planned_amount = request.form[str(category_id)]
        cursor.execute("""INSERT INTO plan (category_id, planned_amount, insert_date) values (%s, %s, %s);""", (category_id, planned_amount, datetime.now()))

def fetch_plans(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM plans""")
    plans = cursor.fetchall()
    return plans