'''Artisinal chat bot'''
# pylint: disable=I0011,C0103
import json
import urllib2
#from unittest import TestCase
from flask import Flask, jsonify
from flask.ext.webtest import TestApp
from model import MyJSONEncoder

# ====== App Start-up ======
# Create a Flask app
app = Flask(__name__)
db = SQLAlchemy()
chat_server_uri = "http://localhost:5001"
db_uri_test = "postgresql:///bot_db_test"
db_uri_prod = "postgresql:///bot_db"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri_test
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up the secret key needed for session and debug-toolbar
app.secret_key = 'BotALot_like_Camalot_but_not'

db.app = app
db.init_app(app)
# ====== END App Start-up ======


# ====== Create an Artisinal, Free-Range Bot ======

class Chattybot(TestApp):
    '''Docstring for Chatterbox'''

    def __init__(self, app, db, name, server_uri):
        super(Chattybot, self).__init__(app)
        self.name = name
        self.server_uri = server_uri
        self.last_updated = 0

    def get_chat_history_all(self):
        '''Gets all messages'''
        # if there is a new message, parse it
        print self.get('/api/rooms/1/messages')

        # test_app = TestApp(app)
        # resp = test_app.get('/admin')
        # self.assertEqual(resp.status_code, 200)

   def get_chat_history_by_time(self):
        '''Checks for a new chat message'''
        # if there is a new message, parse it
        print self.get('/api/rooms/1/messages')

        # test_app = TestApp(app)
        # resp = test_app.get('/admin')
        # self.assertEqual(resp.status_code, 200)

    def parse_chat_message(self, json_message):
        '''Takes a single JSON messages and acts upon it'''

    def post_chat_message(self, chat_message):
        '''Takes in a string to post'''

# ====== END Artisinal, Free-Range Bot ======

if __name__ == "__main__":
    '''polling occurs here'''

    app.json_encoder = MyJSONEncoder
    bot_name = "Merida Meerkat"
    chatty = Chattybot(app=app, db=db, name=bot_name, server_uri=chat_server_uri)
    app.run(port=5002)
    print "\n    {} Lives!!\n\n".format(bot_name)

    chatty.get_chat_history_by_time()
