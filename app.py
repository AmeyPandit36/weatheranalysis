# # from flask import Flask, render_template, request, redirect, url_for, flash
# # import mysql.connector
# # import requests
# # from datetime import datetime, timedelta
# # import pytz
# # from geopy.geocoders import Nominatim
# # from timezonefinder import TimezoneFinder

# # app = Flask(__name__)
# # app.secret_key = 'your_secret_key'  # Needed for flashing messages

# # # MySQL Database Connection
# # def get_db_connection():
# #     connection = mysql.connector.connect(
# #         host='localhost',
# #         user='weather_user',
# #         password='weather_pass',
# #         database='weather_db2'
# #     )
# #     return connection

# # # Home Route
# # @app.route('/', methods=['GET', 'POST'])
# # def home():
# #     if request.method == 'POST':
# #         city = request.form.get('city')
# #         if not city:
# #             flash("Please enter a city name!")
# #             return redirect(url_for('home'))
        
# #         try:
# #             # Geolocation
# #             geolocator = Nominatim(user_agent="web_weather_app")
# #             location = geolocator.geocode(city)
# #             if not location:
# #                 flash("Invalid city name! Try again.")
# #                 return redirect(url_for('home'))

# #             timezone = TimezoneFinder().timezone_at(lng=location.longitude, lat=location.latitude)
# #             home_timezone = pytz.timezone(timezone)
# #             local_time = datetime.now(home_timezone).strftime("%I:%M %p")
            
# #             # Weather API
# #             API_KEY = "a3de7d55963e46a194e20830251104"  # (Same API key)
# #             api_url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=7&aqi=no&alerts=no"
# #             response = requests.get(api_url)
# #             weather_data = response.json()

# #             if "error" in weather_data:
# #                 flash(weather_data["error"]["message"])
# #                 return redirect(url_for('home'))

# #             # Extract current weather
# #             current = {
# #                 'temp': weather_data['current']['temp_c'],
# #                 'humidity': weather_data['current']['humidity'],
# #                 'pressure': weather_data['current']['pressure_mb'],
# #                 'wind': weather_data['current']['wind_kph'],
# #                 'description': weather_data['current']['condition']['text'],
# #                 'icon': "https:" + weather_data['current']['condition']['icon'],
# #                 'local_time': local_time,
# #                 'timezone': timezone,
# #                 'latitude': round(location.latitude, 4),
# #                 'longitude': round(location.longitude, 4)
# #             }

# #             # Extract 7 days forecast
# #             forecast = []
# #             for day in weather_data['forecast']['forecastday']:
# #                 forecast.append({
# #                     'date': day['date'],
# #                     'avg_temp': day['day']['avgtemp_c'],
# #                     'humidity': day['day']['avghumidity'],
# #                     'icon': "https:" + day['day']['condition']['icon'],
# #                     'description': day['day']['condition']['text']
# #                 })

# #             return render_template('home.html', city=city, current=current, forecast=forecast)

# #         except Exception as e:
# #             flash(f"Error: {str(e)}")
# #             return redirect(url_for('home'))

# #     return render_template('home.html')

# # if __name__ == '__main__':
# #     app.run(debug=True)



from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import requests
from datetime import datetime, timedelta
import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# MySQL Database Connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='weather_user',
        password='weather_pass',
        database='weather_db2'
    )
    return connection

# # ======================== Home Route ========================
# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         city = request.form.get('city')
#         if not city:
#             flash("Please enter a city name!")
#             return redirect(url_for('home'))
        
#         try:
#             # Geolocation
#             geolocator = Nominatim(user_agent="web_weather_app")
#             location = geolocator.geocode(city)
#             if not location:
#                 flash("Invalid city name! Try again.")
#                 return redirect(url_for('home'))

#             timezone = TimezoneFinder().timezone_at(lng=location.longitude, lat=location.latitude)
#             home_timezone = pytz.timezone(timezone)
#             local_time = datetime.now(home_timezone).strftime("%I:%M %p")
            
#             # Weather API
#             API_KEY = "a3de7d55963e46a194e20830251104"
#             api_url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=7&aqi=no&alerts=no"
#             response = requests.get(api_url)
#             weather_data = response.json()

#             if "error" in weather_data:
#                 flash(weather_data["error"]["message"])
#                 return redirect(url_for('home'))

#             # Extract current weather
#             current = {
#                 'temp': weather_data['current']['temp_c'],
#                 'humidity': weather_data['current']['humidity'],
#                 'pressure': weather_data['current']['pressure_mb'],
#                 'wind': weather_data['current']['wind_kph'],
#                 'description': weather_data['current']['condition']['text'],
#                 'icon': "https:" + weather_data['current']['condition']['icon'],
#                 'local_time': local_time,
#                 'timezone': timezone,
#                 'latitude': round(location.latitude, 4),
#                 'longitude': round(location.longitude, 4)
#             }

#             # Extract 7 days forecast
#             forecast = []
#             for day in weather_data['forecast']['forecastday']:
#                 forecast.append({
#                     'date': day['date'],
#                     'avg_temp': day['day']['avgtemp_c'],
#                     'humidity': day['day']['avghumidity'],
#                     'icon': "https:" + day['day']['condition']['icon'],
#                     'description': day['day']['condition']['text']
#                 })

#             return render_template('home.html', city=city, current=current, forecast=forecast)

#         except Exception as e:
#             flash(f"Error: {str(e)}")
#             return redirect(url_for('home'))

#     return render_template('home.html')



# ======================== Home Route ========================
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        city = request.form.get('city')
        if not city:
            flash("Please enter a city name!")
            return redirect(url_for('home'))
        
        try:
            # Geolocation
            geolocator = Nominatim(user_agent="web_weather_app")
            location = geolocator.geocode(city)
            if not location:
                flash("Invalid city name! Try again.")
                return redirect(url_for('home'))

            timezone = TimezoneFinder().timezone_at(lng=location.longitude, lat=location.latitude)
            home_timezone = pytz.timezone(timezone)
            local_time = datetime.now(home_timezone).strftime("%I:%M %p")
            
            API_KEY = "a3de7d55963e46a194e20830251104"

            # Current weather
            current_url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
            response = requests.get(current_url)
            weather_data = response.json()

            if "error" in weather_data:
                flash(weather_data["error"]["message"])
                return redirect(url_for('home'))

            # Extract current weather
            current = {
                'temp': weather_data['current']['temp_c'],
                'humidity': weather_data['current']['humidity'],
                'pressure': weather_data['current']['pressure_mb'],
                'wind': weather_data['current']['wind_kph'],
                'description': weather_data['current']['condition']['text'],
                'icon': "https:" + weather_data['current']['condition']['icon'],
                'local_time': local_time,
                'timezone': timezone,
                'latitude': round(location.latitude, 4),
                'longitude': round(location.longitude, 4)
            }

            # Fetch past 7 days history
            past_forecast = []
            today = datetime.now().date()

            for i in range(1, 8):  # Past 7 days
                date = today - timedelta(days=i)
                history_url = f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={city}&dt={date}"
                history_response = requests.get(history_url)
                history_data = history_response.json()

                if "error" in history_data:
                    continue

                day_data = history_data['forecast']['forecastday'][0]['day']

                past_forecast.append({
                    'date': date.strftime("%Y-%m-%d"),
                    'avg_temp': day_data['avgtemp_c'],
                    'humidity': day_data['avghumidity'],
                    'icon': "https:" + day_data['condition']['icon'],
                    'description': day_data['condition']['text']
                })

            # Fetch future 3 days forecast
            future_forecast = []
            forecast_url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=3&aqi=no&alerts=no"
            forecast_response = requests.get(forecast_url)
            forecast_data = forecast_response.json()

            if "error" not in forecast_data:
                for day in forecast_data['forecast']['forecastday']:
                    future_forecast.append({
                        'date': day['date'],
                        'avg_temp': day['day']['avgtemp_c'],
                        'humidity': day['day']['avghumidity'],
                        'icon': "https:" + day['day']['condition']['icon'],
                        'description': day['day']['condition']['text']
                    })

            return render_template('home.html', city=city, current=current, past_forecast=past_forecast, future_forecast=future_forecast)

        except Exception as e:
            flash(f"Error: {str(e)}")
            return redirect(url_for('home'))

    return render_template('home.html')



# ======================== Analysis Route ========================
@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all distinct cities for dropdown
    cursor.execute("SELECT DISTINCT city FROM weather_data1")
    cities = [row[0] for row in cursor.fetchall()]
    conn.close()

    if request.method == 'POST':
        city = request.form.get('city')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if not city or not start_date or not end_date:
            flash("Please fill all fields!")
            return redirect(url_for('analysis'))

        try:
            conn = get_db_connection()
            query = """
                SELECT date, temperature, humidity 
                FROM weather_data1 
                WHERE city = %s AND date BETWEEN %s AND %s
            """
            df = pd.read_sql(query, conn, params=(city, start_date, end_date))
            conn.close()

            if df.empty:
                flash("No data found for selected city and date range.")
                return redirect(url_for('analysis'))

            # Generate Graph
            img = io.BytesIO()
            plt.figure(figsize=(10,5))
            plt.plot(df['date'], df['temperature'], label='Temperature (°C)', color='red', marker='o')
            plt.plot(df['date'], df['humidity'], label='Humidity (%)', color='blue', linestyle='--', marker='s')
            plt.legend()
            plt.title(f"Weather Analysis: {city}")
            plt.xlabel("Date")
            plt.ylabel("Values")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()

            return render_template('analysis.html', cities=cities, plot_url=plot_url)

        except Exception as e:
            flash(f"Error generating graph: {str(e)}")
            return redirect(url_for('analysis'))

    return render_template('analysis.html', cities=cities)

# ======================== Run App ========================
if __name__ == '__main__':
    app.run(debug=True)
