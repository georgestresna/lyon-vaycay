from bs4 import BeautifulSoup
import urllib.request

url = 'https://shop.flixbus.fr/search?departureCity=40df89c1-8646-11e6-9066-549f350fcb0c&arrivalCity=40de8964-8646-11e6-9066-549f350fcb0c&route=Lyon-Paris&rideDate=20.03.2026&adult=1&_locale=fr&departureCountryCode=FR&arrivalCountryCode=FR&features%5Bfeature.enable_distribusion%5D=1&features%5Bfeature.train_cities_only%5D=0&features%5Bfeature.station_search%5D=0&features%5Bfeature.station_search_recommendation%5D=0&features%5Bfeature.darken_page%5D=1'
html_page = urllib.request.urlopen(url=url)
soup = BeautifulSoup(html_page, "html.parser")

with open("soup.html", 'w') as f:
    f.write(str(soup))