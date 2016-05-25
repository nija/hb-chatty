'''Artisinal chat bot'''
# pylint: disable=I0011,C0103
import json
import urllib
import urllib2
import random


# response = urllib2.urlopen('http://localhost:5001/api/users')
# html = response.read()
# print html

server_path = 'http://localhost:5001/api'
bot_name = 'Pyro'
bot_user_id = 0
bot_room_ids = [1]
bot_responses = ["PYROOOOOOOO!"]
# class CLI_Chat_Bot(object):
#   '''Chatbot to interact with a chat via an API'''

def get_user_info():

    response = urllib2.urlopen('{}/users'.format(server_path))
    jason = json.loads(response.read())
    j_list = jason["users"]
    for index, person in enumerate(j_list):
        if person["name"] == bot_name:
            bot_user_id = person["user_id"]
            print index, ": ", person

# If the user doesn't exist, create it
# curl --data "name=Pyro" http://localhost:5001/api/users


    # if there is a new message, parse it
    # response = urllib2.urlopen(server_path,
    #            '/api/rooms/1/messages')
def get_chat_history_all():
    '''Gets all messages'''
    room_id = 1
    room_attr = "messages"
    response = urllib2.urlopen('{}/rooms/{}/{}'.format(
                       server_path, room_id, room_attr))
    jason = json.loads(response.read())
    j_list = jason[room_attr]
    return j_list

def get_chat_history_by_time():
    '''Checks for a new chat message'''
    # if there is a new message, parse it
    # print self.get('/api/rooms/1/messages')

    # test_app = TestApp(app)
    # resp = test_app.get('/admin')
    # self.assertEqual(resp.status_code, 200)

def parse_chat_message(json_message):
    '''Takes a single JSON messages and acts upon it. 
    Responds to:
    '''
    print type(json_message), json_message
    msg_data = json_message["data"]
    print msg_data
    if bot_name in msg_data and bot_name != json_message["user_name"]:
        if "weather" in msg_data:
            print "{} - Getting weather".format(bot_name)
            # post_chat_message("{} - Getting weather".format(bot_name))
        else:
            print "Hello {}. I am {}".format(json_message["user_name"], bot_name)
            # post_chat_message("Hello {}. I am {}".format(json_message["user_name"], bot_name))


    # values = {'name' : 'Michael Foord',
    #           'location' : 'Northampton',
    #           'language' : 'Python' }
    #
    # data = urllib.urlencode(values)
    # req = urllib2.Request(url, data)
    # response = urllib2.urlopen(req)
    # the_page = response.read()

def post_chat_message(chat_message):
    '''Takes in a string to post'''

    values = {'user_id': user_id, 'data': chat_message }
    data = urllib.urlencode(values)
    print data
    # post_response = urllib2.urlopen('{}/rooms/{}/{}'.format(
       #                  server_path, room_id, room_attr),
    #                   data)


# get_chat_history_all()
# print type(jason), len(jason), jason
# print type(j_list), len(j_list), j_list


# get_user_info()
ja_list = get_chat_history_all()
parse_chat_message(ja_list[-1])
















