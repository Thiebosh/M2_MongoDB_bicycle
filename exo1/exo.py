from pymongo import  MongoClient, collation, collection
# from pprint import pprint

# client = MongoClient('mongodb://localhost:27017/')

# db = client.test_database # or db = client['test-database']

# collection = db.test_collection # or collection = db['test-collection']

# result = collection.insert_one({
#     "name": "Tyrion",
#     "age": 25
# })

# print('_id:', result.inserted_id)

# collection.insert_one({
#     "name": "Daenerys",
#     "age": 17
# })


# # read data
# cursors = collection.find({})
# for element in cursors:
#     pprint(element)

# # or get all data response in ram
# cursors = collection.find({})
# my_result = list(cursors)
# pprint(my_result)

import requests
import json


def get_vlille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=400"

    response = requests.request("GET", url)
    
    response_json = json.loads(response.text.encode("utf8"))

    allFields = [{**record["fields"], "geometry": record["geometry"]} for record in response_json["records"]]

    filteredFields = [{"_id" : fields["libelle"],
                    "ville" : "Lille",
                    "nom" : fields["nom"],
                    "nbvelosdispo" : fields["nbvelosdispo"],
                    "nbplacesdispo" : fields["nbplacesdispo"],
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

    lille = get_vlille()
    print(f"add 'lille' data...")
    result = collection.insert_many(lille)
    print(f"=> inserted {len(result.inserted_ids)}/{len(lille)} lines")
    
    print("\n\n")

    # lyon

    # montpellier

    print("print some data")
    for element in collection.find({ "geometry": { "$near": {"$geometry": {"type": 'Point', "coordinates":[3.0485, 50.6342]}, "$maxDistance": 500, "$minDistance": 0 } } }):
        print(element)
