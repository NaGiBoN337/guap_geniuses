import json
def load_users_info(id):
    with open("users.json", "r") as my_file:
        capitals_json = my_file.read()
    src = json.loads(capitals_json)
    return src.get(str(id), 3)

def load_users():
    with open("users.json", "r") as my_file:
        capitals_json = my_file.read()

    src = json.loads(capitals_json)
    return src