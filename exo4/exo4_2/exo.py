
def updateStation(collection, object):
    #print(object["_id"])

    match = {
        "_id": object["_id"]
        }
    query = {
        "$set": {
            **object,
        }
    }

    result = collection.update_one(match, query)
    print(result)
    return print(f"=> updated {result.modified_count}/{result.matched_count} lines")
