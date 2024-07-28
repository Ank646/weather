Here's the updated README with your additional features:

---

# Weather Application using Django

This project is a comprehensive weather monitoring application built with Django.

## Features

- **Personalized Weather Updates:** Access real-time weather updates for your city, including max, min, and average temperatures. View upcoming days' weather directly from your homepage.

- **City Weather Search:** Explore current weather conditions and historical data for any city. View comprehensive summaries with graphs and tables.

- **Metropolitan Weather Summary:** Stay informed with updates for major metropolitan cities directly on your homepage.

- **Upcoming Weather Trends:** Discover detailed forecasts, including wind speed and humidity, for cities in the coming days.

- **Weather Alerts:** Receive alerts for unpleasant weather conditions with notifications for weather exceeding your preferred thresholds.

- **Upcoming Days Weather Data:** Get detailed forecasts and trends for upcoming days, including temperature, precipitation, and more.

- **Email Notifications:** Register to get email alerts about significant weather changes in your city.

- **Threshold Condition Checks:** The system checks weather conditions every 5 minutes and sends warnings to registered users every hour if thresholds are exceeded.

## Getting Started

Follow these instructions to set up the project on your local machine.

### Prerequisites

Ensure you have the following installed:

- Python (version 3.x)
- Django (version 3.x)
- API key for weather data (e.g., from OpenWeatherMap)

### Installing

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your/repository.git
   cd repository-name
   ```

2. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables:**

   Create a `.env` file in the root directory and add your API keys and other sensitive information:

   ```bash
   # .env file
   WEATHER_API_KEY=your_weather_api_key_here
   EMAIL_APP_PASSWORD=your_email_app_password_here
   ```

### Database Setup

1. **Make migrations:**

   ```bash
   python manage.py makemigrations
   ```

2. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

### Running the Server

Start the Django development server:

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`.

## Usage

- Visit `http://localhost:8000` in your web browser to access the weather application.
- Enter a city name or ZIP code to retrieve weather information.
