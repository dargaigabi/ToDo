from flask import Flask, request, render_template, redirect, jsonify
import database_connector
import transaction_repository_impl
import type_repository_impl
import period_repository_impl
import category_repository_impl
import plan_repository_impl
import user_repository_impl

app = Flask(__name__)

@app.route("/")
def render_main_page():
    list_of_categories = category_repository_impl.fetch_categories(database_connector.connect_to_db())
    list_of_periods = period_repository_impl.fetch_periods(database_connector.connect_to_db())
    period_id = list_of_periods[0][0]
    dictionary_of_sums = transaction_repository_impl.count_sums(period_id)
    return render_template("transactions.html", category_list = list_of_categories, period_list = list_of_periods, sum_dictionary = dictionary_of_sums)

@app.route("/<period_id>", methods = ['POST'])
def refresh_transactions_by_period(period_id):
    list_of_transactions = transaction_repository_impl.fetch_transactions_by_period_id(database_connector.connect_to_db(), period_id)
    list_of_transactions.reverse()
    dictionary_of_sums = transaction_repository_impl.count_sums(period_id)
    return jsonify(list_of_transactions = list_of_transactions, dictionary_of_sums = dictionary_of_sums)

@app.route("/add_transaction", methods = ['POST'])
def add_transaction():    
    transaction_period = request.form['transaction_period']
    transaction_category = request.form['transaction_category']
    transaction_date = request.form['transaction_date']
    transaction_details = request.form['transaction_details']
    transaction_amount = request.form['transaction_amount']
    transaction_repository_impl.insert_transaction(database_connector.connect_to_db(), transaction_period, transaction_category, transaction_date, transaction_details, transaction_amount)
    return redirect("/")
    
@app.route("/administration")
def render_administration_page():
    list_of_types = type_repository_impl.fetch_types(database_connector.connect_to_db())
    list_of_categories = category_repository_impl.fetch_categories(database_connector.connect_to_db())
    list_of_periods = period_repository_impl.fetch_periods(database_connector.connect_to_db())
    return render_template("administration.html", type_list = list_of_types, category_list = list_of_categories, period_list = list_of_periods)

@app.route("/add_category", methods = ['POST'])
def add_category():
    category_type = request.form['category_type']
    category_name = request.form['category_name']
    category_information = request.form['category_information']    
    category_repository_impl.insert_category(database_connector.connect_to_db(),category_type, category_name, category_information)
    return redirect("/administration")

@app.route("/add_type", methods = ['POST'])
def add_type():
    type_name = request.form['type_name']    
    type_repository_impl.insert_type(database_connector.connect_to_db(), type_name)
    return redirect("/administration")

@app.route("/plans", methods = ['POST', 'GET'])
def render_plans_page():
    if request.method == 'GET':
        list_of_periods = period_repository_impl.fetch_periods(database_connector.connect_to_db())
        period_id = list_of_periods[0][0]
        list_of_plans = plan_repository_impl.fetch_plans_by_period_id(database_connector.connect_to_db(), period_id)
        return render_template("plans.html", plan_list = list_of_plans, period_list = list_of_periods)
    period_id = request.form['period_id']
    list_of_plans = plan_repository_impl.fetch_plans_by_period_id(database_connector.connect_to_db(), period_id)
    return jsonify(list_of_plans = list_of_plans)

@app.route("/update_plan", methods = ['POST'])
def update_plan():
    period_name = request.form.get('period')
    list_of_period_ids = period_repository_impl.get_period_id_by_period_name(database_connector.connect_to_db(), period_name)
    period_id = list_of_period_ids[0]
    list_of_plans = plan_repository_impl.fetch_plans_by_period_id(database_connector.connect_to_db(), period_id)
    for item in list_of_plans:
        category_id = item[0]
        planned_amount = request.form[str(category_id)]
        plan_repository_impl.update_plan(database_connector.connect_to_db(), period_id, category_id, planned_amount)
    return redirect("/plans")

@app.route("/plans/allocation/category-<category_id>", methods = ['POST'])
def count_summary(category_id):
    type_id = type_repository_impl.get_type_id_by_category_id(database_connector.connect_to_db(), category_id)
    return jsonify(type_id=type_id[0])

@app.route("/plans/period/<period_id>", methods = ['POST'])
def select_by_period(period_id):
    allocations_by_period = plan_repository_impl.get_planned_amount_by_period_id(database_connector.connect_to_db(), period_id)
    return jsonify(planned_amounts = allocations_by_period)

@app.route("/add_period", methods = ['POST'])
def add_period():
    period_name = request.form['period_name']
    period_from = request.form['period_from']
    period_to = request.form['period_to']    
    period_repository_impl.insert_period(database_connector.connect_to_db(), period_name, period_from, period_to)
    plan_repository_impl.insert_plan(database_connector.connect_to_db())
    return redirect("/administration")

@app.route("/signup")
def render_signup():
    return render_template("signup.html")

@app.route("/add_user", methods = ['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']
    user_repository_impl.insert_user(database_connector.connect_to_db(), username, password)
    return redirect("/signup")

@app.route("/login")
def render_login():
    return render_template("login.html")

@app.route("/verify_user", methods = ['POST'])
def verify_user():
    username = request.form['username']
    password = request.form['password']
    user_repository_impl.verify_user(database_connector.connect_to_db(), username, password)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)