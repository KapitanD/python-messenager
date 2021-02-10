from flask import Flask
from flask import jsonify
import time as t
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/status")
def status():
    return jsonify(
        {
            "status" : True,
            "name" : "Telegraph app",
            "time" : datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
    )

app.run()
