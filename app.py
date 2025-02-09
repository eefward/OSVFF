from flask import Flask, render_template, request, jsonify
from flask_session import Session
import html

from functions import findEverything


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def home():
    return render_template("index.html")
    
    
@app.route("/data", methods=['POST'])
def data():
    # Prevent malicious input
    username = html.escape(request.form.get("username"))
    data = findEverything(username)

    return jsonify({"data": data})


if __name__ == '__main__':
    app.run(debug=True)