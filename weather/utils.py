from .models import Alert
from datetime import timedelta
from collections import defaultdict
import requests
from datetime import datetime as dt
from .models import WeatherData, Alert, cuties
from random import shuffle, choice

from django.conf import settings
from django.core.mail import send_mail

from datetime import datetime
from django.db.models import Max, Min, Avg
from .models import Weather
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from django import forms


API_KEY = ''
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore',
          'Kolkata', 'Hyderabad']


# def fetch_weather_data():
#     for city in CITIES:
#         url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
#         response = requests.get(url)
#         data = response.json()
#         print(data)
#         store_weather_data(city, data)


def fetch_weather_data():
    extraction_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    today_date = datetime.now().date()
    weather_data_list = []

    for city in CITIES:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        data = response.json()
        icn = data['weather'][0]['icon']
        # Extract weather data
        temp = round(data["main"]["temp"], 2)
        temp_min = round(data["main"]["temp_min"], 2)
        temp_max = round(data["main"]["temp_max"], 2)
        humidity = round(data["main"]["humidity"], 2)
        pressure = round(data["main"]["pressure"], 2)
        visibility = round(data["visibility"], 2)
        latitude = round(data["coord"]["lat"], 2)
        longitude = round(data["coord"]["lon"], 2)
        feels_like = round(data["main"]["feels_like"], 2)
        weather_description = data["weather"][0]["description"]
        wind_speed = round(data["wind"]["speed"], 2)
        rain_1h = round(data.get("rain", {}).get("1h", 0), 2)

        # Aggregate existing data
        existing_data = Weather.objects.filter(city=city, date=today_date).aggregate(
            max_temp=Max('max_temp'),
            min_temp=Min('min_temp'),
            avg_temp=Avg('avg_temp'),
            avg_humidity=Avg('avg_humidity'),
            avg_pressure=Avg('avg_pressure'),
            avg_visibility=Avg('avg_visibility')
        )

        # Handle cases where aggregation results are None
        max_temp_existing = existing_data['max_temp'] or float('-inf')
        min_temp_existing = existing_data['min_temp'] or float('inf')
        avg_temp_existing = existing_data['avg_temp'] or temp
        avg_humidity_existing = existing_data['avg_humidity'] or humidity
        avg_pressure_existing = existing_data['avg_pressure'] or pressure
        avg_visibility_existing = existing_data['avg_visibility'] or visibility

        # Calculate new values
        new_max_temp = round(max(temp_max, max_temp_existing), 2)
        new_min_temp = round(min(temp_min, min_temp_existing), 2)
        new_avg_temp = round((temp + avg_temp_existing) / 2, 2)
        new_avg_humidity = round((humidity + avg_humidity_existing) / 2, 2)
        new_avg_pressure = round((pressure + avg_pressure_existing) / 2, 2)
        new_avg_visibility = round(
            (visibility + avg_visibility_existing) / 2, 2)

        # Update or create weather data entry
        weather, created = Weather.objects.update_or_create(
            city=city,
            date=today_date,
            defaults={
                'latitude': latitude,
                'longitude': longitude,
                'max_temp': new_max_temp,
                'min_temp': new_min_temp,
                'avg_temp': new_avg_temp,
                'avg_humidity': new_avg_humidity,
                'avg_pressure': new_avg_pressure,
                'avg_visibility': new_avg_visibility
            }
        )
        weather.save()

        # Append the updated or created weather data
        weather_data_list.append({
            "city": city,
            "date": today_date,
            "latitude": latitude,
            "longitude": longitude,
            "current_temp": temp,
            "feels_like": feels_like,
            "weather_description": weather_description,
            "wind_speed": wind_speed,
            "rain_1h": rain_1h,
            "visibility": visibility,
            "pressure": pressure,
            "max_temp": weather.max_temp,
            "min_temp": weather.min_temp,
            "avg_temp": weather.avg_temp,
            "avg_humidity": weather.avg_humidity,
            'icon': icn
        })
    check_and_save_alerts(weather_data_list)
    return weather_data_list, extraction_time


def fetch_city(citi):
    extraction_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    today_date = datetime.now().date()
    weather_data_list = []

    for city in citi:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        data = response.json()
        print(data)
        icn = data['weather'][0]['icon']
        # Extract weather data
        temp = round(data["main"]["temp"], 2)
        temp_min = round(data["main"]["temp_min"], 2)
        temp_max = round(data["main"]["temp_max"], 2)
        humidity = round(data["main"]["humidity"], 2)
        pressure = round(data["main"]["pressure"], 2)
        visibility = round(data["visibility"], 2)
        latitude = round(data["coord"]["lat"], 2)
        longitude = round(data["coord"]["lon"], 2)
        feels_like = round(data["main"]["feels_like"], 2)
        weather_description = data["weather"][0]["description"]
        wind_speed = round(data["wind"]["speed"], 2)
        rain_1h = round(data.get("rain", {}).get("1h", 0), 2)

        # Aggregate existing data
        existing_data = Weather.objects.filter(city=city, date=today_date).aggregate(
            max_temp=Max('max_temp'),
            min_temp=Min('min_temp'),
            avg_temp=Avg('avg_temp'),
            avg_humidity=Avg('avg_humidity'),
            avg_pressure=Avg('avg_pressure'),
            avg_visibility=Avg('avg_visibility')
        )

        # Handle cases where aggregation results are None
        max_temp_existing = existing_data['max_temp'] or float('-inf')
        min_temp_existing = existing_data['min_temp'] or float('inf')
        avg_temp_existing = existing_data['avg_temp'] or temp
        avg_humidity_existing = existing_data['avg_humidity'] or humidity
        avg_pressure_existing = existing_data['avg_pressure'] or pressure
        avg_visibility_existing = existing_data['avg_visibility'] or visibility

        # Calculate new values
        new_max_temp = round(max(temp_max, max_temp_existing), 2)
        new_min_temp = round(min(temp_min, min_temp_existing), 2)
        new_avg_temp = round((temp + avg_temp_existing) / 2, 2)
        new_avg_humidity = round((humidity + avg_humidity_existing) / 2, 2)
        new_avg_pressure = round((pressure + avg_pressure_existing) / 2, 2)
        new_avg_visibility = round(
            (visibility + avg_visibility_existing) / 2, 2)

        # Update or create weather data entry
        weather, created = Weather.objects.update_or_create(
            city=city,
            date=today_date,
            defaults={
                'latitude': latitude,
                'longitude': longitude,
                'max_temp': new_max_temp,
                'min_temp': new_min_temp,
                'avg_temp': new_avg_temp,
                'avg_humidity': new_avg_humidity,
                'avg_pressure': new_avg_pressure,
                'avg_visibility': new_avg_visibility
            }
        )
        weather.save()

        # Append the updated or created weather data
        weather_data_list.append({
            "city": city,
            "date": today_date,
            "latitude": latitude,
            "longitude": longitude,
            "current_temp": temp,
            "feels_like": feels_like,
            "weather_description": weather_description,
            "wind_speed": wind_speed,
            "rain_1h": rain_1h,
            "visibility": visibility,
            "pressure": pressure,
            "max_temp": weather.max_temp,
            "min_temp": weather.min_temp,
            "avg_temp": weather.avg_temp,
            "avg_humidity": weather.avg_humidity,
            'icon': icn
        })

    return weather_data_list, extraction_time


def store_weather_data(city, data):
    if WeatherData.objects.filter(city=city, timestamp=dt.fromtimestamp(data['dt'])).exists():
        return
    weather = WeatherData(
        city=city,
        temperature=data['main']['temp'],
        feels_like=data['main']['feels_like'],
        main_condition=data['weather'][0]['main'],
        timestamp=dt.fromtimestamp(data['dt'])
    )

    weather.save()


def convert_kelvin_to_celsius(kelvin):
    return kelvin - 273.15


def alerrt():
    cities = WeatherData.objects.values_list('city', flat=True).distinct()
    cities_list = list(cities)
    for city in cities_list:
        latest_data = WeatherData.objects.filter(
            city=city).order_by('-timestamp').first()
        if latest_data and latest_data.temperature > 34:
            # alert, created = Alert.objects.get_or_create(
            #     city=city, condition='High Temperature', threshold=35)
            # if not alert.triggered:
            #     alert.triggered = True
            #     alert.save()
            notify_users(city, latest_data.temperature)

            # Notify users (e.g., via email)


def check_and_save_alerts(weather_data_list):
    for weather in weather_data_list:
        condition = ""
        threshold = None

        if weather['current_temp'] > 35:
            condition = "High Temperature"
            threshold = 35
        elif weather['current_temp'] < 15:
            condition = "Low Temperature"
            threshold = 15
        elif weather['rain_1h'] > 0.1:
            condition = "Heavy Rain"
            threshold = 0.1
        elif weather['wind_speed'] > 10:
            condition = "High Wind Speed"
            threshold = 10

        if condition:
            last_hour = datetime.now() - timedelta(hours=1)
            print(last_hour)
            recent_alerts = Alert.objects.filter(
                city=weather['city'],

                timestamp__gte=last_hour
            )
            if not recent_alerts.exists():
                uu = Alert.objects.create(
                    city=weather['city'],
                    condition=condition,
                    threshold=threshold,
                    triggered=True,
                    timestamp=datetime.now()
                )
                uu.save()
                notify_users(weather['city'], condition,
                             threshold, datetime.now())


def check_alerts():
    print("running")
    for city in CITIES:
        latest_data = WeatherData.objects.filter(
            city=city).order_by('-timestamp').first()
        if latest_data and latest_data.temperature > 34:
            alert, created = Alert.objects.get_or_create(
                city=city, condition='High Temperature', threshold=35)
            if not alert.triggered:
                alert.triggered = True
                alert.save()
                # notify_users(city, latest_data.temperature)
    # alerrt()           # Notify users (e.g., via email)


BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast'


def get_upcoming_weather(city_name):
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    # print(response.json())
    data = response.json()

    daily_forecast = defaultdict(list)
    for item in data['list']:
        date = item['dt_txt'].split(' ')[0]
        time = item['dt_txt'].split(' ')[1]
        temp = item['main']['temp']
        condition = item['weather'][0]['description'].title()
        icn = item['weather'][0]['icon']
        daily_forecast[date].append({
            'time': time,
            'temp': temp,
            'condition': condition,
            'icon': icn
        })

    return {
        'city_name': city_name,
        'daily_forecast': dict(daily_forecast)
    }


def notify_users(city, condition, threshold, time):
    city_name = city
    emails = cuties.objects.filter(city=city_name).values_list(
        'email', flat=True).distinct()
    emails_list = list(emails)
    sendd_mail(emails_list, city, condition, threshold, time)


def get_code() -> str:
    a = list("12345678901234567890")
    shuffle(a)
    a = "".join(a)
    return "".join(choice(a) for _ in range(6))


def sendd_mail(email, city, cond, thre, time):
    # code: str = get_code()
    # curr = datetime.datetime.now()
    # email = email
    # SERVER = "smtp.gmail.com"
    # PORT = 587
    # FROM = "ankitch860@gmail.com"
    # TO = email
    # print(email)
   
    # msg = MIMEMultipart()
    # msg['subject'] = f"Weather Alert for {city}"
    # msg['From'] = FROM
    # msg['To'] = TO
    # co = f"Temperature in {city} has exceeded the threshold: {temp}°C."
    # msg.attach(MIMEText(co, 'html'))
    # print("Creating mail")
    # server = SMTP(SERVER, PORT)
    # server.set_debuglevel(1)
    # server.ehlo()
    # server.starttls()
    # server.login(FROM, PASS)
    # server.sendmail(FROM, TO, msg.as_string())
    # print('Sending Email')
    # server.quit()
    # print('Email sent ......')
    send_mail(
        f'Weather alert for city {city}',
        f'{cond} in {city} at {time} .Weather in {city} has exceeded the threshold: {thre} Be safe',
        'ankitch860@gmail.com',
        email,
        fail_silently=False,
    )


def send_code(email: str) -> str:
    code: str = get_code()
    # curr = datetime.datetime.now()
    email = email
    SERVER = "smtp.gmail.com"
    PORT = 587
    FROM = "ankitch860@gmail.com"
    TO = email
   
    msg = MIMEMultipart()
    msg['subject'] = f"Verify your account"
    msg['From'] = FROM
    msg['To'] = TO
    co = f"Your verification code is {code}"
    msg.attach(MIMEText(co, 'html'))
    print("Creating mail")
    server = SMTP(SERVER, PORT)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(FROM, PASS)
    server.sendmail(FROM, TO, msg.as_string())
    print('Sending Email')
    server.quit()
    print('Email sent ......')
    return code


def getcity(citty):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={citty}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    context = {
        'city': citty,
        'temperature': data['main']['temp'],
        'feels_like': data['main']['feels_like'],
        'main_condition': data['weather'][0]['main'],
        'timestamp': dt.fromtimestamp(data['dt'])}
    if WeatherData.objects.filter(city=citty, timestamp=dt.fromtimestamp(data['dt'])).exists():
        return context
    weather = WeatherData(
        city=citty,
        temperature=data['main']['temp'],
        feels_like=data['main']['feels_like'],
        main_condition=data['weather'][0]['main'],
        timestamp=dt.fromtimestamp(data['dt'])
    )

    weather.save()
    return context
