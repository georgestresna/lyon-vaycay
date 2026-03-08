
def to_display(data):
    best_trips = []
    for i in range(len(data[0])):
        best_trip_for_city_coord = {
            "city": i,
            "week": None,
            "k_ind": None,
            "l_ind": None
        }
        current_best_score = -1
        for j in range(len(data)):
            all_c2c_data = data[j][i]

            for k in range(len(all_c2c_data)):
                for l in range(len(all_c2c_data[k])):
                    score = do_score(all_c2c_data[k][l]["price_score"], all_c2c_data[k][l]["time_score"])
                    if score > current_best_score:
                        current_best_score = score
                        best_trip_for_city_coord["week"] = j
                        best_trip_for_city_coord["k_ind"] = k
                        best_trip_for_city_coord["l_ind"] = l

        best_trips.append(best_trip_for_city_coord)

    return best_trips

def do_score(price, time):
    return float('%.4f'%((price * 0.5) + (time * 0.5)))

def final_data(data, trimmed):
    best_trip_details = []
    for trip in trimmed:
        best_trip_details.append(data[trip["week"]][trip["city"]][trip["k_ind"]][trip["l_ind"]])
    return best_trip_details

