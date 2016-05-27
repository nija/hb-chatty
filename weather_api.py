'''API wrapper class'''
# pylint: disable=I0011,C0103
import json
import urllib
import urllib2

class WeatherAPI(object):
	"""docstring for WeatherAPI"""

	@staticmethod
	def get_weather(api_key, location)
	result = urllib2.urlopen("http://api.openweathermap.org/data/2.5/weather?zip={},us{}".format(location, api_key)
		