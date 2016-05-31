'''Everything about the Listener class and subclasses
WeatherBot
StoryBot
'''

import os
import re
import urllib
import urllib2
from weather_api import WeatherAPI
from event import Event
from bus import Bus

class Listener(object):
    """docstring for Listener"""
    def __init__(self, bus):
        return

    def handle_event(self, event):
        return

class WeatherBot(Listener):
    """docstring for WeatherBot"""

    def __init__(self, name, bus, user_id=1):
        self.name = name
        self.bus = bus
        # Set the weather API key from env vars
        self.api_key = "&APPID={}".format(os.environ.get('APPID'))
        self.server_path = 'http://localhost:5001/api'
        self.user_id = user_id

    def __repr__(self):
        return "<{} {} {}>".format(type(self).__name__, self.name, self.api_key)

    def set_user_id(self, user_id):
        '''adds a user id to weatherbot, needed for responses'''
        self.user_id = user_id

    def get_user_id(self):
        '''returns the user id weatherbot is using, needed for responses'''
        return self.user_id

    def handle_event(self, event):
        event_keywords = {
            'weather':['zipcode'],
            'story': [],
            'help': []}
        # print "WeatherBot is handling event {}".format(event)
        msg_data = event.data.get("data")

        # functions = ["weather", "zombie", "lyft"]

        # if msg_data.startswith("pyro"):
        #     for function in functions:
        #         if function in msg_data.contains(function):
        #             getattr(function, )

        if msg_data.startswith(self.name):
            if "weather" in msg_data:
                self.do_weather(event)
            elif "story" in msg_data:
                self.do_story(event)
        else:
            return

        return

    def do_weather(self, event):
        '''Parse and handle the weather requested event'''
        msg_data = event.data.get("data")
        requestor_name = event.data.get("user_name")
        room_id = event.data.get("room_id")
        pattern = "^(.*)\s(.*)\s(\d*)"
        groups = re.findall(pattern, msg_data)
        location = groups[0][2]
        weather_response = WeatherAPI.get_weather(self.api_key, location)
        # print event
        # print dir(event)
        # import pdb; pdb.set_trace()
        # print "\n\n\nWeather result:\n{}\n\n\n".format(weather_response)
        # self.bus.notify(Event(Event.Types.message_response_event), msg_response)
        wr_city = weather_response["name"]
        wr_main = weather_response["main"]
        wr_main_temp = wr_main["temp"]
        wr_weather = weather_response["weather"][0]
        wr_weather_desc = wr_weather["description"]


        # print "\n\n\nWeather result:\n{}, {} is {} degrees and experiencing {}\n\n\n".format(
        #     requestor_name,
        #     wr_city,
        #     wr_main_temp,
        #     wr_weather_desc)

        # Create the response payload
        message = "{}, {} is {} degrees and experiencing {}".format(
            requestor_name,
            wr_city,
            wr_main_temp,
            wr_weather_desc)

        # Call the response
        self.post_result(room_id, message)

    def post_result(self, room_id, message):
        '''Posts a message back to the server using the API'''
        endpoint = "{}/rooms/{}/messages".format(self.server_path, room_id)
        # endpoint0 = 'http://localhost:5001/api/rooms/1/messages'
        # message = 'postal_floral'
        values = {'user_id': '{}'.format(self.user_id), 'data': message}
        data = urllib.urlencode(values)
        # # import pdb; pdb.set_trace()
        print "\n\n\nPosting {} to {} with uid {}\n\n\n".format(data, endpoint, self.user_id)
        post_request = urllib2.Request(endpoint, data)
        # post_request = urllib2.Request(endpoint0, data)
        # import pdb; pdb.set_trace()
        # get_request = urllib2.Request('http://localhost:5001/api/rooms/1/messages')
        # get_response = urllib2.urlopen(get_request)
        # resp = get_response.read()
        # print resp


        post_response = urllib2.urlopen(post_request)
        response = post_response.read()
        print response

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






