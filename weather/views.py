from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import WeatherData, Alert
from .utils import get_upcoming_weather, fetch_weather_data, check_alerts, CITIES, send_code, send_mail, getcity

from django.shortcuts import render
from .models import WeatherData, Alert
from django.db.models import Avg, Max, Min
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import WeatherData, cuties
import uuid
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
# Adjust the import if needed
from .utils import fetch_weather_data, check_and_save_alerts, fetch_city
from django.db.models import Sum
from .models import Alert
from django.utils.timezone import now
from .models import Weather
from datetime import date, timedelta


# # def weather_view(request):
# #     weather_data_list, extraction_time = fetch_weather_data()  # Adjust this if needed

# #     check_and_save_alerts(weather_data_list)

# #     alerts = Alert.objects.all()
# #     context = {
# #         'weather_data_list': weather_data_list,
# #         'alerts': alerts,
# #         'current_year': timezone.now().year
# #     }
#     return render(request, 'weather.html', context)


@login_required(login_url='/loginn')
def logout(request):
    auth.logout(request)
    messages.success(request, "Succesfully logout")
    return redirect("/")


@login_required(login_url='/loginn')
def weather_view(request):
    # Fetch all weather data (you might have a different function for this)
    weather_data_list, extraction_time = fetch_weather_data()
    user = request.user.username

    cit = cuties.objects.filter(email=user).first()
    citty = cit.city
    # Get the current time
    ci = []
    ci.append(citty)
    city_data, city_time = fetch_city(ci)
    print(city_data)
    current_time = now()
    check_and_save_alerts(weather_data_list)


# Get the current time and calculate the time two hours ago
    noww = timezone.now()
    two_hours_ago = noww - timezone.timedelta(hours=4)

    # Filter alerts from the past two hours
    recent_alerts = Alert.objects.filter(timestamp__gte=two_hours_ago)

    # Aggregate counts of different alert types
    alert_summary = recent_alerts.values('condition').annotate(
        total_quantity=Sum('quantity')
    )

    # Create a dictionary to pass to the context
    alert_counts = {condition['condition']: condition['total_quantity']
                    for condition in alert_summary}

    # Print the alert summary for debugging
    print(alert_counts)

    # Pass the alert_counts to the context
    context = {
        'alert_counts': alert_counts,
        # Add other context variables as needed
    }  # Context for rendering the template
    context = {
        'weather_data_list': weather_data_list,
        'alerts': recent_alerts,
        'weatheer': city_data,
        'city_time': city_time,
        'high_temp_count': alert_counts.get('High Temperature', 0),
        'low_temp_count': alert_counts.get('Low Temperature', 0),
        'rain_count': alert_counts.get('Heavy Rain', 0),
        'wind_count': alert_counts.get('High Wind Speed', 0),
        'current_year': current_time.year
    }

    return render(request, 'weather.html', context)


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST.get('password', '')
        email = request.POST['email']
        city = request.POST['citty']
        if cuties.objects.filter(email=email, is_active=True).exists():
            messages.info(request, "Account already exists.Kindly login")

            return redirect("/register_gh")
        if cuties.objects.filter(email=email, is_active=False).exists():
            messages.info(request, "Account not verified.Kindly verify.")
            return redirect("/register_gh")
        code: str = send_code(email=email)
        token = uuid.uuid4()
        student = cuties.objects.create(
            city=city, name=name, password=password, email=email, code=code, token=token)
        student.save()
        return render(request, 'validate.html', {"token": token})
    return render(request, 'register.html')


def validatestudent(request, token):
    if request.method == 'POST':
        code: str = request.POST.get('code')
        student = cuties.objects.get(token=token)
        if student.is_active == True:
            messages.info(request, "Account already verified.Kindly login")
            return redirect('/register_gh')
        if code == student.code:
            student.is_active = True
            user = User.objects.create_user(
                username=student.email, password=student.password)
            user.save()
            student.save()
            CITIES.append(student.city)
            messages.info(
                request, "Account  verified Successfully.Kindly login")
            return redirect('/register_gh')
        else:
            messages.info(request, "Wrong code")
            return redirect(f'/validatestudent/{token}')
    else:
        return render(request, 'validate.html', {"token": token})


def loginn(request):
    if request.user.is_authenticated:
        return redirect('/weather')
    if request.method == 'POST':
        email = request.POST['email']
        passs = request.POST['password']
        user = auth.authenticate(username=email, password=passs)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Invalid details")
            return redirect('/loginn')

    return render(request, "login.html")


def search(request):
    if request.method == 'POST':
        city = request.POST['city']
        citi = []
        citi.append(city)
        fetch_city(citi)
        return redirect(f"/city/{city}")
    return redirect("/")


def city_details(request, city_name):
    today_summary = Weather.objects.filter(city=city_name, date=date.today()).aggregate(
        avg_temp=Avg('avg_temp'),
        max_temp=Max('max_temp'),
        min_temp=Min('min_temp')
    )
    ci = []
    ci.append(city_name)
    weather_details, extr = fetch_city(ci)
    # Fetch weather data for the last week
    one_week_ago = date.today() - timedelta(days=7)
    daily_aggregates = Weather.objects.filter(
        city=city_name, date__gte=one_week_ago).order_by('date')

    context = {
        'weather_details': weather_details,
        'city_name': city_name,
        'summary': today_summary,
        'daily_aggregates': daily_aggregates,
    }
    return render(request, 'city_details.html', context)


@login_required(login_url='/loginn')
def home(request):
    weather_data = {}
    alerts = Alert.objects.filter(triggered=True)
    user = request.user.username
    print(user)
    cit = cuties.objects.filter(email=user).first()
    citty = cit.city
    context = {
        'weather_data': weather_data,
        'alerts': alerts,
        'summary_data': get_summary_data(),
        'city_data': getcity(citty),
        'historical_data': get_historical_data(),
    }
    return render(request, 'home.html', context)


def weather_forecast_view(request, city_name):
    city_name = city_name  # Example city
    context = get_upcoming_weather(city_name)

    return render(request, 'weather_forecast.html', context)


def refresh(request):
    fetch_weather_data()
    check_alerts()
    return redirect("/")


def get_summary_data():
    # Aggregate data for summaries
    today = timezone.now().date()
    summary = WeatherData.objects.filter(timestamp__date=today).aggregate(
        avg_temp=Avg('temperature'),
        max_temp=Max('temperature'),
        min_temp=Min('temperature')
    )
    return summary


def get_historical_data():
    # Collect historical data for trends
    last_week = timezone.now() - timedelta(days=7)
    historical = WeatherData.objects.filter(timestamp__gte=last_week).values(
        'timestamp__date'
    ).annotate(avg_temp=Avg('temperature')).order_by('timestamp__date')
    return historical


def fetch_data_view(request):
    fetch_weather_data()
    return JsonResponse({'status': 'Data fetched successfully'})


def chec_alerts(request):
    check_alerts()
    return JsonResponse({'status': 'Alert fetched successfully'})
