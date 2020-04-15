from flask import Flask, request, render_template, redirect
import database_connector

app = Flask(__name__)

@app.route("/")
def render_main_page():
    list_of_transactions = database_connector.fetch_transactions(database_connector.connect_to_db())
    list_of_transactions.reverse()
    return render_template("transactions.html", transaction_list = list_of_transactions)

@app.route("/add_transaction", methods = ['POST'])
def add_transaction():    
    database_connector.insert_transaction(database_connector.connect_to_db())
    return redirect("/")
    
@app.route("/administration")
def render_administration_page():
    list_of_types = database_connector.fetch_types(database_connector.connect_to_db())
    list_of_categories = database_connector.fetch_categories(database_connector.connect_to_db())
    return render_template("administration.html", type_list = list_of_types, category_list = list_of_categories)

@app.route("/plans")
def render_plans_page():
    return render_template("plans.html")

if __name__ == "__main__":
    app.run(debug=True)