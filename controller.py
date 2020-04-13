from flask import Flask, request, render_template, redirect
import database_connector

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def render_main_page():
    list_of_transactions = database_connector.fetch_transactions(database_connector.connect_to_db())
    
    if request.method=='POST':
        database_connector.insert_transaction(database_connector.connect_to_db())
        return redirect("/")

    return render_template("index.html", list = list_of_transactions)
    

if __name__ == "__main__":
    app.run(debug=True)