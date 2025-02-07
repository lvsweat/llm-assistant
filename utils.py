import json
import requests
import datetime
from dateutil.parser import parse
import api_keys

class coords:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

class weather:
    def __init__(self):
        self.tempurature = -100
        self.unit = '°C'

class time:
    def __init__(self):
        self.time = '00:00'
        self.timezone = 'UTC'

class ip_info:
    def __init__(self):
        self.ip_address = ''
        self.city = ''
        self.country_code = ''
        self.country = ''
        self.region = ''
        self.region_name = ''
        self.timezone = ''
        self.coords = coords(0.0, 0.0)

def get_ip_info() -> ip_info:
    """
    Obtain location data using public ip address

    Returns:
        ip_info: Object containing location data
    """

    ret = ip_info()
    ip_address = requests.get('https://api.ipify.org').text # Get public ip address
    ip_info_resp = requests.get(f'http://ip-api.com/json/{ip_address}').text # Get location data from public ip address
    ip_info_json = json.loads(ip_info_resp) # Parse json response from location data request

    ret.ip_address = ip_info_json['query']
    ret.city = ip_info_json['city']
    ret.country = ip_info_json['country']
    ret.country_code = ip_info_json['countryCode']
    ret.region = ip_info_json['region']
    ret.region_name = ip_info_json['regionName']
    ret.timezone = ip_info_json['timezone']
    ret.coords.latitude = ip_info_json['lat']
    ret.coords.longitude = ip_info_json['lon']
    return ret



def resolve_lat_and_long(country: str, city: str, state: str = '') -> coords:
    """
    Obtain coordinates at a given location

    Args:
        country (string): The country to get coordinates for
        city (string): The city to get coordinates for
        state (string): The state to get coordinates for

    Returns:
        coords: Object containing coordinates to provided location. This will be coords(0, 0) if the provided location could not be found, or if you are looking for null island I guess.
    """
        
    api_url = f'https://api.api-ninjas.com/v1/geocoding?country={country}&city={city}&state={state}'
    response = requests.get(api_url, headers={'X-Api-Key': api_keys.API_NINJAS_KEY})
    ret = coords(0, 0)
    data = {}
    arr = []
    if response.status_code == requests.codes.ok: # Make sure the api request succeeded
        data = json.loads(response.text) # Parse json response. This will be an array
        if (len(data) < 1): # Make sure the array is not empty
            return ret
        ret.latitude = data[0]["latitude"]
        ret.longitude = data[0]["longitude"]

    return ret

def get_weather_from_coords(coordinates: coords) -> weather:
    """
    Obtain current weather at specified coordinates

    Args:
        coordinates (coords): The coordinates to get the weather for

    Returns:
        weather: Object containing weather data
    """

    ret = weather()
    api_url = f'https://api.open-meteo.com/v1/forecast?latitude={coordinates.latitude}&longitude={coordinates.longitude}&hourly=temperature_2m&forecast_hours=2'
    response = requests.get(api_url)
    data = {}
    if response.status_code == requests.codes.ok: # Make sure the api request succeeded
        data = json.loads(response.text) # Parse json response
        ret.unit = data["hourly_units"]["temperature_2m"]
        ret.tempurature = data["hourly"]["temperature_2m"][0]

    return ret

def get_weather_from_ip() -> weather:
    """
    Obtain current weather at the location of your public ip address

    Returns:
        weather: Object containing weather data
    """

    ret = weather()
    location_data = get_ip_info()
    api_url = f'https://api.open-meteo.com/v1/forecast?latitude={location_data.coords.latitude}&longitude={location_data.coords.longitude}&hourly=temperature_2m&forecast_hours=2'
    response = requests.get(api_url)
    data = {}
    if response.status_code == requests.codes.ok: # Make sure the api request succeeded
        data = json.loads(response.text) # Parse json response
        ret.unit = data["hourly_units"]["temperature_2m"]
        ret.tempurature = data["hourly"]["temperature_2m"][0]

    return ret

def get_time_from_coords(coordinates: coords) -> time:
    """
    Obtain current time at specified coordinates

    Args:
        coordinates (coords): The coordinates to get the time for

    Returns:
        time: Object containing time data
    """
        
    ret = time()
    api_url = f'https://timeapi.io/api/time/current/coordinate?latitude={coordinates.latitude}&longitude={coordinates.longitude}'
    response = requests.get(api_url)
    data = {}
    if response.status_code == requests.codes.ok: # Make sure the api request succeeded
        data = json.loads(response.text) # Parse json response
        ret.time = data["time"]
        ret.timezone = data["timeZone"]

    return ret

def get_time_from_ip() -> time:
    """
    Obtain current time at the location of your public ip address

    Returns:
        time: Object containing time data
    """

    ret = time()
    location_data = get_ip_info()
    api_url = f'http://worldtimeapi.org/api/timezone/{location_data.timezone}'
    response = requests.get(api_url)
    data = {}

    if response.status_code == requests.codes.ok: # Make sure the api request succeeded
        data = json.loads(response.text) # Parse json response
        datetime_data = parse(data["datetime"]) # Parse the formatted datetime string
        hours = str(datetime_data.hour).rjust(2, '0') # Pad hours string with zeros if needed
        minutes = str(datetime_data.minute).rjust(2, '0') # Pad minutes string with zeros if needed
        ret.time = f"{hours}:{minutes}"
        ret.timezone = data['abbreviation']

    return ret