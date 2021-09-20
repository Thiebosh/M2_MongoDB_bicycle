import json
from os.path import exists
from requests import request


def readJson(jsonFile):
    if not exists(jsonFile):
        print(f"Cannot found '{jsonFile}' file, close program.")
        exit(1)
    
    with open(jsonFile) as file:
        content = file.read()

    return json.loads(content)


def download(url):
    return json.loads(request("GET", url).text.encode("utf8"))


def access_data(accessed, actions):
    for key in actions:
        if not type(key) == dict:
            accessed = accessed[key]

        elif "unpack" in key:
            accessed = [record[key["unpack"]] for record in accessed]

    return accessed
