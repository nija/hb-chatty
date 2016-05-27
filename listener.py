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
        # Set the weather API key from env vars
        self.api_key = "&APPID={}".format(os.environ.get('APPID'))


    def __repr__(self):
        return "<{} {} {}>".format(type(self).__name__, self.name, self.api_key)


    def handle_event(self, event):
        # print "WeatherBot is handling event {}".format(event)
        msg_data = event.data.get("data")

        # functions = ["weather", "zombie", "lyft"]

        # if msg_data.startswith("pyro"):
        #     for function in functions:
        #         if function in msg_data.contains(function):
        #             eval(function, )

        if msg_data.startswith(self.name):
            if "weather" in msg_data:
                pattern = "^(.*)\s(.*)\s(\d*)"
                groups = re.findall(pattern, msg_data)
                location = groups[0][2]
                self.do_weather(location)
        else:
            return

        return

    def do_weather(self, location):
        data = WeatherAPI.get_weather(self.api_key, location)
        print "\n\n\nWeather result:\n{}\n\n\n".format(data)






