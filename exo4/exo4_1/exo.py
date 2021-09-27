
def searchByTownAndStation(collection, town, station):
    filter = {
        # regex pour station
        "$text": {
            "$search": town
        }
    }

    return collection.find(filter)


def getTowns(collection):
    aggregation = [
        {
            "$project": {
                "_id": 0,
                "ville": 1
            }
        },
        {
            "$group": {
                "_id": "$ville"
            }
        }
    ]

    return list(collection.aggregate(aggregation))
