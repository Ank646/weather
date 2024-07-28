from django.db import models

import uuid


class cuties(models.Model):
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=False)
    token = models.UUIDField(default=uuid.uuid4())
    code = models.CharField(max_length=6, default="")

    def __str__(self):
        return self.name


class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    feels_like = models.FloatField()
    main_condition = models.CharField(max_length=50)
    timestamp = models.DateTimeField()


class Weather(models.Model):
    city = models.CharField(max_length=100)
    date = models.DateField()
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    avg_temp = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    avg_humidity = models.FloatField()
    avg_pressure = models.FloatField()
    avg_visibility = models.FloatField()

    def __str__(self):
        return f"Weather for {self.city} on {self.date}"


class Alert(models.Model):
    city = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    threshold = models.FloatField()
    triggered = models.BooleanField(default=False)
    timestamp = models.DateTimeField()
    quantity = models.PositiveIntegerField(default=1)
