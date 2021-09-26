
def flipStations(collection, objectIds, state):
    pass
    # update all ids with one state


def getCoordsByTown(collection):
    aggregation = [
        {
            "$project": {
                "_id": 0,
                "ville": 1,
                "coords": "$geometry.coordinates"
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
    ]

    return list(collection.aggregate(aggregation))
