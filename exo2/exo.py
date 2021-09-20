from pymongo import UpdateOne, InsertOne
from pymongo.errors import BulkWriteError
from datetime import datetime
from os import listdir

import threading
from time import sleep

from utils.utils import download
from utils.utils import readJson
from utils.utils import access_data


def update_from_api(path):
    api = readJson(path)["dynamic"]

    accessed = access_data(download(api['url']), api["data_access"])

    mapper = api["fields_mapper"]
    return [{
                "_id": f"{mapper['ville']}_{fields[mapper['_id']]}",
                "nbvelosdispo": fields[mapper['nbvelosdispo']],
                "nbplacesdispo": fields[mapper['nbplacesdispo']]
            } for fields in accessed]


def refresh(collection_live, collection_history):
    datas = []
    for file in listdir("apis"):
        datas += update_from_api(f"apis/{file}")

    try:
        result = collection_live.bulk_write([
            UpdateOne(
                {"_id": data["_id"]},
                {"$set": {
                    "nbvelosdispo": data["nbvelosdispo"],
                    "nbplacesdispo": data["nbplacesdispo"]
                }}
            )
            for data in datas]).bulk_api_result

        print(f"=> Live collection - updated {result['nModified']}/{result['nMatched']}/{len(datas)} lines")

    except BulkWriteError as bwe:
        print("Live collection - bulk_write error :")
        print(f"Index : {bwe.details['writeErrors']['index']}")
        print(f"Message : {bwe.details['writeErrors']['errmsg']}")

    except Exception as e:
        print("something went wrong...")
        print(e)

    try:
        insert_timestamp = datetime.utcnow()
        result = collection_history.bulk_write([
            InsertOne({
                "station_id": data["_id"],
                "nbvelosdispo": data["nbvelosdispo"],
                "nbplacesdispo": data["nbplacesdispo"],
                "record_timestamp": insert_timestamp
            })
            for data in datas]).bulk_api_result

        print(f"=> History collection - inserted {result['nInserted']}/{len(datas)} lines")

    except BulkWriteError as bwe:
        print("History collection - bulk_write error :")
        print(f"Index : {bwe.details['writeErrors']['index']}")
        print(f"Message : {bwe.details['writeErrors']['errmsg']}")

    except Exception as e:
        print("something went wrong...")
        print(e)


def worker(collection_live, collection_history, evt_end):
    try:
        while not evt_end.is_set():
            refresh(collection_live, collection_history)
            sleep(60) # seconds

    finally:
        print("close thread")
        evt_end.set()


def exo2(collection_live, collection_history, evt_end):
    threading.Thread(target=worker, args=(collection_live, collection_history, evt_end)).start()
