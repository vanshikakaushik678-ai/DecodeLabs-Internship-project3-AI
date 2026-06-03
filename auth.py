import json
import os

USER_FILE = "user_data/user.json"

def load_users():

    if not os.path.exists(USER_FILE):
        return {}

    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):

    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register(username, password):

    users = load_users()

    if username in users:
        return False

    users[username] = password

    save_users(users)

    return True

def login(username, password):

    users = load_users()

    return users.get(username) == password