import json
import os

import requests
from lazyme.string import color_print as cprint
import time

host = "http://127.0.0.1:8000"


def check_for_new_message(user_id, client_id):
    last_msg = ""
    # check for new message every 10 seconds
    while True:
        response = requests.get(f"{host}/get_message/{user_id}/{client_id}")
        if response.status_code == 200:
            msg = response.json()[3]
            if msg != last_msg:
                cprint(msg, color='green')
                last_msg = msg
        else:
            cprint("Something went wrong", color='red')
            return False
        time.sleep(10)


def start_msg_server():
    if os.path.exists("chat.json"):
        with open("chat.json", "r") as f:
            data = json.load(f)
            user_id = data["user_id"]
            client_id = data["client_id"]
            print(f"Your user id is {user_id}")
            print(f"Your client id is {client_id}")
            print(f"If you want to change client id, delete chat.json file and restart the program.")
            check_for_new_message(user_id, client_id)
    else:
        cprint("Please create or login user first.", color='red')
        cprint("Use 'python 1_chat_io.py' to create or login user.", color='yellow')


if __name__ == '__main__':
    start_msg_server()