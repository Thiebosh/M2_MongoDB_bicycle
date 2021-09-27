
def flipStations(collection, objectIds, state):
    match = {
        "_id": {
            "$in": objectIds
        }
    }
    query = {
        "$set" : {
            "actif": state,
        }
    }

    result = collection.update_many(match, query)
    print(f"=> updated {result.modified_count}/{result.matched_count}/{len(objectIds)} lines")


def searchByPolygon(collection, polygon):
    filter = {
        "geometry": {
            "$geoWithin": {
                "$polygon": polygon
            }
        }
    }

    print(filter)

    return collection.find(filter)


def getCoordsByTown(collection):
    aggregation = [
        {
            "$project": {
                "_id": 0,
                "ville": 1,
                "coords": [
                    {
                        "$arrayElemAt": ["$geometry.coordinates", 0]
                    },
                    {
                        "$arrayElemAt": ["$geometry.coordinates", 1]
                    },
                    "$actif"
                ]
            }
        },
        {
            "$group": {
                "_id": "$ville",
                "coords": {
                    "$push": "$coords"
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "ville": "$_id",
                "coords": 1
            }
        },
        {
            "$sort": {
                "ville": 1
            }
        }
    ]

    return list(collection.aggregate(aggregation))
