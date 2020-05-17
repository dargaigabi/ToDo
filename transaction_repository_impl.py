import database_connector

def insert_transaction(conn, period, category, date, details, amount):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM period WHERE name = %s", (period,))
    period_id = cursor.fetchone()
    cursor.execute("INSERT INTO transaction (category, date, details, amount, period_id) values (%s, %s, %s, %s, %s);", (category, date, details, amount, period_id))

def fetch_transactions_by_period_id(conn, period_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT * from transaction WHERE period_id = %s""", (period_id,))
    transactions = cursor.fetchall()
    return transactions

def get_sum_by_type(conn, category_type, period_id):
    cursor = conn.cursor()
    cursor.execute("""select coalesce(sum(t.amount), 0)
                        from transaction t join category c on t.category = c.name
                        where c.type = %s and t.period_id = %s""", (category_type, period_id))
    sum_of_recurring_expenses = cursor.fetchone()
    return sum_of_recurring_expenses

def count_sums(period_id):
    sum_of_recurring_expenses = get_sum_by_type(database_connector.connect_to_db(), 'Recurring Expenses', period_id)[0] 
    sum_of_one_time_expenses = get_sum_by_type(database_connector.connect_to_db(), 'One-Time Expenses', period_id)[0] 
    sum_of_recurring_incomes = get_sum_by_type(database_connector.connect_to_db(), 'Recurring Incomes', period_id)[0]
    sum_of_one_time_incomes = get_sum_by_type(database_connector.connect_to_db(), 'One-Time Incomes', period_id)[0]
    dictionary_of_sums = {"recurring_expenses": sum_of_recurring_expenses,
                    "one_time_expenses": sum_of_one_time_expenses,
                    "recurring_incomes": sum_of_recurring_incomes,
                    "one_time_incomes": sum_of_one_time_incomes}

    sum_of_sums = sum_of_recurring_incomes + sum_of_one_time_incomes - sum_of_recurring_expenses - sum_of_one_time_expenses
    
    dictionary_of_sums['sum'] = sum_of_sums
    
    return dictionary_of_sums