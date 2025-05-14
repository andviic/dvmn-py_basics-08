import json
import requests
from geopy import distance
from pprint import pprint


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(
        base_url,
        params={
            "geocode": address,
            "apikey": apikey,
            "format": "json",
        },
    )
    response.raise_for_status()
    found_places = response.json()["response"]["GeoObjectCollection"]["featureMember"]

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant["GeoObject"]["Point"]["pos"].split(" ")
    return lon, lat


with open("coffee.json", "r", encoding="CP1251") as coffee:
    coffee_contents = coffee.read()

coffee_list = json.loads(coffee_contents)

apikey = "9b2793be-1d14-4c36-aa34-18b7975af9a0"
location_1 = input("Где вы находитесь? ")

coords = fetch_coordinates(apikey, location_1)
print(f"Ваши координаты: {coords}")

radius = 1
сoffee_nearby_list = []

for coffee_shop in coffee_list:
    dist = distance.distance(coords, coffee_shop["geoData"]["coordinates"]).km
    coffee_nearby = {
        "title": coffee_shop["Name"],
        "distance": dist,
        "latitude": coffee_shop["geoData"]["coordinates"][1],
        "longitude": coffee_shop["geoData"]["coordinates"][0],
    }

    if dist <= radius:
        сoffee_nearby_list.append(coffee_nearby)

pprint(сoffee_nearby_list, sort_dicts=False)
