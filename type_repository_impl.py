import database_connector

def insert_type(conn, type_name):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO type (name) values (%s);""", (type_name,))

def fetch_types(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT * from type""")
    types = cursor.fetchall()
    return types

def get_type_id_by_category_id(conn, category_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT t.id FROM type t JOIN category c ON t.name = c.type WHERE c.id = %s""", (category_id,))
    type_id = cursor.fetchone()
    return type_id
