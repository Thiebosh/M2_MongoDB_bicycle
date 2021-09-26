import json
import os
import requests


def listFiles(path):
    return [f"{path}/{name}" for name in os.listdir(path) if os.path.isfile(f"{path}/{name}")]


def readJson(jsonFile):
    if not os.path.exists(jsonFile):
        print(f"Cannot found '{jsonFile}' file, close program.")
        exit(1)
    
    with open(jsonFile) as file:
        content = file.read()

    return json.loads(content)


def download(url):
    return requests.get(url).json()


def access_data(accessed, actions):
    for key in actions:
        if not type(key) == dict:
            accessed = accessed[key]

        elif "unpack" in key:
            accessed = [record[key["unpack"]] for record in accessed]

    return accessed
