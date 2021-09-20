from pymongo.errors import WriteError
from os import listdir

from utils.utils import download
from utils.utils import readJson
from utils.utils import interpreter


def get_from_api(path):
    api = readJson(path)

    print(f"starting {api['fields_mapper']['ville']}...")

    accessed = download(api['url'])
    for key in api["data_access"]:
        if not type(key) == dict:
            accessed = accessed[key]

        elif "lambda" in key:
            ldic = locals()
            exec(key["lambda"].replace("{}", "accessed"), globals(), ldic)
            accessed = ldic["accessed"]

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
            } for fields in accessed]


def exo1(collection, *_):
    collection.delete_many({})
    print("\nLive DB cleaned")

    print("create geo index for 'geometry' field...")
    result = collection.create_index([("geometry", "2dsphere")])
    print(f"=> index name : {result}")

    print("\nCollect static api's datas...")
    datas = []
    for file in listdir("apis"):
        datas += get_from_api(f"apis/{file}")

    print("Collect done - uploading...")
    try:
        result = collection.insert_many(datas)
        print(f"=> inserted {len(result.inserted_ids)}/{len(datas)} lines")

    except WriteError as we:
        print(we.details)

    except Exception as e:
        print("something went wrong...")
        print(e)
