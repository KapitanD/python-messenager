from flask import Flask, request, jsonify, abort
import time as t
from datetime import datetime
from pokebot import PokeBot

app = Flask(__name__)

db = []
users = set()
bot = PokeBot()

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/status")
def status():
    return jsonify(
        {
            "status" : True,
            "name" : "Telegraph app",
            "time" : datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "messages_count" : len(db),
            "users_count" : len(users)
        }
    )

@app.route("/send", methods=["POST"])
def send_message():
    data = request.json

    if not isinstance(data, dict):
        return abort(400)
    if set(data.keys()) != {"name", "text"}:
        return abort(400) 

    name = data["name"]
    text = data["text"]

    if not isinstance(name, str) or \
            not isinstance(text, str) or \
            name == "" or \
            text == "":
        return abort(400)

    users.add(name)
    message = {
        'time': t.time(),
        'name': name,
        'text': text,
    }
    db.append(message)

    bot_message = bot.check_message(text, name)
    if bot_message:
        db.append(bot_message)

    return jsonify(
        {
            "ok" : True
        }
    )

@app.route("/messages", methods=["GET"])
def get_messages():
    """messages from db after given timestamp"""
    # if "after" not in request.args:
    #     return abort(400)
    try:
        after = float(request.args["after"])
    except:
        return abort(400)

    result = []
    for message in db:
        if message['time'] > after:
            result.append(message)
            if len(result) >= 1:
                break

    return jsonify(result)

app.run()
