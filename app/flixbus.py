
def get_deeplink_flix(departure_uuid, arrival_uuid, date_string):
    url = f"https://shop.flixbus.fr/search?departureCity={departure_uuid}&arrivalCity={arrival_uuid}&rideDate={date_string}&adult=1"
    return url