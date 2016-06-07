'''Everything about the Listener class and subclasses
RainbowBot
StoryBot
'''
# pylint: disable=I0011,C0103

import os
import re
import urllib
import urllib2
import pprint
from weather_api import WeatherAPI
from event import Event
from bus import Bus
from markov import Markov


class Listener(object):
    """docstring for Listener"""
    server_path = 'http://localhost:5001/api'
    def __init__(self, bus):

        return

    def handle_event(self, event):
        return

class SparkleBot(Listener):
    """docstring for SparkleBot"""

    def __init__(self, name, bus, user_id=1):
        self.name = name
        self.bus = bus
        # Set the weather API key from env vars
        # For openweathermap API key
        # self.api_key = "&APPID={}".format(os.environ.get('APPID'))
        # For Wunderground API key
        self.api_key = os.environ.get('WUNDERGROUND_API_KEY')
        # self.server_path = 'http://localhost:5001/api'
        self.user_id = user_id
        self.marky = Markov(
            limit = 600,
            ngram = 7,
            paths = ['static/markov_text/alice_in_wonderland.txt',
                    'static/markov_text/through_the_looking_glass.txt'])

    def __repr__(self):
        return "<{} {} {} {}>".format(type(self).__name__, self.name, self.user_id, self.server_path)

    def set_user_id(self, user_id):
        '''adds a user id to SparkleBot, needed for responses'''
        self.user_id = user_id

    def get_user_id(self):
        '''returns the user id SparkleBot is using, needed for responses'''
        return self.user_id

    def handle_event(self, event):
        event_keywords = {
            'weather': ['zipcode'],
            'story': [],
            'help': []}
        # print "SparkleBot is handling event {}".format(event)
        msg_data = event.data.get("data")

        # If we posted the message, ignore it
        if event.data.get('user_id') == self.user_id:
            return

        # TODO: I feel the below code should work to find the function to call
        # event_keywords = {"weather":['zipcode'], "story":[], "zombie":[]}

        # if msg_data.startswith(self.name):
        #     for method in event_keywords.keys():
        #         me = None
        #         if method in msg_data:
        #             try:
        #                 me = getattr(self,'do_{}'.format(method))
        #             except AttributeError:
        #                 raise NotImplementedError(
        #                     "Class '{}' does not implement '{}'".format(
        #                         type(self).__name__,
        #                         method)
        #             self.me(event)

        # Generic politeness responses
        if self.name in msg_data:
            if msg_data.startswith(('hello', 'Hello', 'hi', 'Hi', 'Greetings', 'greetings', 'hiya', 'Hiya')):
                self.do_greeting(event)
            elif msg_data.startswith(('thank you', 'Thank you', 'thanks', 'Thanks', 'ty', 'TY')):
                self.do_welcome_response(event)

            # Functional responses
            elif msg_data.startswith(self.name):
                if "weather" in msg_data:
                    self.do_weather(event)
                elif "story" in msg_data:
                    self.do_story(event)
                elif "help" in msg_data or "halp" in msg_data:
                    self.do_help(event, event_keywords)
            else:
                return
        return

    def do_greeting(self, event):
        '''Respond to a user's greeting'''
        requestor_name = event.data.get("user_name")
        room_id = event.data.get("room_id")
        message = "Hello {}".format(requestor_name)
        self.post_result(room_id, message)

    def do_welcome_response(self, event):
        '''Respond to a user's thanks'''
        requestor_name = event.data.get("user_name")
        room_id = event.data.get("room_id")
        message = "You are welcome, {}".format(requestor_name)
        self.post_result(room_id, message)

    def do_help(self, event, event_keywords):
        '''Posts a help message to the user'''
        requestor_name = event.data.get("user_name")
        room_id = event.data.get("room_id")
        build_response = '{}, here is what I can do: '.format(requestor_name)
        for iteration, key in enumerate(event_keywords.keys()):
            build_response += ' {}. {} {} {} '.format(
                iteration + 1, 
                self.name, 
                key, 
                ' '.join(event_keywords[key]))
        self.post_result(room_id, build_response)

    def do_story(self, event):
        '''Creates a story using the Markov chain functions'''
        requestor_name = event.data.get("user_name")
        room_id = event.data.get("room_id")
        message = "Sure {}. Here is your story, a la Lewis Carrol. {}".format(
            requestor_name,
            self.marky.tell_a_story())
        self.post_result(room_id, message)

    def do_weather(self, event):
        '''Parse and handle the weather requested event'''
        msg_data = event.data.get("data")
        requestor_name = event.data.get("user_name")
        room_id = event.data.get("room_id")
        pattern = "^(.*)\s(.*)\s(\d*)"
        groups = re.findall(pattern, msg_data)
        location = groups[0][2]
        weather_response = WeatherAPI.get_weather(self.api_key, location)

        # Parsing for OpenWeatherMap
        # pp = pprint.PrettyPrinter()
        # pp.pprint(weather_response)
        # wr_city = weather_response["name"]
        # wr_main = weather_response["main"]
        # wr_main_temp = wr_main["temp"]
        # wr_weather = weather_response["weather"][0]
        # wr_weather_desc = wr_weather["description"]
        # wr_main_temp_f = (wr_main_temp * (9/5.0)) - 459.67

        # Parsing for Wunderground
        # pp = pprint.PrettyPrinter()
        # wr = weather_response["current_observation"]
        # pp.pprint(wr)
        wr_city = weather_response["current_observation"]["display_location"]["city"]
        wr_main_temp_f = weather_response["current_observation"]["temperature_string"]
        wr_weather_desc = weather_response["current_observation"]["weather"].lower()

        # Create the response payload
        message = "{}, {} is {} and is {}".format(
            requestor_name,
            wr_city,
            wr_main_temp_f,
            wr_weather_desc)

        # return message
        # Post the response
        self.post_result(room_id, message)

    def post_result(self, room_id, message):
        '''Posts a message back to the server using the API'''
        endpoint = "{}/rooms/{}/messages".format(self.server_path, room_id)
        values = {'user_id': '{}'.format(self.user_id), 'data': message}
        data = urllib.urlencode(values)
        # print "\n\n\nPosting {} to {} with uid {}\n\n\n".format(data, endpoint, self.user_id)
        post_request = urllib2.Request(endpoint, data)
        post_response = urllib2.urlopen(post_request)
        response = post_response.read()
        # print response

class BabbleBot(Listener):
    """docstring for BabbleBot"""
        
    def __init__(self, name, bus, user_id=1):
        self.name = name
        self.bus = bus
        self.user_id = user_id


    def __repr__(self):
        return "<{} {} {} {}>".format(type(self).__name__, self.name, self.user_id, self.server_path)

    def get_user_id(self):
        '''returns the user id SparkleBot is using, needed for responses'''
        return self.user_id

    def set_user_id(self, user_id):
        '''adds a user id to SparkleBot, needed for responses'''
        self.user_id = user_id

    def post_result(self, room_id, message):
        '''Posts a message back to the server using the API'''
        endpoint = "{}/rooms/{}/messages".format(self.server_path, room_id)
        values = {'user_id': '{}'.format(self.user_id), 'data': message}
        data = urllib.urlencode(values)
        # print "\n\n\nPosting {} to {} with uid {}\n\n\n".format(data, endpoint, self.user_id)
        post_request = urllib2.Request(endpoint, data)
        post_response = urllib2.urlopen(post_request)
        response = post_response.read()
        # print response


# GET request
# req = urllib2.Request('http://www.voidspace.org.uk')
# response = urllib2.urlopen(req)

# POST requests
# url = 'http://www.someserver.com/cgi-bin/register.cgi'
# values = {'name' : 'Michael Foord',
#           'location' : 'Northampton',
#           'language' : 'Python' }
# data = urllib.urlencode(values)
# req = urllib2.Request(url, data)
# response = urllib2.urlopen(req)
# the_page = response.read()

# url = 'http://192.168.1.3/epreuves/WEB/epreuve2/page2.php'
# data = urllib.urlencode({'login' : 'MyLogin', 'password' : 'MyPassword'})
# req = urllib2.Request(url, data)
# response = urllib2.urlopen(req)
# d = response.read()
# print d


if __name__ == '__main__':
    bus = Bus()
    sparkle = SparkleBot("sparkle", bus)

    event1 = Event(
                   Event.Types.message_created_event,
                   {"room_id":1, "data": "Pyro weather 94301", "user_id": 123})

    out = sparkle.do_weather(event1)

    print out




