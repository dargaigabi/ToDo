import database_connector

def insert_category(conn, category_type, category_name, category_information):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO category (name, information, type) values (%s, %s, %s);""", (category_name, category_information, category_type))

def fetch_categories(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM category""")
    categories = cursor.fetchall()
    return categories

