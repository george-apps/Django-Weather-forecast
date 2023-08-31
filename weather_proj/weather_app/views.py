from datetime import datetime
import requests
from django.shortcuts import render
from dotenv import load_dotenv
import os


def config():
    load_dotenv()


def index(request):
    config()
    api_key=os.getenv('api_key')

    curr_weather_url='https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_weather_url='https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&units=metric&appid={}'

    if request.method == 'POST':
        city=request.POST['city']

        weather_data,daily_forecast=get_weather_forecast(city,api_key,curr_weather_url,forecast_weather_url)

        context = {
            'weather_data': weather_data,
            'daily_forecast':daily_forecast,

        }
        return render(request,'weather_app/index.html',context)

    else:

        return render(request,'weather_app/index.html')


def get_weather_forecast(city,api_key,curr_weather_url,forecast_weather_url):

    response=requests.get(curr_weather_url.format(city,api_key)).json()

    lat,lon=response['coord']['lat'],response['coord']['lon']

    forecast_response=requests.get(forecast_weather_url.format(lat,lon,api_key)).json()

    weather_data={
        'city':city,
        'temperature': round(response['main']['temp'] - 273.15,2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon']
    }

    daily_forecasts=[]

    for forecast_data in forecast_response['list'][:5]:
        daily_forecasts.append({
            'day':datetime.fromtimestamp(forecast_data['dt']).strftime('%A'),
            'day_time':datetime.fromisoformat(forecast_data['dt_txt']).strftime('%R'),
            'min_temp': round(forecast_data['main']['temp_min'],2),
            'max_temp': round(forecast_data['main']['temp_max'],2),
            'description': forecast_data['weather'][0]['description'],
            'icon': forecast_data['weather'][0]['icon'],
        })

    return weather_data, daily_forecasts
