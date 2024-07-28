from django.apps import AppConfig


class WeatherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather'

    # name = 'weather'

    # def ready(self):
    #     # Schedule the task
    #     schedule('weather.utils.fetch_weather_data',
    #              schedule_type=Schedule.MINUTES, minutes=1)
