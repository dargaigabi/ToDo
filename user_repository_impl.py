import psycopg2
import database_connector
from passlib.hash import pbkdf2_sha256
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

def insert_user(conn, username, password):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO users (username, password_hash, logged_in) VALUES (%s, %s, %s);""", (username, hash_password(password), True))

def hash_password(password):
    return pbkdf2_sha256.hash(password)

@auth.verify_password
def verify_user(conn, username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = %s;", (username,))
    stored_password_hash_list = cursor.fetchone()
    stored_password_hash = stored_password_hash_list[0]
    return pbkdf2_sha256.verify(password, stored_password_hash)

def login(conn, username):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET logged_in = true WHERE username = %s;", (username,))

def check_login(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT logged_in FROM users WHERE username = %s;", (username,))
    logged_in = cursor.fetchone()
    return logged_in