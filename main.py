import datetime as dt
import requests
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request
from flask_frozen import Freezer

load_dotenv('.env')
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast?"
API_KEY = os.getenv('API_KEY')
app = Flask(__name__)
freezer = Freezer(app)

# back end
def kelToCF(kelvin):
    cels = kelvin - 273.15
    fah = cels * (9 / 5) + 32
    return cels, fah

def valid_city(city):
    url = f"{BASE_URL}q={city}&appid={API_KEY}"
    response = requests.get(url).json()
    if response['cod'] == '404':
        return False
    else:
        return True

def weather(city):
    url = f"{BASE_URL}q={city}&appid={API_KEY}"
    
    # prettyResponse = json.dumps(requests.get(url).json(), indent=4)
    response = requests.get(url).json()
    
    temp_kelvin = response['list'][0]['main']['temp']
    temp_cel, temp_fah = kelToCF(temp_kelvin)

    feels_k = response['list'][0]['main']['feels_like']
    feels_c, feels_f = kelToCF(feels_k)

    humidity = response['list'][0]['main']['humidity']

    desc = response['list'][0]['weather'][0]['description']

    sunrise = dt.datetime.utcfromtimestamp(response['city']['sunrise'] + response['city']['timezone'])
    sunset = dt.datetime.utcfromtimestamp(response['city']['sunset'] + response['city']['timezone'])

    wind_spd = response['list'][0]['wind']['speed']

    # print(f"Temperature in {CITY}: {temp_cel:.2f}°C or {temp_fah:.2f}°F")
    # print(f"Temperature in {CITY}: feels like: {feels_c:.2f}°C or feels like: {feels_f:.2f}°F")
    # print(f"Humidity in {CITY}: {humidity}%")
    # print(f"Wind Speed in {CITY}: {wind_spd}m/s")
    # print(f"General Weather Description in {CITY}: {desc}")
    # print(f"Sun rises in {CITY} at {sunrise} local time")
    # print(f"Sun sets in {CITY} at {sunset} local time")

    return city, temp_cel, temp_fah, desc, sunrise, sunset

# front end logic
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['input']
        if valid_city(city):
            city, tempC, tempF, dsc, sunr, suns = weather(city)
            tempC_format = f"{tempC:.2f}"
            tempF_format = f"{tempF:.2f}"
            return render_template("index.html", city=city, tempC=tempC_format, tempF=tempF_format, dsc=dsc, sunr=sunr, suns=suns)
        else:
            return render_template("index.html", error="City Not Found.")
    else:
        return render_template("index.html", city="", tempC="", tempF="", dsc="", sunr="", suns="")

if __name__ == '__main__':
    freezer.freeze()
    app.run(host="0.0.0.0", port=80)