import json
import requests
from dotenv import load_dotenv
import os
from geopy import distance
import folium


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
    return lat, lon


def get_distance(coffee):
    return coffee["distance"]


def get_coffee_nearby(col, coffee_shops, coords):
    сoffee_shops_list = []
    for coffee_shop in coffee_shops:
        lat = coffee_shop["geoData"]["coordinates"][1]
        lon = coffee_shop["geoData"]["coordinates"][0]
        dist = distance.distance(coords, (lat, lon)).km
        сoffee_shops_list.append(
            {
                "title": coffee_shop["Name"],
                "distance": dist,
                "latitude": lat,
                "longitude": lon,
            }
        )
    сoffee_shops_nearby = sorted(сoffee_shops_list, key=get_distance)[:col]
    return сoffee_shops_nearby


def get_coffee_on_map(сoffee_shops_nearby, coords):
    map = folium.Map(location=coords, zoom_start=15)
    folium.Marker(
        location=coords,
        tooltip="Я здесь!",
        icon=folium.Icon(icon="person", prefix="fa", color="red"),
    ).add_to(map)

    for сoffee_shop in сoffee_shops_nearby:
        folium.Marker(
            location=[сoffee_shop["latitude"], сoffee_shop["longitude"]],
            tooltip=сoffee_shop["title"],
            icon=folium.Icon(icon="mug-hot", prefix="fa", color="green"),
        ).add_to(map)

    return map.save("index.html")


def main():
    location = input("Где вы находитесь? ")

    with open("coffee.json", "r", encoding="CP1251") as coffee:
        coffee_contents = coffee.read()
    coffee_shops = json.loads(coffee_contents)

    load_dotenv()
    apikey = os.getenv("API_KEY")
    coords = fetch_coordinates(apikey, location)
    сoffee_shops_nearby = get_coffee_nearby(5, coffee_shops, coords)

    get_coffee_on_map(сoffee_shops_nearby, coords)


if __name__ == "__main__":
    main()
