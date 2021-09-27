def searchByStats(collection_live, collection_history, compare, ratio, begin_hour, begin_minutes, end_hour, end_minutes,
                  begin_week, end_week):

    begin_week += 1
    end_week += 1
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
                "dayOfWeek": {
                    "$in": {
                        list(range(begin_week, end_week + 1))
                    }
                }
            }
        },
    ]
    print("start")
    print(list(collection_history.aggregate(aggregation)))
    print("end")

    # print(compare)
    # print(ratio)
    # print(begin_hour)
    # print(begin_minutes)
    # print(end_hour)
    # print(end_minutes)
    # print(begin_week)
    # print(end_week)

    return []
