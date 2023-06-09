import requests
from lazyme.string import color_print as cprint
import time
import json
import os
from constants import server_host

host = server_host


def check_for_new_message(user_id, client_id):
    # check for new message every 10 seconds
    while True:
        response = requests.get(f"{host}/get_message/{user_id}/{client_id}")
        if response.status_code == 200:
            cprint(response.json()[3], color='green')
        else:
            cprint("Something went wrong", color='red')
            return False
        time.sleep(10)


def create_or_login_user(user_id, password):
    """
       curl -X 'POST' \
         'http://127.0.0.1:8000/users/dipesh?password=1234567' \
         -H 'accept: application/json' \
         -d ''
       """
    response = requests.post(f"{host}/add_user/{user_id}?password={password}")
    if response.status_code == 400:
        cprint("User already exists. Authenticated.", color='green')
        return False
    elif response.status_code == 200:
        cprint("User created successfully", color='green')
        cprint("Remember your user id and password.", color='green')
        cprint("You can also use same user id and password to login from different devices.", color='green')
        cprint("You can also create new chat user from different device and start chatting.", color='green')
        cprint("We don't store any of your data.", color='green')
        cprint("User will be deleted automatically after 30 days of account creation.", color='green')
    else:
        cprint("Something went wrong", color='red')
        return False

    cprint(f"'{user_id}' is your user id. Share this with your client.", color='green')
    return user_id


def set_client(user_id, client_id, password):
    response = requests.get(
        f"{host}/set_or_update_client_id/?user_id={user_id}&client_id={client_id}&password={password}")
    if response.status_code == 200:
        cprint("Client id set successfully", color='green')
        return True
    else:
        cprint("Something went wrong", color='red')
        return False


def send_message(user_id, client_id, msg):
    """curl -X 'POST' \
  'http://127.0.0.1:8000/send_message/dipesh1/dipesh?message=erty' \
  -H 'accept: application/json' \
  -d ''
  """
    response = requests.post(f"{host}/send_message/{user_id}/{client_id}?message={msg}")
    if response.status_code == 200:
        cprint("Message sent successfully", color='green')
    else:
        cprint("Something went wrong", color='red')
        return False


def start_chat(user_id, client_id, password):
    user_id_status = create_or_login_user(user_id, password)
    client_id_status = set_client(user_id, client_id, password)
    if not client_id_status:
        return
    cprint("You can start chatting now.", color='green')
    cprint("Type 'exit' to exit the chat.", color='green')
    while True:
        msg = input(f"Enter your message to '{client_id}': ")
        if msg == "exit":
            break
        send_message(user_id, client_id, msg)


def start_chat_server():
    if os.path.exists("chat.json"):
        cprint("Press 1, if you want to login with existing user id and password and client id.", color='green')
        cprint("Press 2, if you want to create new user id and password and NEW CLIENT ID", color='green')
        cprint("Press 3, if you want to create new user id and password and EXISTING CLIENT ID", color='green')
        inp = input("Enter your choice (1/2/3): ")
        if inp == "1":
            with open("chat.json", "r") as f:
                data = json.load(f)
            start_chat(data["user_id"], data["client_id"], data["password"])
        elif inp == "2":
            with open("chat.json", "r") as f:
                data = json.load(f)
            client_id = input("Enter your client/friend id (alias): ")
            with open("chat.json", "w") as f:
                json.dump({"user_id": data["user_id"], "client_id": client_id, "password": data["password"]}, f)
            start_chat(data["user_id"], client_id, data["password"])
        else:
            user_id = input("Enter your user id (alias): ")
            password = input("Enter your password: ")
            client_id = input("Enter your client id (alias): ")
            save = input("Do you want to save your chat? (y/n): ")
            # save user_id, client_id, password in json file
            if save == "y":
                with open("chat.json", "w") as f:
                    json.dump({"user_id": user_id, "client_id": client_id, "password": password}, f)
            start_chat(user_id, client_id, password)
    else:
        print("Create or login with your user id and password")
        user_id = input("Enter your user id (alias): ")
        password = input("Enter your password: ")
        client_id = input("Enter your client/friend id (alias): ")
        save = input("Do you want to save your chat? (y/n): ")
        # save user_id, client_id, password in json file
        if save == "y":
            with open("chat.json", "w") as f:
                json.dump({"user_id": user_id, "client_id": client_id, "password": password}, f)

        start_chat(user_id, client_id, password)


if __name__ == '__main__':
    start_chat_server()
