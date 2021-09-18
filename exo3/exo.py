from pprint import pprint

def exo3(collection):
    print("print some data")
    for element in collection.find({ "geometry": { "$near": {"$geometry": {"type": 'Point', "coordinates":[3.0485, 50.6342]}, "$maxDistance": 300, "$minDistance": 0 } } }):
        pprint(element)
