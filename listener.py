import os
import re
from weather_api import WeatherAPI


class Listener(object):
    """docstring for Listener"""
    def __init__(self):
        return

    def handle_event(self, event):
        return

class WeatherBot(Listener):
    """docstring for WeatherBot"""

    def __init__(self, name):
        self.name = name
        # Set the weather API key for env vars
        self.api_key = "&APPID=".format(os.environ.get('APPID'))
        return

    def handle_event(self, event):
        print "{} is handling event {}".format(
            type(self).__name__,
            event)

        # Access the dict key/value with a get so it doesn't throw an exception
        msg_data = event.data.get("data")

        if msg_data.startswith(self.name):
            if "weather" in msg_data:
                pattern = "^(.*)\s(.*)\s(\d*)\s"
                groups = re.findall(pattern,msg_data)
                location = groups[0][2]
                self.do_weather(location)
        else:
            return
        return

    def do_weather(self, location):
        WeatherApi.get_weather(self.api_key,location)
