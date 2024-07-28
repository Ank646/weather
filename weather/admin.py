from django.contrib import admin

# Register your models here.
from .models import Alert, WeatherData, Weather, cuties
# Register your models here.
admin.site.register(Alert)
admin.site.register(WeatherData)
admin.site.register(cuties)
admin.site.register(Weather)
