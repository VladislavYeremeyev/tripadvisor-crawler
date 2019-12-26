import json

with open("./reviews.json", "r") as reviews_file:
    reviews_datastore = json.load(reviews_file)
    result = {}

    for review in reviews_datastore:
        stars_amount = review.get("stars_amount")

        if review.get("restaurant_name") in result:
            result_item = result.get(review.get("restaurant_name"))

            result.get(review.get("restaurant_name")).update(
                {
                    "reviews_count": result_item.get("reviews_count") + 1,
                    f"reviews_{stars_amount}_stars_count": result_item.get(
                        f"reviews_{stars_amount}_stars_count"
                    )
                    + 1,
                }
            )
        else:
            result.update(
                {
                    review.get("restaurant_name"): {
                        "reviews_count": 1,
                        "reviews_5_stars_count": 1
                        if review.get("stars_amount") == 5
                        else 0,
                        "reviews_4_stars_count": 1
                        if review.get("stars_amount") == 4
                        else 0,
                        "reviews_3_stars_count": 1
                        if review.get("stars_amount") == 3
                        else 0,
                        "reviews_2_stars_count": 1
                        if review.get("stars_amount") == 2
                        else 0,
                        "reviews_1_stars_count": 1
                        if review.get("stars_amount") == 1
                        else 0,
                    }
                }
            )

    stats = [
        {
            "restaurant_name": key,
            "reviews_count": value.get("reviews_count"),
            "reviews_5_stars_count": value.get("reviews_5_stars_count"),
            "reviews_4_stars_count": value.get("reviews_4_stars_count"),
            "reviews_3_stars_count": value.get("reviews_3_stars_count"),
            "reviews_2_stars_count": value.get("reviews_2_stars_count"),
            "reviews_1_stars_count": value.get("reviews_1_stars_count"),
        }
        for key, value in result.items()
    ]

with open("./stats.json", "w") as fout:
    json.dump(stats, fout, ensure_ascii=False)
