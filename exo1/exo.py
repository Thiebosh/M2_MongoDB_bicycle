from pymongo.errors import WriteError
from os import listdir

from utils.utils import download
from utils.utils import readJson
from utils.utils import access_data


def interpreter(field, fields, mapper):
    atomic_mapper = mapper[field]
    
    if not type(atomic_mapper) == dict:
        return fields[atomic_mapper]
    
    elif "addition" in atomic_mapper:
        atomic_mapper = atomic_mapper["addition"]
        return fields[atomic_mapper[0]] + fields[atomic_mapper[1]]
    
    elif "var" in atomic_mapper and "pos" in atomic_mapper:
        return fields[atomic_mapper["var"]][atomic_mapper["pos"]]

    print(f"bad json structure : no interpretation for {mapper}")
    exit(1)


def insert_from_api(path):
    api = readJson(path)["static"]

    print(f"starting {api['fields_mapper']['ville']}...")

    mapper = api["fields_mapper"]
    return [{
                "_id": f"{mapper['ville']}_{fields[mapper['_id']]}",
                "ville": mapper['ville'],
                "nom": fields[mapper['nom']],
                "nbvelosdispo": 0,
                "nbplacesdispo": 0,
                "nbplacestotal": interpreter("nbplacestotal", fields, mapper),
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        interpreter("longitude", fields, mapper),
                        interpreter("latitude", fields, mapper)
                ]}
            } for fields in access_data(download(api['url']), api["data_access"])]


def exo1(collection, *_):
    collection.delete_many({})
    print("\nLive DB cleaned")

    print("create geo index for 'geometry' field...")
    result = collection.create_index([("geometry", "2dsphere")])
    print(f"=> index name : {result}")

    print("\nCollect static api's datas...")
    datas = []
    for file in listdir("apis"):
        datas += insert_from_api(f"apis/{file}")

    print("Collect done - uploading...")
    try:
        result = collection.insert_many(datas)
        print(f"=> inserted {len(result.inserted_ids)}/{len(datas)} lines")

    except WriteError as we:
        print(we.details)

    except Exception as e:
        print("something went wrong...")
        print(e)
