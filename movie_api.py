# '''API wrapper class'''
# pylint: disable=I0011,C0103
import pprint
import json
import urllib
import urllib2

class MovieAPI(object):
    """docstring for NetflixRouletteAPI"""

    @staticmethod
    def get_plot(title_keywords):
        '''Wrapper function for getting a movie plot by title'''

        # The Open Movie Database call
        print title_keywords
        values = {"t":title_keywords}
        print "values dict: ", values
        value = urllib.urlencode(values)
        uri = "http://www.omdbapi.com/?{}&plot=full".format(value)
        print "uri is ", uri
        response = urllib2.urlopen(uri)
        resp = json.loads(response.read())

        # Function stub for testing
        # This is a hardcoded sample json response from API endpoint
        # response = '{"unit":7474,"show_id":70153391,"show_title":"The Boondocks","release_year":"2005","rating":"4.0","category":"TV Shows","show_cast":"Regina King, John Witherspoon, Cedric Yarbrough, Gary Anthony Williams, Jill Talley, Gabby Soleil","director":"","summary":"Based on the comic strip by Aaron McGruder, this satirical animated series follows the socially conscious misadventures of Huey Freeman, a preternaturally smart 10-year-old who relocates from inner-city Chicago to the suburbs.","poster":"http:\/\/netflixroulette.net\/api\/posters\/70153391.jpg","mediatype":1,"runtime":"20 min"}'
        # resp = json.loads(response)
        print resp
        return resp

if __name__ == '__main__':
    pp = pprint.PrettyPrinter()
    # resp = get_all_data('House')
    # print type(resp)
    # pp.pprint(resp)

    resp = MovieAPI.get_plot('grace and frankie')
    pp.pprint(resp)


# $ curl 'http://www.omdbapi.com/?t=grace%20and%20frankie&plot=full'|jq .
# {
#   "Title": "Grace and Frankie",
#   "Year": "2015-",
#   "Rated": "TV-MA",
#   "Released": "08 May 2015",
#   "Runtime": "30 min",
#   "Genre": "Comedy",
#   "Director": "N/A",
#   "Writer": "Marta Kauffman, Howard J. Morris",
#   "Actors": "Jane Fonda, Lily Tomlin, Sam Waterston, Martin Sheen",
#   "Plot": "Finding out that their husbands are not just work partners, but have also been romantically involved for the last 20 years, two women with an already strained relationship try to cope with the circumstances together.",
#   "Language": "English",
#   "Country": "USA",
#   "Awards": "Nominated for 1 Golden Globe. Another 1 win & 14 nominations.",
#   "Poster": "http://ia.media-imdb.com/images/M/MV5BMTgwNTkyOTIwOF5BMl5BanBnXkFtZTgwMDg0MTQ1ODE@._V1_SX300.jpg",
#   "Metascore": "N/A",
#   "imdbRating": "8.1",
#   "imdbVotes": "9,416",
#   "imdbID": "tt3609352",
#   "Type": "series",
#   "Response": "True"
# }
