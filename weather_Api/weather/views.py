from django.shortcuts import render
from django import forms
import requests
# Create your views here.
class cityForm(forms.Form):
    city = forms.CharField(label='City')
def index(request):
    if(request.method == 'POST'):
        form = cityForm(request.POST)
        if form.is_valid():
            apiAdress = "http://api.openweathermap.org/data/2.5/weather?appid=d8f077af512a644a30e8de49c5735e3a&units=metric&q="
            cityName = form.cleaned_data["city"]
            url = apiAdress + cityName
            response = requests.get(url)
            data = response.json()
            if(data["cod"] != 200):
                return(render(request,"weather/error.html",{
                    "form": cityForm()
                }))
            else:
                context = {
                    "form": cityForm(),
                    "city": cityName.capitalize(),
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "temp_max": data["main"]["temp_max"],
                    "temp_min": data["main"]["temp_min"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                    "country": data["sys"]["country"]  
                }
                return(render(request, "weather/city.html",context))
        else:
            return(render(request,"weather/index.html"),{
                "form": form
            })
    return render(request, "weather/index.html",{
        "form": cityForm()
    })