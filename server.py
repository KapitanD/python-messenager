"""server.py
Реализация сервера для мессенеджера
"""
import time as t
from datetime import datetime
from flask import Flask, request, jsonify, abort
from pokebot import PokeBot

app = Flask(__name__)

db = []
users = set()
bot = PokeBot()
db.append(bot.check_message("/help", "все"))


@app.route("/")
def hello():
    """handler for root
    """
    return "Hello, World!"


@app.route("/status")
def status():
    """handler for status
    return status, name of service, current server time, number of messages and users
    """
    return jsonify(
        {
            "status": True,
            "name": "Telegraph app",
            "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "messages_count": len(db),
            "users_count": len(users)
        }
    )


@app.route("/send", methods=["POST"])
def send_message():
    """handler for send
    POST body format:
    {
        "name" : string,
        "text" : string
    }
    validation error - 400,
    return message:
    {
        "ok" : True
    }
    Status code for ok: 200
    """
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
            "ok": True
        }
    )


@app.route("/messages", methods=["GET"])
def get_messages():
    """handler for messages
    GET needs parameter after : float
    validation error - 400,
    return message:
    [
        {
            "time" : timestamp,
            "name" : string,
            "text" : string
        },
        ...
    ]
    Status code for ok: 200
    """
    try:
        after = float(request.args["after"])
    except KeyError:
        return abort(400)
    except ValueError:
        return abort(400)

    result = []
    for message in db:
        if message['time'] > after:
            result.append(message)
            if len(result) >= 1:
                break

    return jsonify(result)


app.run()
