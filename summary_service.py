import database_connector

def count_sums(period_id):
    sum_of_recurring_expenses = database_connector.get_sum_by_type(database_connector.connect_to_db(), 'Recurring Expenses', period_id)[0] 
    sum_of_one_time_expenses = database_connector.get_sum_by_type(database_connector.connect_to_db(), 'One-Time Expenses', period_id)[0] 
    sum_of_recurring_incomes = database_connector.get_sum_by_type(database_connector.connect_to_db(), 'Recurring Incomes', period_id)[0]
    sum_of_one_time_incomes = database_connector.get_sum_by_type(database_connector.connect_to_db(), 'One-Time Incomes', period_id)[0]
    dictionary_of_sums = {"recurring_expenses": sum_of_recurring_expenses,
                    "one_time_expenses": sum_of_one_time_expenses,
                    "recurring_incomes": sum_of_recurring_incomes,
                    "one_time_incomes": sum_of_one_time_incomes}
    print(dictionary_of_sums)

    sum_of_sums = sum_of_recurring_incomes + sum_of_one_time_incomes - sum_of_recurring_expenses - sum_of_one_time_expenses
    
    dictionary_of_sums['sum'] = sum_of_sums
    
    return dictionary_of_sums
    