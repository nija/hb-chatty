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
from threading import Timer
from weather_api import WeatherAPI
from movie_api import MovieAPI
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
            ngram = 6,
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
            'movie': ['title'],
            'story': [],
            'help': []}
        # print "SparkleBot is handling event {}".format(event)
        msg_data = event.data.get("data")

        # If we posted the message, ignore it
        if event.data.get('user_id') == self.user_id:
            return

        # TODO: I feel the below code should work to find the function to call
        # event_keywords = {"weather":['zipcode'], "story":[], "help":[], "zombie":[]}

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
        if self.name.lower() in msg_data.lower():
            if msg_data.startswith(('hello', 'Hello', 'hi', 'Hi', 'Greetings', 'greetings', 'hiya',
                                    'Hiya')):
                self.do_greeting(event)
            elif msg_data.startswith(('thank you', 'Thank you', 'thanks', 'Thanks', 'ty', 'TY')):
                self.do_welcome_response(event)

            # Functional responses
            elif msg_data.lower().startswith(self.name.lower()):
                if "weather" in msg_data:
                    self.do_weather(event)
                elif "story" in msg_data:
                    self.do_story(event)
                elif "movie" in msg_data:
                    self.do_movie(event)
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

        # Post the response
        self.post_result(room_id, message)
        return message

    def do_movie(self, event):
        # print "doin' le MOVIE"       
        # pp = pprint.PrettyPrinter()
        msg_data = event.data.get('data')
        requestor_name = event.data.get('user_name')
        room_id = event.data.get('room_id')
        # Process the requested title
        title_keywords = ' '.join(msg_data.split()[2:]).strip()
        # pp.pprint(title_keywords)
        # print "Parsing complete -", title_keywords
        movie_response = MovieAPI.get_plot(title_keywords)
        # pp.pprint(movie_response)

    # {u'Actors': u'Jane Fonda, Lily Tomlin, Sam Waterston, Martin Sheen',
    #  u'Awards': u'Nominated for 1 Golden Globe. Another 1 win & 14 nominations.',
    #  u'Country': u'USA',
    #  u'Director': u'N/A',
    #  u'Genre': u'Comedy',
    #  u'Language': u'English',
    #  u'Metascore': u'N/A',
    #  u'Plot': u'Finding out that their husbands are not just work partners, but have also been romantically involved for the last 20 years, two women with an already strained relationship try to cope with the circumstances together.',
    #  u'Poster': u'http://ia.media-imdb.com/images/M/MV5BMTgwNTkyOTIwOF5BMl5BanBnXkFtZTgwMDg0MTQ1ODE@._V1_SX300.jpg',
    #  u'Rated': u'TV-MA',
    #  u'Released': u'08 May 2015',
    #  u'Response': u'True',
    #  u'Runtime': u'30 min',
    #  u'Title': u'Grace and Frankie',
    #  u'Type': u'series',
    #  u'Writer': u'Marta Kauffman, Howard J. Morris',
    #  u'Year': u'2015\u2013',
    #  u'imdbID': u'tt3609352',
    #  u'imdbRating': u'8.1',
    #  u'imdbVotes': u'9,416'}
        movie_title = movie_response.get('Title')
        movie_writer = movie_response.get('Writer').split(',')[0]
        movie_plot = movie_response.get('Plot').strip()

        # Create the response payload
        message = "{}, '{}' was primarily written by {} and the plot summary is: {}".format(
            requestor_name,
            movie_title,
            movie_writer,
            movie_plot)

        # pp.pprint(message)

        # Post the response
        self.post_result(room_id, message)
        return message

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
    responses = ([
                 ])

    def __init__(self, name, bus, user_id=1):
        self.name = name
        self.bus = bus
        self.user_id = user_id
        self.timer = RepeatedTimer(1, hello, "World")

    def __repr__(self):
        return "<{} {} {} {}>".format(
                                      type(self).__name__,
                                      self.name,
                                      self.user_id,
                                      self.server_path)

    def get_user_id(self):
        '''returns the user id SparkleBot is using, needed for responses'''
        return self.user_id

    def set_user_id(self, user_id):
        '''adds a user id to SparkleBot, needed for responses'''
        self.user_id = user_id

    def do_babble(self):
        pass

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


class RepeatedTimer(object):
    '''General purpose utility timer using basic threading'''
    def __init__(self, interval_in_seconds, function_to_call, *args, **kwargs):
        self._timer = None
        self.interval = interval_in_seconds
        self.function = function_to_call
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            # Create a thread timer to keep close and private
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False




if __name__ == '__main__':
    bus = Bus()
    sparkle = SparkleBot("sparkle", bus)

    weather_event = Event(
                   Event.Types.message_created_event,
                   {"room_id":1, "data": "Pyro weather 94301", 'user_name': 'Balloonicorn', "user_id": 1})
    w_out = sparkle.do_weather(weather_event)
    print w_out


    movie_event = Event(
                   Event.Types.message_created_event,
                   {"room_id":1, "data": "Pyro movie grace and frankie", 'user_name': 'Balloonicorn', "user_id": 1})
    m_out = sparkle.do_movie(movie_event)
    print m_out




