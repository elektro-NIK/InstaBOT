import json
from key import login, password
from api import API


def pretty_print_json(json_dict):
    print(json.dumps(json_dict, indent=2))


if __name__ == '__main__':
    insta = API(login=login, password=password)
    last_activity = insta.login()
    print(last_activity)
