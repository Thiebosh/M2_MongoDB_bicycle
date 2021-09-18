import requests
import json


def get_lille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=400"

    response = requests.request("GET", url)
    
    response_json = json.loads(response.text.encode("utf8"))

    allFields = [{**record["fields"], "geometry": record["geometry"]} for record in response_json["records"]]

    filteredFields = [{"_id" : fields["libelle"],
                    "ville" : "Lille",
                    "nom" : fields["nom"],
                    "nbvelosdispo" : 0, # fields["nbvelosdispo"],
                    "nbplacesdispo" : 0, # fields["nbplacesdispo"],
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

    print(f"call api's...")
    datas = get_lille()
    
    print("\n\n")

    datas += [] # lyon

    datas += [] # montpellier

    try:
        result = collection.insert_many(datas)
        print(f"=> inserted {len(result.inserted_ids)}/{len(datas)} lines")

    except Exception as e:
        print("something went wrong...")
        print(e)
