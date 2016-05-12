'''Chat Engine'''
from datetime import datetime
from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import Message, Room, User, connect_to_db, db

# Log all the things
#TODO: Add loggers
import logging
from logging.handlers import RotatingFileHandler


# ====== Server Start-up ======
# Create a Flask app
app = Flask(__name__)

# Set up the secret key needed for session and debug-toolbar
app.secret_key = 'BalloonicornSmash'

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined



# Right now, we only have one room
main_chat = Room(name='Main Chat')
print main_chat
print dir(main_chat)
#db.session.add(main_chat)
#db.session.commit()

# Create the system user
#balloonicorn = User("Balloonicorn (System User)")
#db.session.add(balloonicorn)
#db.session.commit()

# ====== END Server Start-up ======

# ====== Routes Definitions ======

@app.route('/')
def index():
    '''Home page'''

    return render_template("home.html")

@app.route('/messages', methods=["GET"])
def show_message():
    '''
    Return jsonified messages from room_id
    '''
    return jsonify(main_chat.messages)

#TODO: Data sanitization
@app.route('/messages', methods=["POST"])
def create_message():
    # import pdb; pdb.set_trace()
    # Can call curl with --data-binary and retrieve with request.data
    print request.form
    data = request.form.get('data')
    uid = int(request.form.get('user_id'))
    print uid, data
    print type(uid), " uid: ", uid
    users = User.query.all()
    print users
    #user = User.query(user_id=uid)

    return jsonify({'hello': 'world'})




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    # Connect to the database
    # Test
    #connect_to_db(app, db_uri="postgresql:///ch")
    connect_to_db(app)
    # Prod
    #connect_to_db(app, db_uri="postgresql:///chatty")

    # Create our data schema
    db.create_all()


    print "\n    HEREEEEE!\n\n"
    app.run(port=5001)
