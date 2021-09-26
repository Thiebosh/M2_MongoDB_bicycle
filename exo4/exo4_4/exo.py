
def flipStations(collection, objectIds, state):
    query = {
        "_id": {
            "$in": objectIds
        }
    },
    {
        "$set" : {
            "actif": state,
        }
    }

    result = collection.update_many(query)
    print(f"=> updated {result.modified_count}/{result.matched_count}/{len(objectIds)} lines")


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
