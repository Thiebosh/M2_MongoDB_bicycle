
def searchByTownAndStation(collection, town, station):
    filter = {
        "$text": {
            "$search": station
        }
    }

    return collection.find(filter)
