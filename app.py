from flask import Flask, render_template, request, redirect
from flask_session import Session
import html

from functions import findEverything


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template("index.html")
    
    # Prevent malicious input
    username = html.escape(request.form.get("username"))
    data = findEverything(username)
    


if __name__ == '__main__':
    app.run(debug=True)