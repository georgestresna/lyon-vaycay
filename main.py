import os
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

from datetime import datetime, date

from flixbus import get_deeplink_flix
from time_mngmt import next4weekends, str2hour, plus1day, weekend_str2date, timedif, final_dates
from find_id import find_flixbus_uuid
from db import setup_cities_data
from mgmt import score_trips

def init_driver():
    options = Options()
    # options.add_argument("--headless") # Commented out for visual debugging
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    # options.add_argument("--window-size=1920,1080")
    # Avoid detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    return driver

def trip_details(driver, url):

    wait = WebDriverWait(driver, 5)
    driver.get(url)
    wait.until(EC.element_to_be_clickable(driver.find_element(By.TAG_NAME, 'body')))
    time.sleep(3)

    listings_today = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[1]/div[2]/div/figure[1]/ul').find_elements(By.TAG_NAME, 'li')
    # listings_tomorrow = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[1]/div[2]/div/figure[2]/ul').find_elements(By.TAG_NAME, 'li')
    # de implementat mai tarziu si pentru cele peste miezu noptii

    departure_list=[]

    for listing in listings_today:
        departure_hour = listing.find_element(By.XPATH, ".//div[2]/div[1]/div/div/div[1]/div/div[1]/span[2]").get_attribute('innerHTML')
        destination_hour = listing.find_element(By.XPATH, ".//div[2]/div[1]/div/div/div[2]/div/span/span[2]").get_attribute('innerHTML')
        duration_raw = listing.find_element(By.XPATH, ".//div[2]/div[1]/div/div/div[1]/div/div[2]/div/span[2]").get_attribute('innerHTML')
        price_raw = listing.find_element(By.XPATH, ".//div[2]/div[1]/button/span/div/span").get_attribute('innerHTML')
        price_pieces = re.split(r'[<,>]',price_raw)

        price = int(price_pieces[0]) + int(price_pieces[3])/100
        duration = re.split( r'[ ]', duration_raw.strip())[0]
        departure_hour = str2hour(departure_hour)
        destination_hour = str2hour(destination_hour)

        trip_data = {
            "departure": departure_hour,
            "arrival": destination_hour,
            "price": price,
            "duration": duration,
            "next_day_arr": bool(destination_hour < departure_hour)
        }

        departure_list.append(trip_data)
    
    return departure_list



# body = driver.page_source
# with open("soup.html", 'w') as f:
#     f.write(body)

def __init__():
    driver = init_driver()
    wait = WebDriverWait(driver, 5)
    print("[*] Started driver")

    # link logic
    weekends = next4weekends()
    print("[*] Calculated weekends")
    
    ####
    my_col = setup_cities_data()
    cities_info = list(my_col.find())
    departure_city = cities_info[0]
    print("[*] Departure city set")

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

        # print(indicator_dic)
    ####

    with open("trips.json", "w") as file:
        json.dump(indicator_dic, file, indent=4)

    return
    data = score_trips(indicator_dic)

    with open('trips.json', 'r') as file:
        loaded_matrix = json.load(file)

    num_weeks = len(weekends)
    num_cities = len(cities_info)
    # indicator_dic[week_index][city_index][combo_index]
    city_baseline = []
    for i in range(num_cities):
        for j in range(num_weeks):
            general_route = []
            for combo in indicator_dic[j][i]:
                route_data={
                    "price": combo["price"],
                    "time_in":combo["time_in"]
                }
                general_route.append(route_data)
            
            ###
        city_baseline.append({
            "p_min": min(general_route["price"]),
            "p_max": max(general_route["price"]),
            "t_min": min(general_route["time_in"]),
            "t_max": max(general_route["time_in"])
        })

    ###


    return

    driver.quit()

__init__()
# url="https://shop.flixbus.fr/search?departureCity=40df89c1-8646-11e6-9066-549f350fcb0c&arrivalCity=40e13a46-8646-11e6-9066-549f350fcb0c&route=Lyon-Nice&rideDate=10.03.2026&adult=1&_locale=fr&departureCountryCode=FR&arrivalCountryCode=FR&features%5Bfeature.enable_distribusion%5D=1&features%5Bfeature.train_cities_only%5D=0&features%5Bfeature.station_search%5D=0&features%5Bfeature.station_search_recommendation%5D=0&features%5Bfeature.darken_page%5D=1"
# trip_details(init_driver(), url)
