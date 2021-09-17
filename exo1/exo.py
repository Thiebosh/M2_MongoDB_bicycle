# from pymongo import collation, collection
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

    allFields = [record["fields"] for record in response_json["records"]]

    filteredFields = [{"_id" : fields["libelle"],
                    "ville" : "Lille",
                    "nom" : fields["nom"],
                    "nbvelosdispo" : fields["nbvelosdispo"],
                    "nbplacesdispo" : fields["nbplacesdispo"],
                    "nbplacestotal" : fields["nbvelosdispo"] + fields["nbplacesdispo"],
                    "cb" : int(fields["type"]=="AVEC TPE"), 
                    "geometry" : {
                        "type" : "Point",
                        "coordinates": fields["geo"]
                    }
                    } for fields in allFields]

    filteredFields.sort(key=lambda x: x["_id"])

    return filteredFields

def exo1(client):

    

    print(" step1 : access collection")
    collection = client.TP1.exo1


    print(" step2 : add data")
    collection.create_index("{geometry: '2dsphere'}")
    collection.insert_many(get_vlille())
    

    print(" step3 : print data")
    for element in collection.find({}):
        print(element)


# db.stations.createIndex({geometry: "2dsphere"})
# db.stations.find({ "geometry": { $near: {$geometry: {type: 'Point', coordinates:[3.0485, 50.6342]}, $maxDistance: 500, $minDistance: 0 } } } )
