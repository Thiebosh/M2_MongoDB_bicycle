from pymongo import UpdateOne, InsertOne
from pymongo.errors import BulkWriteError
from datetime import datetime
from os import listdir

import threading
from time import sleep

from utils.utils import download
from utils.utils import readJson
from utils.utils import access_data


def update_from_api(api):
    mapper = api["fields_mapper"]
    return [{
                "_id": f"{mapper['ville']}_{fields[mapper['_id']]}",
                "nbvelosdispo": fields[mapper['nbvelosdispo']],
                "nbplacesdispo": fields[mapper['nbplacesdispo']]
            } for fields in access_data(download(api['url']), api["data_access"])]


def refresh(api, collection_live, collection_history):
    datas = update_from_api(api)
    town = api['fields_mapper']['ville']

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

        print(f"=> '{town}' - Live collection - " +
            f"updated {result['nModified']}/{result['nMatched']}/{len(datas)} lines")

    except BulkWriteError as bwe:
        print(f"'{town}' - Live collection - bulk_write error :")
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

        print(f"=> '{town}' - History collection - inserted {result['nInserted']}/{len(datas)} lines")

    except BulkWriteError as bwe:
        print(f"'{town}' - History collection - bulk_write error :")
        print(f"Index : {bwe.details['writeErrors']['index']}")
        print(f"Message : {bwe.details['writeErrors']['errmsg']}")

    except Exception as e:
        print("something went wrong...")
        print(e)


def worker(path, collection_live, collection_history, evt_end):
    api = readJson(path)["dynamic"]
    town = api['fields_mapper']['ville']
    print(f"start refresh worker '{town}'")

    try:
        while not evt_end.is_set():
            refresh(api, collection_live, collection_history)
            sleep(api["refresh_time"]) # seconds

    finally:
        print(f"close refresh worker '{town}'")
        evt_end.set()


def exo2(collection_live, collection_history, evt_end):
    for file in listdir("apis"):
        threading.Thread(target=worker, args=(f"apis/{file}", collection_live, collection_history, evt_end)).start()
