import database_connector
import psycopg2

def fetch_periods(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM period ORDER BY id DESC")
    periods = cursor.fetchall()
    return periods

def insert_period(conn, period_name, period_from, period_to):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO period (name, date_from, date_to) values (%s, %s, %s);""", (period_name, period_from, period_to))

def get_period_id_by_period_name(conn, period_name):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM period WHERE name = %s", (period_name,))
        period_id = cursor.fetchone()
        return period_id
    except (Exception, psycopg2.Error) as error :
        print ("Error while getting data from PostgreSQL", error)
    finally:
        database_connector.close_db_connection(cursor, conn)    