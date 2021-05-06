from flask import Flask, render_template, redirect, url_for, make_response, request
import requests
from config import Config
from forms import SearchForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adlq,3-1eo,3o32dmi23jr4394if43093ikpdw'
app.config['OWM_TOKEN']='34be0019993203b5a55de4637b2cd0e1'
app.config['IPINFO_TOKEN']='254aabce1a4e9e'


@app.route('/home', defaults={'city_by_search':None}, methods=['get', 'post'])
@app.route('/home/index', defaults={'city_by_search':None}, methods=['get', 'post'])
@app.route('/weather_at/<city_by_search>', methods=['get', 'post'])
def index(city_by_search):
    form = SearchForm()
    if request.method=='POST':
        if form.validate_on_submit():
            city = form.search.data
            return redirect(f'/weather_at/{city}')
    if city_by_search:
        city = city_by_search
    elif request.cookies.get('ipinfo_city'):
        city=request.cookies.get('ipinfo_city')
    else:
        ipinfo = requests.get('http://ipinfo.io/?token=254aabce1a4e9e').json()
        city = ipinfo['city']

    json_weather_data = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=34be0019993203b5a55de4637b2cd0e1&units=metric&lang=ru').json()
    image = json_weather_data['weather'][0]['icon']
    temperature = json_weather_data['main']['temp']
    weather = json_weather_data['weather'][0]['description']
    town = json_weather_data['name']
    wind = json_weather_data['wind']['speed']

        #return redirect(f'/weather_at/{city}')
    res = make_response(render_template('index.html', ipinfo_city=None, town=town, temperature=temperature, weather=weather,
                           wind=wind, image=image, form=form))
    if not request.cookies.get('ipinfo_city'):
        res.set_cookie('ipinfo_city',city, max_age=60*60*24*365)
    return res

if __name__ == '__main__':
    app.run()