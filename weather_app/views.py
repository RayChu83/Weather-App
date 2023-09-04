from django.shortcuts import render
from django.views.generic import *
from django.conf import settings

import requests
# Create your views here.

class WeatherMixin():
    def create_context(self, data, image_data):
        city_context = {
            "city_errors" : False,
            "city_image" : image_data["results"][0]["urls"]["raw"],
            # CITY INFORMATION
            "city_name" : data["name"],
            "city_country": data["sys"]["country"],
            "city_description" : data["weather"][0]["description"],
            "city_wind" : int(data["wind"]["speed"]),
            # TEMPERATURE CONTEXT DICTIONARY
            "temperature" : int(data["main"]["temp"]),
            "temperature_feeling" : int(data["main"]["feels_like"]),
            "temperature_min" : int(data["main"]["temp_min"]),
            "temperature_max" : int(data["main"]["temp_max"]),

            "weather_icon_code" : data["weather"][0]["icon"],
        }
        return city_context

class Index(TemplateView, WeatherMixin):
    template_name = "weather_app/index.html"
    API_KEY = settings.API_KEY
    UNSPLASH_KEY = settings.UNSPLASH_KEY

    def get(self,request):
        return render(request, self.template_name)
    
    def post(self,request):
        city = request.POST.get("city-input")
        
        image_url = f"https://api.unsplash.com/search/photos/?client_id={self.UNSPLASH_KEY}&page=1&per_page=1&query={city}"
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.API_KEY}&units=imperial"

        image_response = requests.get(image_url)
        image_data = image_response.json()

        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        if "message" not in weather_data:
            context = self.create_context(weather_data, image_data)
        else:
            context = {"city_errors" : True,
                       "city": city}
            
        return render(request, self.template_name, context)