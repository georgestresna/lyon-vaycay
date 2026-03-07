from urllib.parse import urlencode

def get_deeplink_booking(city_name, dest_id, checkin_date, checkout_date):
    url = "https://www.booking.com/searchresults.html"
    params = {
        "ss": city_name,
        "dest_id": dest_id,
        "dest_type": "city",
        "checkin": checkin_date,
        "checkout": checkout_date,
        "group_adults": 1,
        "no_rooms": 1,
        "group_children": 0,
        "order": "price" # lowest first
    }
    return f"{url}?{urlencode(params)}"

paris_id = "-1456928"
print(get_deeplink_booking("Paris, France", paris_id, "2026-03-06", "2026-03-08"))
