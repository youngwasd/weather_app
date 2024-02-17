import datetime as dt
import requests

BASE_URL = "http://api.openweathermap.org/data/2.5/forecast?"
API_KEY = ""
CITY = input("Enter city: ")

def kelToCF(kelvin):
    cels = kelvin - 273.15
    fah = cels * (9 / 5) + 32
    return cels, fah

url = BASE_URL + "q=" + CITY + "&appid=" + API_KEY

#prettyResponse = json.dumps(requests.get(url).json(), indent=4)
response = requests.get(url).json()

if response['cod'] == '404':
    print("No City Found.")
else:
    # stupid = json.dumps(response['list'][0]['wind']['speed'], indent=4)
    # print(stupid)

    temp_kelvin = response['list'][0]['main']['temp']
    temp_cel, temp_fah = kelToCF(temp_kelvin)

    feels_k = response['list'][0]['main']['feels_like']
    feels_c, feels_f = kelToCF(feels_k)

    humidity = response['list'][0]['main']['humidity']

    desc = response['list'][0]['weather'][0]['description']

    sunrise = dt.datetime.utcfromtimestamp(response['city']['sunrise'] + response['city']['timezone'])
    sunset = dt.datetime.utcfromtimestamp(response['city']['sunset'] + response['city']['timezone'])

    wind_spd = response['list'][0]['wind']['speed']

    print(f"Temperature in {CITY}: {temp_cel:.2f}°C or {temp_fah:.2f}°F")
    print(f"Temperature in {CITY}: feels like: {feels_c:.2f}°C or feels like: {feels_f:.2f}°F")
    print(f"Humidity in {CITY}: {humidity}%")
    print(f"Wind Speed in {CITY}: {wind_spd}m/s")
    print(f"General Weather Description in {CITY}: {desc}")
    print(f"Sun rises in {CITY} at {sunrise} local time")
    print(f"Sun sets in {CITY} at {sunset} local time")