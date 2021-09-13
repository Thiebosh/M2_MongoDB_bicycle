from pymongo import MongoClient
import json
import os

from exo1.exo import exo1
from exo2 import *
from exo3 import *
from exo4 import *


def connectDB(jsonFile):
    if not os.path.exists(jsonFile):
        print(f"Cannot found '{jsonFile}' file, close program.")
        exit(1)
    
    with open(jsonFile) as file:
        content = file.read()

    creds = json.loads(content)
    if set(creds.keys()) != set(['username', 'password', 'dbAccess']):
        print(f"Missing keys in your '{jsonFile}' file, close program.")
        exit(1)

    return MongoClient(f"mongodb+srv://{creds['username']}:{creds['password']}@{creds['dbAccess']}")


if __name__ == "__main__":
    client = connectDB("credentials.json")

    print("server's connection established")

    exo1(client)

    print("everything's done")
