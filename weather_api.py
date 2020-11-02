'''API wrapper class'''
# pylint: disable=I0011,C0103
import json
import os
import pprint
import requests

class WeatherAPI(object):
    """docstring for WeatherAPI"""

    @staticmethod
    def get_weather(apikey, location):
        '''Wrapper function for getting weather by zipcode'''
        # OpenWeatherMap call
        # uri = "http://api.openweathermap.org/data/2.5/weather?zip={},us{}".format(location, apikey)
        # Wunderground call
        # uri = "http://api.wunderground.com/api/{}/conditions/q/{}.json".format(apikey, location)
        # OpenWeatherMap 2020 call
        uri = "https://community-open-weather-map.p.rapidapi.com/weather"
        callback = "test"
        # print("WeatherAPI uri: ", uri)
        # querystring = {"lat":"0","lon":"0","callback":"test","id":"2172797","lang":"null","units":"imperial","q":"London,uk"}
        querystring = {"lat":"0","lon":"0","callback":callback,"id":"2172797","lang":"null","units":"imperial","q":location}
        headers = {
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
            'x-rapidapi-key': apikey
            }
        resp = requests.request("GET", uri, headers=headers, params=querystring)

        return json.loads(resp.text.strip(callback).strip('(').rstrip(')'))

        #resp = resp.strip([''.join(callback,'(')])
        #resp = resp.rstrip(')')
        # Function stub for testing
        # This is a hardcoded sample json response from the API endpoint
        # response = 'test({"coord":{"lon":-0.13,"lat":51.51},"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}],"base":"stations","main":{"temp":62.26,"feels_like":54.03,"temp_min":61,"temp_max":64.4,"pressure":1000,"humidity":82},"visibility":10000,"wind":{"speed":18.34,"deg":230},"clouds":{"all":90},"dt":1604270626,"sys":{"type":1,"id":1414,"country":"GB","sunrise":1604213674,"sunset":1604248411},"timezone":0,"id":2643743,"name":"London","cod":200})'
        # pp.pprint(type(response))
        # pp.pprint(response)

        # return json.loads(resp)

if __name__ == '__main__':
    apikey = os.environ.get("OPENWEATHER_API_KEY","")
    pp = pprint.PrettyPrinter()
    # resp = WeatherAPI.get_weather(apikey,'Palo Alto, ca, usa')
    # pp.pprint(resp)
    # resp = WeatherAPI.get_weather(apikey,'Alameda,ca,usa')
    # pp.pprint(resp)
    resp = WeatherAPI.get_weather(apikey,'london, uk')
    pp.pprint(type(resp))
    pp.pprint(resp)
    pp.pprint(resp["main"]["feels_like"])

