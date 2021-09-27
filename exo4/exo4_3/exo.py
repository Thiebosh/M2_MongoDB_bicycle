# from bson.objectid import ObjectId

def deleteStation(collection_live, collection_history, objectIds):
    match = {
        "_id": {
            "$in": objectIds
        }
    }

    result_live = collection_live.delete_many(match)
    result_history = collection_history.delete_many(match)
    print(f"=> All selected stations erased : {result_history.acknowledged and result_history.acknowledged}")
