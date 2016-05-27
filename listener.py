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
        print "WeatherBot is handling event {}".format(event)
        msg_data = event.data.get("data")
        pattern = "^(.*)\s(.*)\s(\d*)\s"

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


    # def handle_event(self, event):
    #     '''Is this an event addressed to us?
    #     If so, handle it. If not, toss it'''
    #     # print "{} is handling event {}".format(
    #     #     type(self).__name__,
    #     #     event)

    #     # Access the dict key/value with a get so it doesn't throw an exception
    #     msg_data = event.data.get("data")

    #     # Parse the message data
    #     # Must be of the form:
    #     #   bot_name weather zipcode
    #     # If the message is addressed to us,
    #     if msg_data.startswith(self.name):
    #         # If the message contains the keyword weather
    #         if "weather" in msg_data:
    #             # Parse the message
    #             print "{} is handling event {}".format(
    #                 type(self).__name__,
    #                 event)
    #             pattern = "^(.*)\s(.*)\s(\d*)\s"
    #             groups = re.findall(pattern, msg_data)
    #             print msg_data
    #             print groups
    #             import pdb; pdb.set_trace()
    #             location = groups[0][2]
    #             self.do_weather(location)
    #     else:
    #         return
    #     return

    def do_weather(self, location):
        data = WeatherAPI.get_weather(self.api_key, location)
        print "\n\n\nWeather result:\n{}\n\n\n".format(data)






