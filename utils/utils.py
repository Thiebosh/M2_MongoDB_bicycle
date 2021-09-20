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


def interpreter(field, fields, mapper):
    atomic_mapper = mapper[field]
    
    if not type(atomic_mapper) == dict:
        return fields[atomic_mapper]
    
    elif "addition" in atomic_mapper:
        atomic_mapper = atomic_mapper["addition"]
        return fields[atomic_mapper[0]] + fields[atomic_mapper[1]]
    
    elif "var" in atomic_mapper and "pos" in atomic_mapper:
        return fields[atomic_mapper["var"]][atomic_mapper["pos"]]

    print(f"bad json structure : no interpretation for {mapper}")
    exit(1)
