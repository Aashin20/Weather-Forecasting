import streamlit as st
import requests
import datetime
from geopy.geocoders import Nominatim
import time


st.title("WeatherBee 🐝")
st.header("Forecast the weather in your city!")
st.write("")


city = st.text_input("Enter your City")
unit = st.selectbox("Enter the unit", ['Celsius', 'Fahrenheit'])


geolocator = Nominatim(user_agent="weather_app_exercise")


lat, lon = None, None


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
    
    
    time.sleep(1)


if unit == "Celsius":
    temp_unit = " °C"
    temp_conversion = lambda kelvin: round(kelvin - 273.15, 2)
else:
    temp_unit = " °F"
    temp_conversion = lambda kelvin: round(((kelvin - 273.15) * 1.8) + 32, 2)

api = "82a3c62eb946e26e84efd9f2cf475970"

if st.button("SUBMIT") and lat is not None and lon is not None:
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api}'
    res = requests.get(url)
    y = res.json()
