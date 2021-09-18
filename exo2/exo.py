from requests import request
import json
from pymongo import UpdateOne
from pymongo.errors import BulkWriteError
# from bson.objectid import ObjectId


def update_lille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=400"

    response = request("GET", url)
    
    response_json = json.loads(response.text.encode("utf8"))

    allFields = [record["fields"] for record in response_json["records"]]

    filteredFields = [{"_id" : fields["libelle"],
                    "nbvelosdispo" : fields["nbvelosdispo"],
                    "nbplacesdispo" : fields["nbplacesdispo"]}
                    for fields in allFields]

    return filteredFields


def exo2(collection):
    print("collect dynamic api's datas...")
    datas = update_lille()
    datas += [] # lyon
    datas += [] # montpellier

    try:
        # result = collection.update_many(
        #     {
        #         "_id": {
        #             "$in": [data["_id"] for data in datas]
        #         }
        #     },
        #     {
        #         "$set" : {
        #             "nbvelosdispo": [data["nbvelosdispo"] for data in datas],
        #             "nbplacesdispo": [data["nbplacesdispo"] for data in datas]
        #         }
        #     }
        # )

        # print(f"=> updated {result.modified_count}/{result.matched_count}/{len(datas)} lines")

        result = collection.bulk_write([
                UpdateOne(
                    { "_id": data["_id"] },
                    { "$set": {
                            "nbvelosdispo": data["nbvelosdispo"],
                            "nbplacesdispo": data["nbplacesdispo"]
                    } }
                )
            for data in datas]).bulk_api_result

        print(f"=> updated {result['nModified']}/{result['nMatched']}/{len(datas)} lines")

    except BulkWriteError as bwe:
        print(bwe.details.writeErrors)

    except Exception as e:
        print("something went wrong...")
        print(e)
