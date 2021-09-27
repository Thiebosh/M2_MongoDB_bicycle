from pymongo import MongoClient
from threading import Event
from utils.utils import readJson

from exo1.exo import exo1
from exo2.exo import exo2
from exo3.exo import exo3
from exo4.exo import exo4


def connectDB(jsonFile):
    creds = readJson(jsonFile)

    if set(creds.keys()) != set(['username', 'password', 'dbAccess']):
        print(f"Missing keys in your '{jsonFile}' file, close program.")
        exit(1)

    return MongoClient(f"mongodb+srv://{creds['username']}:{creds['password']}@{creds['dbAccess']}")


if __name__ == "__main__":
    client = connectDB("credentials.json").TP1
    collection_live = client.live
    collection_history = client.history
    print("server's connection established")

    evt_end = Event()

    try:
        exos = [
            {
                "ptr": exo1,
                "args" : ()
            },
            {
                "ptr": exo2,
                "args" : (evt_end, )
            },
            {
                "ptr": exo3,
                "args" : ()
            },
            {
                "ptr": exo4,
                "args" : ()
            }
        ]
        end = len(exos) - 1

        for i, exo in enumerate(exos):
            print(f"\nexo {i+1}:")

            exo["ptr"](collection_live, collection_history, *exo["args"])

    finally:
        # input("\nPress enter to close program...")
        evt_end.set()
        print("everything's done")
