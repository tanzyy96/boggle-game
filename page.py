from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template("main.html")