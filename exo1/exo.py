from pymongo.errors import WriteError

from utils.utils import listFiles, download, readJson, access_data


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
                "actif": True,
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        interpreter("longitude", fields, mapper),
                        interpreter("latitude", fields, mapper)
                ]}
            } for fields in access_data(download(api['url']), api["data_access"])]


def exo1(collection, *_):
    try:
        collection.delete_many({})
        collection.drop_indexes()
        print("\nLive DB cleaned")
    except Exception as e:
        print("something went wrong...")
        print(e)
        exit()

    try:
        print("\nCreate 2dsphere index for 'geometry' field...")
        result = collection.create_index([("geometry", "2dsphere")])
        print(f"=> index name : {result}")
        
        print("\nCreate text index for 'name' field...")
        result = collection.create_index([("nom", "text")])
        print(f"=> index name : {result}")
    except Exception as e:
        print("something went wrong...")
        print(e)
        exit()

    print("\nCollect static api's datas...")
    datas = []
    for file in listFiles("apis"):
        datas += insert_from_api(file)

    print("Collect done - uploading...")
    try:
        result = collection.insert_many(datas)
        print(f"=> inserted {len(result.inserted_ids)}/{len(datas)} lines")

    except WriteError as we:
        print(we.details)

    except Exception as e:
        print("something went wrong...")
        print(type(e))
        print(e)
