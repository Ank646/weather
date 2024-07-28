from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather_view, name='home'),
    path('logout', views.logout, name='logout'),
    path('fetch/', views.fetch_data_view, name='fetch_data'),
    path('alert/', views.chec_alerts, name='alert'),
    path('validatestudent/<str:token>', views.validatestudent, name='validate'),
    path('register_gh', views.register, name='register'),
    path('loginn', views.loginn, name='loginn'),
    path('search', views.search, name='search'),
    path('refresh', views.refresh, name='refresh'),
    path('weather', views.weather_view, name='weather'),

    path('city/<str:city_name>/', views.city_details, name='city_details'),
    path('forecast/<str:city_name>/', views.weather_forecast_view, name='city_details'),]
