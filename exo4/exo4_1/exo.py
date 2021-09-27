
def searchByTownAndStation(collection, town, station):
    stationFilter = {}
    if station:
        stationFilter = {
            "nom": {
                "$regex": station,
                "$options": "i"
            }
        }

    townFilter = {}
    if town != "Tous":
        townFilter = {
            "$text": {
                "$search": town
            }
        }

    filter = {
        **stationFilter,
        **townFilter
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
        },
        {
            "$sort": {
                "_id": 1
            }
        }
    ]

    return collection.aggregate(aggregation)
