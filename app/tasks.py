import requests
from huey import RedisHuey

huey = RedisHuey('weather_app', host='testing_redis')

@huey.task()
def get_weather(location):
    # Use OpenMeteo API to get coordinates
    geocoding_url = f'https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json'
    geo_response = requests.get(geocoding_url)
    
    if geo_response.status_code != 200:
        return {'error': 'Unable to find location'}
    
    geo_data = geo_response.json()
    if not geo_data.get('results'):
        return {'error': 'Location not found'}
    
    lat = geo_data['results'][0]['latitude']
    lon = geo_data['results'][0]['longitude']
    
    # Use OpenMeteo API to get weather data
    weather_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true'
    weather_response = requests.get(weather_url)
    
    if weather_response.status_code != 200:
        return {'error': 'Unable to fetch weather data'}
    
    weather_data = weather_response.json()
    current_weather = weather_data['current_weather']
    
    return {
        'location': geo_data['results'][0]['name'],
        'temperature': current_weather['temperature'],
        'description': get_weather_description(current_weather['weathercode'])
    }

def get_weather_description(code):
    weather_codes = {
        0: 'Clear sky',
        1: 'Mainly clear',
        2: 'Partly cloudy',
        3: 'Overcast',
        45: 'Fog',
        48: 'Depositing rime fog',
        51: 'Light drizzle',
        53: 'Moderate drizzle',
        55: 'Dense drizzle',
        61: 'Slight rain',
        63: 'Moderate rain',
        65: 'Heavy rain',
        71: 'Slight snow fall',
        73: 'Moderate snow fall',
        75: 'Heavy snow fall',
        95: 'Thunderstorm',
    }
    return weather_codes.get(code, 'Unknown')
