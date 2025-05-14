import json
import requests


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
location = input("Где вы находитесь? ")
coords = fetch_coordinates(apikey, location)
print(f"Ваши координаты: {coords}")


# for coffee_shop_name in coffee_list:
#     print(
#         f"""{coffee_shop_name['Name']}
# {coffee_shop_name['geoData']['coordinates'][1]} \
# {coffee_shop_name['geoData']['coordinates'][0]}"""
#     )
