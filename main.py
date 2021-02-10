import time

db = [
    {
        'time': time.time(),
        'name': 'Jack',
        'text': 'Привет всем!',
    },
    {
        'time': time.time(),
        'name': 'Mary',
        'text': 'Привет, Jack!',
    },
]

def send_message(name, text):
    message = {
        'time': time.time(),
        'name': name,
        'text': text,
    }
    db.append(message)

def get_messages(after):
    """messages from db after given timestamp"""
    result = []
    for message in db:
        if message['time'] > after:
            result.append(message)
    return result