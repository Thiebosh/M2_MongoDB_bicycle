from pprint import pprint

def exo3(collection, _, coordinates, minDistance, maxDistance, closest, *__):
    print("print some data")
    # filter = {
    #     "geometry": { 
    #         "$near": {
    #             "$geometry": {
    #                 "type": 'Point',
    #                 "coordinates": coordinates
    #             },
    #             "$minDistance": minDistance,
    #             "$maxDistance": maxDistance,
    #             "distanceField": "distance"
    #         },
    #     },
    #     "nbvelosdispo": {
    #         "$gt": 0
    #     }
    # }
    projection = {
        "_id": 0,
        "nom": 1,
        "nbvelosdispo": 1,
        "nbplacesdispo": 1
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

    query = collection.aggregate(aggregation)

    try:
        for element in query:
            pprint(element)
    except Exception as e:
        print("something went wrong...")
        print(type(e))
        print(e)
