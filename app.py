from flask import Flask, render_template, request, redirect
from flask_session import Session


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def home():


    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)