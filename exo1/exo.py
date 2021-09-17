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

    records = response_json["records"]

    allFields = [record["fields"] for record in records]

    filteredFields = [{"ville" : "Lille",
                   "nom" : fields["nom"],
                   "nbvelosdispo" : fields["nbvelosdispo"],
                   "nbplacesdispo" : fields["nbplacesdispo"],
                   "nbplacestotal" : fields["nbvelosdispo"] + fields["nbplacesdispo"],
                   "cb" : int(fields["type"]=="AVEC TPE"), 
                   "geo" : fields["geo"]} for fields in allFields]

    print(filteredFields[0])
    print("\n")
    print(len(filteredFields))

def exo1(client):

    get_vlille()
    exit()
    print(" step1 : access collection")
    collection = client.test.some

    print(" step2 : print data")
    for element in collection.find({}):
        print(element)

