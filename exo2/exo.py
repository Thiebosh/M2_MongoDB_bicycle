import requests
import json
# from bson.objectid import ObjectId


def update_lille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=400"

    response = requests.request("GET", url)
    
    response_json = json.loads(response.text.encode("utf8"))

    allFields = [record["fields"] for record in response_json["records"]]

    filteredFields = [{"_id" : fields["libelle"],
                    "nbvelosdispo" : fields["nbvelosdispo"],
                    "nbplacesdispo" : fields["nbplacesdispo"]}
                    for fields in allFields]

    # filteredFields.sort(key=lambda x: x["_id"])

    return filteredFields


def exo2(collection):
    datas = update_lille()

    try:
        result = collection.update_many(
            {
                "_id": {
                    "$in": [data["_id"] for data in datas]
                }
            },
            {
                "$set" : {
                    "nbvelosdispo": [data["nbvelosdispo"] for data in datas],
                    "nbplacesdispo": [data["nbplacesdispo"] for data in datas],
                }
            }
        )

        print(f"=> updated {len(result.modified_count)}/{len(result.matched_count)}/{len(datas)} lines")

    except Exception as e:
        print("something went wrong...")
        print(e)
