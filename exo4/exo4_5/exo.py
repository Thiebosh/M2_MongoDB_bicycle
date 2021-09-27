def searchByStats(collection_live, collection_history, compare, ratio, begin_hour, begin_minutes, end_hour, end_minutes,
                  begin_week, end_week):
    begin_week += 1
    end_week += 1

    # TODO :
    begin_hour = 1

    days_range = list(range(begin_week, end_week + 1))
    hour_range = list(range(begin_hour, end_hour + 1))

    aggregation = [
        {
            "$group":
                {
                    "_id": {"station": "$station_id",
                            "dayOfWeek": {"$dayOfWeek": "$record_timestamp"},
                            "hourOfDay": {"$hour": "$record_timestamp"}},
                    "bike_available_avg": {"$avg": "$nbvelosdispo"},
                    "stand_available_avg": {"$avg": "$nbplacesdispo"}
                }

        },
        {
            "$match": {
                "_id.dayOfWeek": {
                    "$in":
                        days_range
                },
                "_id.hourOfDay": {
                    "$in":
                        hour_range
                }
            }
        },
        {
            "$project": {
                "ratio": {
                    "$let": {
                        "vars": {
                            "result": {
                                "$sum": ["$bike_available_avg", "$stand_available_avg"]
                            }
                        },
                        "in": {
                            "$cond": {
                                "if": {
                                    "$ne": ["$$result", 0]
                                },
                                "then": {
                                    "$multiply": [{
                                        "$divide": [
                                            "$bike_available_avg", "$$result"
                                        ]}, 100]
                                },
                                "else": 0
                            }
                        },
                    },
                }
            }
        },
        {
            "$match": {
                "ratio": {
                    compare:
                        ratio
                }
            }
        }
    ]

    return collection_history.aggregate(aggregation)
