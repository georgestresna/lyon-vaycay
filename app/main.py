import json
import os

from app.flixbus import get_deeplink_flix
from app.time_mngmt import next4weekends, timedif, final_dates
from app.find_id import find_flixbus_uuid
# from db import setup_cities_data
from app.mgmt import scoring_formula_price, scoring_formula_time
from app.scrapping_logic import init_driver, trip_details

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
CITIES_FILE = os.path.join(PROJECT_ROOT, "json_files", "cities.json")
TRIPS_FILE = os.path.join(PROJECT_ROOT, "json_files", "trips_rated.json")

def compile_trips(driver, weekends, cities_info, departure_city):
    indicator_dic =[]
    for weekend in weekends:
        print("[~] Iteration through weekend")
        city_travel = []
        for city_ind in range(1, len(cities_info)):
            link_1 = get_deeplink_flix(departure_city["city_uuid"], cities_info[city_ind]["city_uuid"], weekend["begin"])
            link_2 = get_deeplink_flix(cities_info[city_ind]["city_uuid"], departure_city["city_uuid"], weekend["end"])

            departure_list = trip_details(driver=driver, url=link_1)
            comeback_list = trip_details(driver=driver, url=link_2)
            print("     [~]Iteration through city")

            combos=[]
            #fac matricea
            for i in range(len(departure_list)):
                row =[]
                for j in range(len(comeback_list)):
                    # pret calatorie + timp in vacanta, 
                    # pentru a calcula care sunt cele mai bune variante
                    date1, date2 = final_dates(weekend=weekend, departure_list=departure_list, comeback_list=comeback_list, i=i, j=j)
                    temp = {
                        "price": round(departure_list[i]["price"] + comeback_list[j]["price"], 2),
                        "time_in": timedif(date1, date2),
                        "price_score": 0,
                        "time_score": 0,
                        "departure time": date1.strftime("%Y-%m-%d %H:%M:%S"),
                        "arrival_time": date2.strftime("%Y-%m-%d %H:%M:%S"),
                        "travel_location": cities_info[city_ind]["city_name"]
                    }

                    row.append(temp)
                combos.append(row)
            city_travel.append(combos)
        indicator_dic.append(city_travel)
    return indicator_dic

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

def __init__():
    driver = init_driver()
    print("[*] Started driver")

    # link logic
    weekends = next4weekends()
    print("[*] Calculated weekends")
    
    ####
    # my_col = setup_cities_data()
    # cities_info = list(my_col.find())
    with open(CITIES_FILE, "r") as file:
        cities_info = json.load(file)
    departure_city = cities_info[0]
    print("[*] Departure city set")

    # all_data[week_nr][dest_city][ind_lyon][ind_dest]
    trips = compile_trips(driver, weekends, cities_info, departure_city)
    print("[*] Compiled the raw scrapped data")

    trips_rated = score_trips(trips)
    print("[*] Scored trips | Final version of data")

    with open(TRIPS_FILE, "w") as file:
        json.dump(trips_rated, file, indent=4)
    print("[*] Saved final data to JSON")

    driver.quit()

__init__()
