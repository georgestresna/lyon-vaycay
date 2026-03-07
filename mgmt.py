import json

with open("trips.json", "r") as file:
    data = json.load(file)

###

def score_trips(data):

    for i in range(len(data[0])):
        storing_price = []
        storing_time = []
        for j in range(len(data)):
            all_c2c_data = data[j][i]

            for row in all_c2c_data:
                for combo in row:
                    storing_price.append(combo["price"])
                    storing_time.append(combo["time_in"])

        if storing_price and storing_time:
            scoring_obj = {
                "p_max": max(storing_price),
                "p_min": min(storing_price),
                "t_max": max(storing_time),
                "t_min": min(storing_time)
            }
        else:
            scoring_obj = {"p_max": 0, "p_min": 0, "t_max": 0, "t_min": 0}

        for j in range(len(data)):
            all_c2c_data = data[j][i]

            for row in all_c2c_data:
                for combo in row:
                    combo["price_score"] = scoring_formula_price(scoring_obj["p_min"], scoring_obj["p_max"], combo["price"])
                    combo["time_score"] = scoring_formula_time(scoring_obj["t_min"], scoring_obj["t_max"], combo["time_in"])
    
    return data
        

def scoring_formula_price(min, max, curr):
    return (max - curr) / (max - min)
def scoring_formula_time(min, max, curr):
    return (curr - min) / (max - min)

data = score_trips(data)
with open("trips_rated.json", "w") as file:
        json.dump(data, file, indent=4)
