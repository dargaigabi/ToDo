import psycopg2
import database_connector
from passlib.hash import pbkdf2_sha256
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

def insert_user(conn, username, password):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO users (username, password_hash) VALUES (%s, %s);""", (username, hash_password(password)))

def hash_password(password):
    return pbkdf2_sha256.hash(password)

@auth.verify_password
def verify_user(conn, username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = %s;", (username,))
    stored_password_hash_list = cursor.fetchone()
    stored_password_hash = stored_password_hash_list[0]
    return pbkdf2_sha256.verify(password, stored_password_hash)