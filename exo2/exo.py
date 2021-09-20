from requests import request
import json
from datetime import datetime
from pymongo import UpdateOne, InsertOne
from pymongo.errors import BulkWriteError


# from bson.objectid import ObjectId

import threading
from time import sleep


def update_Lyon():
    url = "https://transport.data.gouv.fr/gbfs/lyon/station_status.json"

    response = request("GET", url)

    response_json = json.loads(response.text.encode("utf8"))

    filteredFields = [{"_id": f"Lyon_{fields['station_id']}",
                       "nbvelosdispo": fields["num_bikes_available"],
                       "nbplacesdispo": fields["num_docks_available"]}
                      for fields in response_json["data"]["stations"]]

    return filteredFields


def update_montpellier():
    url = "https://data.opendatasoft.com/api/records/1.0/search/?dataset=disponibilite-des-places-velomagg-en-temps" \
          "-reel%40occitanie&q=&rows=100 "

    response = request("GET", url)

    response_json = json.loads(response.text.encode("utf8"))

    allFields = [record["fields"] for record in response_json["records"]]

    filteredFields = [{"_id": f"Montpellier_{fields['id']}",
                       "nbvelosdispo": fields["av"],
                       "nbplacesdispo": fields["fr"]}
                      for fields in allFields]

    return filteredFields


def update_lille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=400"

    response = request("GET", url)

    response_json = json.loads(response.text.encode("utf8"))

    allFields = [record["fields"] for record in response_json["records"]]

    filteredFields = [{"_id": f"Lille_{fields['libelle']}",
                       "nbvelosdispo": fields["nbvelosdispo"],
                       "nbplacesdispo": fields["nbplacesdispo"]}
                      for fields in allFields]

    return filteredFields


def refresh(collection_live, collection_history):
    datas = update_lille()
    print("Lille done")
    datas += update_Lyon()
    print("Lyon done")
    datas += update_montpellier()
    print("Montpellier done")
    
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

        print(f"=> History collection - updated {result['nInserted']}/{len(datas)} lines")

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
            sleep(2) # seconds

    finally:
        print("close thread")
        evt_end.set()


def exo2(collection_live, collection_history, evt_end):
    threading.Thread(target=worker, args=(collection_live, collection_history, evt_end)).start()
