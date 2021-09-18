from requests import request
import json
from pymongo.errors import WriteError


def get_lille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=400"

    response = request("GET", url)
    
    response_json = json.loads(response.text.encode("utf8"))

    allFields = [{**record["fields"], "geometry": record["geometry"]} for record in response_json["records"]]

    filteredFields = [{"_id" : fields["libelle"],
                    "ville" : "Lille",
                    "nom" : fields["nom"],
                    "nbvelosdispo" : 0,
                    "nbplacesdispo" : 0,
                    "nbplacestotal" : fields["nbvelosdispo"] + fields["nbplacesdispo"],
                    "cb" : int(fields["type"]=="AVEC TPE"), 
                    "geometry" : fields["geometry"]} for fields in allFields]

    filteredFields.sort(key=lambda x: x["_id"])

    return filteredFields

def exo1(collection):
    print("create geo index for 'geometry' field...")
    result = collection.create_index([("geometry", "2dsphere")])
    print(f"=> index name : {result}")

    print("\n\n")

    print("collect static api's datas...")
    datas = get_lille()
    
    print("\n\n")

    datas += [] # lyon

    datas += [] # montpellier

    try:
        result = collection.insert_many(datas)
        print(f"=> inserted {len(result.inserted_ids)}/{len(datas)} lines")

    except WriteError as we:
        print(we.details)

    except Exception as e:
        print("something went wrong...")
        print(e)
