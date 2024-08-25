import streamlit as st
import requests
from datetime import datetime
from geopy.geocoders import Nominatim
import time
import pytz

# Setting up streamlit 


current_time = datetime.now(pytz.timezone('Asia/Kolkata'))
now = int(current_time.strftime("%H"))
if(now>5 and now<12):
  st.title("Good Morning!!⛅")
elif(now>12 and now<17):
  st.title("Good Afternoon!!☀️")
elif(now>17 and now<21):
  st.title("Good Evening!! 🌇")
else:
  st.title("Good Night!! 🌙")


st.header("Check the weather in your location!")
st.write("")

# Input for city and unit selection
city = st.text_input("Enter your City")
unit = st.selectbox("Enter the unit", ['Celsius', 'Fahrenheit'])

# Initialize the Nominatim geolocator with a descriptive user-agent
geolocator = Nominatim(user_agent="weather_app_exercise")

# Initialize latitude and longitude 
lat, lon = None, None

# Perform geocoding to get latitude and longitude
if city:
    try:
        location = geolocator.geocode(city)
        if location:
            lat = location.latitude
            lon = location.longitude
        else:
            st.error("City not found!")
    except geopy.exc.GeocoderTimedOut:
        st.error("Geocoding service timed out.")
    except geopy.exc.GeocoderServiceError:
        st.error("Geocoding service error.")
    except geopy.exc.GeocoderInsufficientPrivileges:
        st.error("Insufficient privileges to access geocoding service.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    
    # Adding a delay between requests to avoid rate limits
    time.sleep(1)

# Determine the temperature unit based on the user's selection
if unit == "Celsius":
    temp_unit = " °C"
    temp_conversion = lambda kelvin: round(kelvin - 273.15, 2)
else:
    temp_unit = " °F"
    temp_conversion = lambda kelvin: round(((kelvin - 273.15) * 1.8) + 32, 2)

# OpenWeatherMap API key
api = "82a3c62eb946e26e84efd9f2cf475970"

# Fetch and display weather data if the user clicks the submit button
if st.button("SUBMIT") and lat is not None and lon is not None:
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api}'
    res = requests.get(url)
    y = res.json()

    if res.status_code == 200:
        # Extract the required information from the API response
        main = y["main"]
        weather = y["weather"][0]
        sys = y["sys"]
        visib=y["visibility"]

        maxtemp = temp_conversion(main["temp_max"])
        mintemp = temp_conversion(main["temp_min"])
        current_temp = str(temp_conversion(main["temp"]))
        feels_like = str(temp_conversion(main["feels_like"]))
        pres = main["pressure"]
        humd = f'{main["humidity"]} %'
        desc = weather["description"].title()
        icon=weather["icon"]
        visi=visib

        # Changing date and time to UTC
        d1 = datetime.fromtimestamp(y["dt"])
        date_str = d1.strftime('%d %b')

        # Convert sunrise and sunset from UTC to IST
        utc_time_zone = pytz.utc
        ist_time_zone = pytz.timezone('Asia/Kolkata')
        
        sunrise_utc = datetime.utcfromtimestamp(sys["sunrise"]).replace(tzinfo=utc_time_zone)
        sunset_utc = datetime.utcfromtimestamp(sys["sunset"]).replace(tzinfo=utc_time_zone)
        
        sunrise_ist = sunrise_utc.astimezone(ist_time_zone).strftime('%H:%M IST')
        sunset_ist = sunset_utc.astimezone(ist_time_zone).strftime('%H:%M IST')
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("## Current Weather ")
        with col2:
            st.image(f"http://openweathermap.org/img/wn/{icon}@2x.png",width=70)

        
        col1, col2= st.columns(2)
        col1.metric("TEMPERATURE",current_temp+temp_unit) 
        col2.metric("WEATHER",desc)
        col2.caption("Feels like:"+feels_like+temp_unit)
        st.subheader(" ")

        #Displaying data

        col1.text(f"♨️Max Temp today: {maxtemp}{temp_unit}")
        col1.text(f"❄️Min Temp today: {mintemp}{temp_unit}")
        col1.text(f"💨Pressure: {pres}hPa")
        col1.text(f"💧Humidity: {humd}")
        col1.text(f"🌫️Visibility: {visi}")
        col1.text(f"🌅Sunrise: {sunrise_ist} ")
        col1.text(f"🌇Sunset: {sunset_ist} ")



    else:
        st.error("Failed to retrieve data. Please check the city name.")
