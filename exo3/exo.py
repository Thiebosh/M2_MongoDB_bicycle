from guizero import App, Box, Text, PushButton, ListBox

from utils.utils import formGenerator


def getClosestStations(collection, coordinates, minDistance, maxDistance, closest):
    # filter = {
    #     "geometry": { 
    #         "$near": {
    #             "$geometry": {
    #                 "type": 'Point',
    #                 "coordinates": coordinates
    #             },
    #             "$minDistance": minDistance,
    #             "$maxDistance": maxDistance
    #         },
    #     },
    #     "nbvelosdispo": {
    #         "$gt": 0
    #     }
    # }
    projection = {
        "_id": 0,
        "nom": 1,
        "velos": "$nbvelosdispo",
        "places": "$nbplacesdispo"
    }

    # query = collection.find(filter, projection).limit(closest)

    aggregation = [
        {
            "$geoNear": {
                "near": {
                    "type": "Point",
                    "coordinates": coordinates
                }, 
                "minDistance": minDistance,
                "maxDistance": maxDistance,
                "distanceField": "distance"
            }
        },
        {
            "$match": {
                "nbvelosdispo": {
                    "$gt": 0
                }
            }
        },
        {
            "$project": {
                **projection,
                "distance": {
                    "$concat": [
                        {
                            "$substr": [
                                {
                                    "$round": ["$distance", 2]
                                },
                                0,
                                -1
                            ]
                        },
                        " mètres"
                    ]
                },
                "direction": {
                    "$let": {
                        "vars": {
                            "lon": {
                                "$arrayElemAt": ["$geometry.coordinates", 0]
                            },
                            "lat": {
                                "$arrayElemAt": ["$geometry.coordinates", 1]
                            }
                        },
                        "in": {
                            "$concat": [
                                {
                                    "$cond": {
                                        "if": {
                                            "$eq": ["$$lat", coordinates[1]]
                                        },
                                        "then": "",
                                        "else": {
                                            "$cond": {
                                                "if": {
                                                    "$gt": ["$$lat", coordinates[1]]
                                                },
                                                "then": "Nord ",
                                                "else": "Sud "
                                            }
                                        }
                                    }
                                },
                                {
                                    "$cond": {
                                        "if": {
                                            "$eq": ["$$lon", coordinates[0]]
                                        },
                                        "then": "",
                                        "else": {
                                            "$cond": {
                                                "if": {
                                                    "$lt": ["$$lon", coordinates[0]]
                                                },
                                                "then": "Ouest",
                                                "else": "Est"
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        },
        {
            "$facet": {
                "closest_results": [
                    { 
                        "$limit": closest
                    }
                ],
                "total": [
                    {
                        "$count": 'nb_stations'
                    }
                ]
            }
        },
        {
            "$unwind": "$total"
        },
        {
            "$project": {
                "closest_results": 1,
                "nb_stations":  "$total.nb_stations"
            }
        }
    ]

    return collection.aggregate(aggregation)


def exo3(collection, *_):
    try:
        app = App(title="Client", height="600", width="800")
        app.tk.resizable(False, False)  # everything will be absolutely relative

        Box(app, height="10")  # margin

        Text(app, text="Recherche de station")

        Box(app, height="25")  # margin

        inputs = {
            "lat": {
                "text": "Latitude",
                "value": 3.0485
            },
            "lon": {
                "text": "Longitude",
                "value": 50.6342
            },
            "minDist": {
                "text": "Distance min",
                "value": 0
            },
            "maxDist": {
                "text": "Distance max",
                "value": 400
            },
            "limit": {
                "text": "Affichage max",
                "value": 3
            }
        }
        formGenerator(app, inputs)

        Box(app, height="40")  # margin

        resultList = ListBox(app, align="bottom", width="fill", scrollbar=True)
        box = Box(app, align="bottom", width="fill")
        Text(box, align="left", text="Nb de stations totales : ")
        resultNb = Text(box, align="left")

        PushButton(app, text="Rechercher", width="16", command=displayStations, args=(collection, inputs, resultList, resultNb))

        app.display()
    except Exception as e:
        print(e)


def displayStations(collection, inputs, containerList, containerNb):
    containerList.clear()
    containerNb.clear()

    try:
        args = ([float(inputs["lat"]["ptr"].value), float(inputs["lon"]["ptr"].value)],
                float(inputs["minDist"]["ptr"].value),
                float(inputs["maxDist"]["ptr"].value),
                int(inputs["limit"]["ptr"].value))

        result = list(getClosestStations(collection, *args))[0]
        for elem in result["closest_results"]:
            containerList.append(f"'{elem['nom']}' est à {elem['distance']} direction {elem['direction']} avec {elem['velos']} vélos dispos et {elem['places']} places libres")

        containerNb.append(result["nb_stations"])

    except IndexError:
        containerNb.append(0)

    except Exception as e:
        print("something went wrong...")
        print(type(e))
        print(e)
