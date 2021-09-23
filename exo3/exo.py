from pprint import pprint

def exo3(collection, _, coordinates, minDistance, maxDistance, *__):
    print("print some data")
    filter = {
        "geometry": { 
            "$near": {
                "$geometry": {
                    "type": 'Point',
                    "coordinates": coordinates
                },
                "$minDistance": minDistance,
                "$maxDistance": maxDistance,
                "distanceField": "distance"
            },
        },
        "nbvelosdispo": {
            "$gt": 0
        }
    }
    projection = {
        "_id": 0,
        "nom": 1,
        "nbvelosdispo": 1,
        "nbplacesdispo": 1
    }

    # try:
    #     for element in collection.find(filter, projection).limit(3): # triangule utilisateur
    #         print(element)
    # except Exception as e:
    #     print("something went wrong...")
    #     print(type(e))
    #     print(e)

    # print("\n\n")

    try:
        for element in collection.aggregate([
            {
                "$geoNear": {
                    "near": {
                        "type": "Point",
                        "coordinates": coordinates
                    }, 
                    "minDistance": minDistance,
                    "maxDistance": maxDistance,
                    "distanceField": "distance"
                }
            },
            {
                "$match": {
                    "nbvelosdispo": {
                        "$gte": 0
                    }
                }
            },
            {
                "$project": {
                    **projection,
                    "distance": 1
                }
            },
            {
                "$facet": {
                    "closest_results": [
                        { 
                            "$limit": 3  # triangulation
                        }
                    ],
                    "total": [
                        {
                            "$count": 'nb_stations'
                        }
                    ]
                }
            },
            {
                "$unwind": "$total"
            },
            {
                "$project": {
                    "closest_results": 1,
                    "nb_stations":  "$total.nb_stations"
                }
            }
        ]):
            pprint(element)
    except Exception as e:
        print("something went wrong...")
        print(type(e))
        print(e)
