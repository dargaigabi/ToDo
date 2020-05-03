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
    transaction_period = request.form['transaction_period']
    transaction_category = request.form['transaction_category']
    transaction_date = request.form['transaction_date']
    transaction_details = request.form['transaction_details']
    transaction_amount = request.form['transaction_amount']
    cursor.execute("SELECT id FROM period WHERE name = %s", (transaction_period,))
    transaction_period_id = cursor.fetchone()
    cursor.execute("INSERT INTO transaction (category, date, details, amount, period_id) values (%s, %s, %s, %s, %s);", (transaction_category, transaction_date, transaction_details, transaction_amount, transaction_period_id))

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

def fetch_periods(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM period ORDER BY id DESC")
    periods = cursor.fetchall()
    return periods

def insert_plan(conn):
    cursor = conn.cursor()
    category_list=fetch_categories(conn)
    for item in category_list:
        category_id=item[0]
        planned_amount = request.form[str(category_id)]
        cursor.execute("""INSERT INTO plan (category_id, planned_amount, insert_date) values (%s, %s, %s);""", (category_id, planned_amount, datetime.now()))

def fetch_plans(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT c.id, c.name, p.planned_amount, p.period_id, t.id
                        FROM category c
                        JOIN plan p ON c.id = p.category_id
						JOIN type t ON c.type = t.name
                        ORDER BY c.id""")
    plans = cursor.fetchall()
    return plans

def get_type_id_by_category_id(conn, category_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT t.id FROM type t JOIN category c ON t.name = c.type WHERE c.id = %s""", (category_id,))
    type_id = cursor.fetchone()
    return type_id

def get_planned_amount_by_period_id(conn, period_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT planned_amount FROM plan WHERE period_id = %s ORDER BY id", (period_id,))
        planned_amounts = cursor.fetchall()
        return planned_amounts
    except (Exception, psycopg2.Error) as error :
        print ("Error while getting data from PostgreSQL", error)
    finally:
        close_db_connection(cursor, conn)

def close_db_connection(cursor, conn):
    if (conn):
        cursor.close()
        conn.close()