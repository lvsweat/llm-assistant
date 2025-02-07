from utils import *
import os

def get_weather(country: str, city: str, state: str = '') -> str:
    """
    Tool function to get the weather at a specified location

    Args:
        country (string): The country to get weather for
        city (string): The city to get weather for
        state (string): The state to get weather for

    Returns:
        str: The formatted approximate temperature at the specified location or nothing if the call was unnecessary
    """

    ret = ""
    current_weather = weather()

    if (country == '' and city == '' and state == ''):
        current_weather = get_weather_from_ip()
    else:
        coordinates = resolve_lat_and_long(country, city, state)
        current_weather = get_weather_from_coords(coordinates)

    ret = f"{current_weather.tempurature}{current_weather.unit}"
    print(f"get_weather result: {ret}")
    return ret

def get_time(country: str, city: str, state: str = '') -> str:
    """
    Tool function to get the time at a specified location

    Args:
        country (string): The country to get the time for
        city (string): The city to get the time for
        state (string): The state to get the time for

    Returns:
        str: The formatted current time at the provided location or locally if no location is provided.
    """

    ret = ""
    current_time = time()

    if (country == '' and city == '' and state == ''):
       current_time = get_time_from_ip()
    else:
        coordinates = resolve_lat_and_long(country, city, state)
        current_time = get_time_from_coords(coordinates)

    ret = f"{current_time.time} {current_time.timezone}"
    print(f"get_time result: {ret}")
    return ret

def save_file(file_name: str, contents: str) -> bool:
    """
    Tool call to save information to a file

    Args:
        file_name (string): The name of the file including the file extension to save information to
        contents (string): The information/contents to save to the file

    Returns:
        bool: True if the file save succeeded, or False if the file save failed
    """
    try:
        file = open(file_name, 'w')
        file.write(contents)
        file.close()
    except OSError as e:
        return False

    return True