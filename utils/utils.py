import json
import os
import requests
import io
import pickle
from guizero import Box, TextBox, Text


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


def formGenerator(container, config):
    inputsContainer = Box(container, layout="grid")

    i = 0
    for (key, data) in config.items():
        Text(inputsContainer, grid=[0,i], text=data["text"].title())
        Text(inputsContainer, grid=[1,i])  # margin
        config[key]["ptr"] = TextBox(inputsContainer, grid=[2,i], width="25")

        if "value" in data:
            config[key]["ptr"].value = data["value"]
        i += 1

        Box(inputsContainer, grid=[0,i], height="5")  # margin
        i += 1


def dumpGraph(graph):
    graph_buffer = io.BytesIO()
    pickle.dump(graph, graph_buffer)
    graph_buffer.seek(0)  # crucial
    return pickle.load(graph_buffer)
