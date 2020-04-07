from flask import Flask, request, render_template
import database_connector

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def render_main_page():
    list_of_tasks = []
    if request.method=='POST':
        database_connector.insert_text(database_connector.connect_to_db())
        list_of_tasks = database_connector.fetch_text(database_connector.connect_to_db())
    return render_template("index.html", list = list_of_tasks)
    

if __name__ == "__main__":
    app.run(debug=True)