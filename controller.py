from flask import Flask, request, render_template, redirect, jsonify
import database_connector

app = Flask(__name__)

@app.route("/")
def render_main_page():
    list_of_transactions = database_connector.fetch_transactions(database_connector.connect_to_db())
    list_of_transactions.reverse()
    list_of_categories = database_connector.fetch_categories(database_connector.connect_to_db())
    list_of_periods = database_connector.fetch_periods(database_connector.connect_to_db())
    return render_template("transactions.html", transaction_list = list_of_transactions, category_list = list_of_categories, period_list = list_of_periods)

@app.route("/add_transaction", methods = ['POST'])
def add_transaction():    
    database_connector.insert_transaction(database_connector.connect_to_db())
    return redirect("/")
    
@app.route("/administration")
def render_administration_page():
    list_of_types = database_connector.fetch_types(database_connector.connect_to_db())
    list_of_categories = database_connector.fetch_categories(database_connector.connect_to_db())
    list_of_periods = database_connector.fetch_periods(database_connector.connect_to_db())
    return render_template("administration.html", type_list = list_of_types, category_list = list_of_categories, period_list = list_of_periods)

@app.route("/add_category", methods = ['POST'])
def add_category():    
    database_connector.insert_category(database_connector.connect_to_db())
    return redirect("/administration")

@app.route("/add_type", methods = ['POST'])
def add_type():    
    database_connector.insert_type(database_connector.connect_to_db())
    return redirect("/administration")

@app.route("/plans", methods = ['POST', 'GET'])
def render_plans_page():
    if request.method == 'GET':
        list_of_periods = database_connector.fetch_periods(database_connector.connect_to_db())
        period_id = list_of_periods[0][0]
        list_of_plans = database_connector.fetch_plans(database_connector.connect_to_db(), period_id)
        return render_template("plans.html", plan_list = list_of_plans, period_list = list_of_periods)
    period_id = request.form['period_id']
    list_of_plans = database_connector.fetch_plans(database_connector.connect_to_db(), period_id)
    return jsonify(list_of_plans = list_of_plans)

@app.route("/update_plan", methods = ['POST'])
def update_plan():
    period_name = request.form.get('period')
    list_of_period_ids = database_connector.get_period_id_by_period_name(database_connector.connect_to_db(), period_name)
    period_id = list_of_period_ids[0][0]
    list_of_plans = database_connector.fetch_plans(database_connector.connect_to_db(), period_id)
    for item in list_of_plans:
        category_id = item[0]
        print(category_id)
        planned_amount = request.form[str(category_id)]
        print(planned_amount)
        database_connector.update_plan(database_connector.connect_to_db(), period_id, category_id, planned_amount)
    return redirect("/plans")

@app.route("/plans/allocation/category-<category_id>", methods = ['POST'])
def count_summary(category_id):
    data = request.form
    type_id = database_connector.get_type_id_by_category_id(database_connector.connect_to_db(), category_id)
    return jsonify(type_id=type_id[0], 
                    amount=data['field_value'])

@app.route("/plans/period/<period_id>", methods = ['POST'])
def select_by_period(period_id):
    allocations_by_period = database_connector.get_planned_amount_by_period_id(database_connector.connect_to_db(), period_id)
    return jsonify(planned_amounts = allocations_by_period)

@app.route("/add_period", methods = ['POST'])
def add_period():    
    database_connector.insert_period(database_connector.connect_to_db())
    return redirect("/administration")

if __name__ == "__main__":
    app.run(debug=True)