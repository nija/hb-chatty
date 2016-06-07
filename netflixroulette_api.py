# '''API wrapper class'''
# pylint: disable=I0011,C0103
import pprint
import json
import urllib
import urllib2
from NetflixRoulette import *

class NetflixRouletteAPI(object):
    """docstring for NetflixRouletteAPI"""

    @staticmethod
    def get_title(exact_match):
        '''Wrapper function for getting netflix by title'''
        # Netflix Roulette call
        resp = get_all_data(exact_match)

        # Function stub for testing
        # This is a hardcoded sample json response from API endpoint
        # response = '{"unit":7474,"show_id":70153391,"show_title":"The Boondocks","release_year":"2005","rating":"4.0","category":"TV Shows","show_cast":"Regina King, John Witherspoon, Cedric Yarbrough, Gary Anthony Williams, Jill Talley, Gabby Soleil","director":"","summary":"Based on the comic strip by Aaron McGruder, this satirical animated series follows the socially conscious misadventures of Huey Freeman, a preternaturally smart 10-year-old who relocates from inner-city Chicago to the suburbs.","poster":"http:\/\/netflixroulette.net\/api\/posters\/70153391.jpg","mediatype":1,"runtime":"20 min"}'
        # resp = json.loads(response)
        return resp

if __name__ == '__main__':
    pp = pprint.PrettyPrinter()
    # resp = get_all_data('House')
    # print type(resp)
    # pp.pprint(resp)
    resp = NetflixRouletteAPI.get_title('grace and frankie')
    pp.pprint(resp)