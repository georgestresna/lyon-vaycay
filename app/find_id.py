import re
from pymongo import MongoClient

def find_flixbus_uuid(link):
    link_pieces = re.split(r'[?&]', link)

    departure_uuid = re.split(r'[=]',link_pieces[1])[1]
    arrival_uuid = re.split(r'[=]',link_pieces[2])[1]
    route = re.split(r'[=-]',link_pieces[3])[1:3]

    client = MongoClient('localhost', 27017)
    db = client['busScraper']
    mycol = db["cities"]

    cities = [
    {
        "city_name": route[0],
        "city_uuid": departure_uuid
    },
    {
        "city_name": route[1],
        "city_uuid": arrival_uuid
    }
    ]

    for city in cities:
        found_city = mycol.find({"city_name": city["city_name"]})
        if not len(list(found_city)):
            mycol.insert_one(city)
            print("[*] Locatie noua adaugata")


def find_booking_id(link):
    link_pieces = re.split(r'[%=&]', link)
    for i in range(len(link_pieces)):
        if link_pieces[i] == "dest_id":
            city ={
                "city_name": link_pieces[1],
                "city_booking_id": link_pieces[i+1]
            }
            break
    print(city)

    if city["city_name"] == "Geneva":
        city["city_name"] = "Gen%C3%A8ve"
    elif city["city_name"] == "Barcelona":
        city["city_name"] = "Barcelone"
    elif city["city_name"] == "Chamb":
        city["city_name"] = "Chamb%C3%A9ry"

    client = MongoClient('localhost', 27017)
    db = client['busScraper']
    mycol = db["cities"]

    found_city = mycol.find({"city_name": city["city_name"]})
    if len(list(found_city)) == 1:
        mycol.update_one({"city_name": city["city_name"]}, {"$set" : {"booking_id": city["city_booking_id"]}})
        print("[*] Locatie noua updatata")

# while 1:
#     print("Baga link:")
#     link = input()
#     find_flixbus_uuid(link)
#     print("Iar? (1, else 0)")
#     confirm =input()
#     if not confirm:
#         break

# find_booking_id(f'''
# https://www.booking.com/searchresults.html?ss=Chamb%C3%A9ry%2C+Rh%C3%B4ne-Alps%2C+France&ssne=Geneva&ssne_untouched=Geneva&label=gen173nr-10CAEoggI46AdIDVgEaE2IAQGYATO4ARfIAQzYAQPoAQH4AQGIAgGoAgG4ApiBoM0GwAIB0gIkZDg1MjZjNjktMDMwOS00MGFiLWI5YmItZjk1NDU0ODVjNjU12AIB4AIB&sid=c2bcd6000fd7d186c61c2760e278b38a&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-1417924&dest_type=city&ac_position=1&ac_click_type=b&ac_langcode=xu&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=fed64748507a073f&ac_meta=GhBmZWQ2NDc0ODUwN2EwNzNmIAEoATICeHU6BGNoYW0%3D&checkin=2026-03-06&checkout=2026-03-08&group_adults=2&no_rooms=1&group_children=0
#  ''')