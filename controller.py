from flask import Flask, request, render_template, redirect, jsonify
import database_connector

app = Flask(__name__)

@app.route("/")
def render_main_page():
    list_of_transactions = database_connector.fetch_transactions(database_connector.connect_to_db())
    list_of_transactions.reverse()
    list_of_categories = database_connector.fetch_categories(database_connector.connect_to_db())
    return render_template("transactions.html", transaction_list = list_of_transactions, category_list = list_of_categories)

@app.route("/add_transaction", methods = ['POST'])
def add_transaction():    
    database_connector.insert_transaction(database_connector.connect_to_db())
    return redirect("/")
    
@app.route("/administration")
def render_administration_page():
    list_of_types = database_connector.fetch_types(database_connector.connect_to_db())
    list_of_categories = database_connector.fetch_categories(database_connector.connect_to_db())
    return render_template("administration.html", type_list = list_of_types, category_list = list_of_categories)

@app.route("/add_category", methods = ['POST'])
def add_category():    
    database_connector.insert_category(database_connector.connect_to_db())
    return redirect("/administration")

@app.route("/add_type", methods = ['POST'])
def add_type():    
    database_connector.insert_type(database_connector.connect_to_db())
    return redirect("/administration")

@app.route("/plans")
def render_plans_page():
    list_of_categories = database_connector.fetch_categories(database_connector.connect_to_db())
    return render_template("plans.html", category_list = list_of_categories)

@app.route("/add_plan", methods = ['POST'])
def add_plan():    
    database_connector.insert_plan(database_connector.connect_to_db())
    return redirect("/plans")

@app.route("/plans/<category_id>", methods = ['POST'])
def count_summary(category_id):
    data = request.form
    type_id = database_connector.get_type_id_by_category_id(database_connector.connect_to_db(), category_id)
    return jsonify(type_id=type_id[0], 
                    amount=data['field_value'])

if __name__ == "__main__":
    app.run(debug=True)