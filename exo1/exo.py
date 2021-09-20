from requests import request
import json
from pymongo.errors import WriteError


def dowload(url):
    return json.loads(request("GET", url).text.encode("utf8"))

def get_lyon():
    url = "https://transport.data.gouv.fr/gbfs/lyon/station_information.json"

    filteredFields = [{
        "_id": f"Lyon{fields['station_id']}",
        "ville": "Lyon",
        "nom": fields["name"],
        "nbvelosdispo": 0,
        "nbplacesdispo": 0,
        "nbplacestotal": fields["capacity"],
        "geometry": {"type": "Point", "coordinates": [fields['lon'], fields['lat']]}
    } for fields in dowload(url)["data"]["stations"]]

    filteredFields.sort(key=lambda x: x["_id"])

    return filteredFields


def get_montpellier():
    url = "https://data.opendatasoft.com/api/records/1.0/search/?dataset=disponibilite-des-places-velomagg-en-temps" \
          "-reel%40occitanie&q=&rows=100 "

    allFields = [record["fields"] for record in dowload(url)["records"]]

    filteredFields = [{
        "_id": f"Montpellier_{fields['id']}",
        "ville": "Montpellier",
        "nom": fields["na"],
        "nbvelosdispo": 0,
        "nbplacesdispo": 0,
        "nbplacestotal": fields["to"],
        "geometry": {"type": "Point", "coordinates": [fields['lg'], fields['la']]}
    } for fields in allFields]

    filteredFields.sort(key=lambda x: x["_id"])

    return filteredFields


def get_lille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=400"

    allFields = [{**record["fields"], "geometry": record["geometry"]} for record in dowload(url)["records"]]

    filteredFields = [{"_id": f"Lille_{fields['libelle']}",
                       "ville": "Lille",
                       "nom": fields["nom"],
                       "nbvelosdispo": 0,
                       "nbplacesdispo": 0,
                       "nbplacestotal": fields["nbvelosdispo"] + fields["nbplacesdispo"],
                       "cb": int(fields["type"] == "AVEC TPE"),
                       "geometry": fields["geometry"]} for fields in allFields]

    filteredFields.sort(key=lambda x: x["_id"])

    return filteredFields


def exo1(collection, *_):
    collection.delete_many({})
    print("live DB cleaned")

    print("create geo index for 'geometry' field...")
    result = collection.create_index([("geometry", "2dsphere")])
    print(f"=> index name : {result}")

    print("\n\n")

    print("collect static api's datas...")
    datas = get_lille()
    print("Lille done")

    datas += get_lyon()
    print("Lyon done")

    datas += get_montpellier()
    print("Montpellier done")

    try:
        result = collection.insert_many(datas)
        print(f"=> inserted {len(result.inserted_ids)}/{len(datas)} lines")

    except WriteError as we:
        print(we.details)

    except Exception as e:
        print("something went wrong...")
        print(e)
