from pymongo import MongoClient
import json
import os

from exo1.exo import exo1
from exo2.exo import exo2
from exo3.exo import exo3
from exo4.exo import exo4


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
    client = connectDB("credentials.json").TP1
    collection_live = client.live
    collection_history = client.history
    print("server's connection established")
    
    for i, exo in enumerate([exo1, exo2, exo3]):
        print(f"exo {i+1}:\n\n")

        exo(collection_live, collection_history)

        print("\n\n")
        if i != 3:
            input("continue..")

    print("everything's done")
