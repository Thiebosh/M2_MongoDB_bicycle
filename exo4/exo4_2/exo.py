
def updateStation(collection, object):
    match = {
        "_id": object["_id"]
    }
    query = {
        "$set": {
            **object,
        }
    }

    result = collection.update_one(match, query)
    print(f"=> updated {result.modified_count}/{result.matched_count} lines")
