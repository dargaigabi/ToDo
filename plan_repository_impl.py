import psycopg2
from datetime import datetime
import database_connector
import category_repository_impl
import period_repository_impl

def insert_plan(conn):
    cursor = conn.cursor()
    category_list=category_repository_impl.fetch_categories(conn)
    period_list=period_repository_impl.fetch_periods(conn)
    period_id=period_list[0][0]
    for item in category_list:
        category_id=item[0]
        cursor.execute("""INSERT INTO plan (category_id, planned_amount, insert_date, period_id) values (%s, 0, %s, %s)""", (category_id, datetime.now(), period_id))

def update_plan(conn, period_id, category_id, planned_amount):
    try:
        cursor = conn.cursor()
        cursor.execute("""UPDATE plan SET planned_amount = %s, insert_date = %s
                        WHERE period_id = %s
                        AND category_id = %s""", (planned_amount, datetime.now(), period_id, category_id))
    except (Exception, psycopg2.Error) as error :
        print ("Error while getting data from PostgreSQL", error)
    finally:
        database_connector.close_db_connection(cursor, conn)

def fetch_plans_by_period_id(conn, period_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT c.id, c.name, p.planned_amount, p.period_id, t.id
                        FROM category c
                        JOIN plan p ON c.id = p.category_id
						JOIN type t ON c.type = t.name
						WHERE p.period_id = %s
                        ORDER BY c.id""", (period_id, ))
    plans = cursor.fetchall()
    return plans

def get_planned_amount_by_period_id(conn, period_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT planned_amount FROM plan WHERE period_id = %s ORDER BY id", (period_id,))
        planned_amounts = cursor.fetchall()
        return planned_amounts
    except (Exception, psycopg2.Error) as error :
        print ("Error while getting data from PostgreSQL", error)
    finally:
        database_connector.close_db_connection(cursor, conn)