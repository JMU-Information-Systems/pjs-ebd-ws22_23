from app import app, get_weekday
from flask_login import login_required
from pathlib import Path
import os
import json
from datetime import datetime
from flask import render_template

@app.route('/weather')
@login_required
def weather():
    with open(os.path.join(Path(app.root_path).parent.absolute(), 'streaming_data_platform/data.json'), mode='r', encoding='utf-8') as openfile:
        data = json.load(openfile)
    timestamp = []
    clouds = []
    rain = []
    speed = []
    sunrise = []
    sunset = []
    feel_temp = []
    temps = []
    weather = []
    weather_code = []
    pressure = []
    humidity = []
    night = []
    wochentag = []
    records = data['cnt']
    name = data['city']['name']
    for day in data['list']:
        timestamp.append(datetime.utcfromtimestamp(day['dt']).strftime("%d.%m.%Y"))
        temps.append(round(day['temp']['max'], 1))
        weather.append(day['weather'][0]['description'])
        weather_code.append(day['weather'][0]['id'])
        pressure.append(day['pressure'])
        humidity.append(day['humidity'])
        clouds.append(day['clouds'])
        night.append(round(day['temp']['min'], 1))
        wochentag.append(get_weekday(datetime.utcfromtimestamp(day['dt']).strftime("%w")))
        if 'rain' in day:
            rain.append(day['rain'])
        else:
            rain.append(0)
        speed.append(day['speed'])
        sunrise.append(datetime.utcfromtimestamp(day['sunrise']).strftime("%H:%M"))
        sunset.append(datetime.utcfromtimestamp(day['sunset']).strftime("%H:%M"))
        feel_temp.append(round(day['feels_like']['day'], 1))
    informations = {
        'Tag': timestamp,
        'Sonnenaufgang': sunrise,
        'Sonnenuntergang': sunset,
        'Temp': temps,
        'Wetter': weather,
        'Wettercode': weather_code,
        'Druck': pressure,
        'Feuchtigkeit': humidity,
        'Wolken': clouds,
        'Regen': rain,
        'Wind': speed,
        'Feelslike': feel_temp,
        'Nacht': night,
        'Wochentag': wochentag
    }
    return render_template('/pages/weather.html', records=records, informations=informations, cityname=name)