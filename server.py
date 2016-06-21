'''Chat Engine'''
# pylint: disable=I0011,C0103

# ====== Imports ======
# Standard imports
import bleach
from datetime import datetime
import json
import os
import pprint
# Flask and related imports
from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, send_from_directory, session
# from flask_debugtoolbar import DebugToolbarExtension
# Custom imports
from bus import Bus
from event import Event
from listener import SparkleBot
from model import Message, MyJSONEncoder, Room, User, connect_to_db, db, seed_once, seed_force

# Log all the things
#TODO: Add loggers
# import logging
# from logging.handlers import RotatingFileHandler





# ====== Server Start-up ======
# Create a Flask app
app = Flask(__name__)

# Set up the secret key needed for session and debug-toolbar
app.secret_key = 'BalloonicornSmash'

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

# Create an event bus
bus = Bus()

sparklebot_name = 'Pyro'

sparklebot = SparkleBot(name=sparklebot_name, bus=bus)

# Register our new bot with the bus as a listener for
# any Event.Types.message_created_event that are emitted
bus.register(sparklebot, Event.Types.message_created_event)


# ====== END Server Start-up ======



# ====== Routes Definitions ======

######  Flask Routes  ######
# Show homepage
@app.route('/')
def index():
    '''Home page'''

    return render_template("home.html")

@app.route('/favicon.ico')
def serve_favicon():
    '''Serve our favicon'''
    return send_from_directory(os.path.join(app.root_path, 'static/img'), 'favicon.ico')

@app.route('/ping')
def serve_ping():
    '''Serve a basic healthcheck'''
    room=Room.query.get(1)

    if room.name:
        db_status = "DB reachable"
    else:
        db_status = "DB unreachable"

    return render_template('ping.html',
                           db_status=db_status)

@app.route('/healthcheck')
def serve_healthcheck():
    '''Serve a monitoring healthcheck'''

    room=Room.query.get(1)
    if room.name:
        db_status = "DB reachable"
    else:
        db_status = "DB unreachable"

    app_name = '{}.{}'.format(app.name, app.import_name)
    app_db = '{}'.format(app.config['SQLALCHEMY_DATABASE_URI'])
    app_location = '{}'.format(app.root_path)
    app_extensions = '{}'.format(app.extensions)
    # Be rude and use a protected function
    # pp = pprint.PrettyPrinter()
    app_endpoints = '{}'.format(app.url_map._rules_by_endpoint)
    # app_endpoints = pp.pformat(app.url_map._rules_by_endpoint)
    # app_endpoints = json.dumps(app.url_map._rules_by_endpoint)

    num_rooms = len(Room.query.all())
    num_users = len(User.query.all())

    return render_template('healthcheck.html',
                           db_status=db_status,
                           app_name=app_name,
                           app_db=app_db,
                           app_location=app_location,
                           app_extensions=app_extensions,
                           app_endpoints=app_endpoints,
                           num_rooms=num_rooms,
                           num_users=num_users
                           )
    '''To force html to show the debug console:
    host = {{ type(self).__name__ }}<br>
    database = {{ app.database }}<br>'''


@app.route('/new')
def serve_new():
    '''Serve our favicon'''
    return send_from_directory(os.path.join(app.root_path,), 'new_home.html')

######  API Routes  ######

# Get the list of all rooms
@app.route('/api/rooms', methods=["GET"])
def show_all_rooms():
    '''
    Return jsonified rooms
    '''
    # We only have one room; this is niiiiice
    return jsonify({'rooms': [room.as_json() for room in Room.query.all()]})

# Get a specific room
@app.route('/api/rooms/<int:room_id>', methods=["GET"])
def show_room(room_id):
    '''Return jsonified room from passed in room_id'''
    return jsonify(db.session.query(Room).get(room_id).as_json())

# Get a specific room's messages
@app.route('/api/rooms/<int:room_id>/messages', methods=["GET"])
def show_room_messages(room_id):
    '''
    Return jsonified messages from room_id
    '''
    default_limit_responses = 15
    room = db.session.query(Room).get(room_id)

    # If called with a time stamp
    last_updated = request.args.get("last_updated")

    # Set room_msgs to be the time range or the limit of the number of messages
    if last_updated:
        dt_last_updated = datetime.fromtimestamp(int(last_updated))
        # print type(dt_last_updated), dt_last_updated
        room_msgs = db.session.query(Message).filter(
            Message.room_id == room.room_id,
            Message.created_at > dt_last_updated).order_by(
            Message.created_at).all()
    else:
        room_msgs = db.session.query(Message).filter(
            Message.room_id == room.room_id).order_by(
            Message.created_at).all()

    # If called with a limit
    limit_responses = request.args.get("limit_responses")
    if not limit_responses:
        if len(room_msgs) > default_limit_responses:
            limit_responses = default_limit_responses * -1
        else:
            default_limit_responses = len(room_msgs) * -1
    else:
        limit_responses = int(limit_responses) * -1

    # print "\n\n\t", type(limit_responses), limit_responses
    # print "\n\n\t", type(room_msgs), len(room_msgs), room_msgs[limit_responses:]
    return jsonify({"messages" : [msg.as_json() for msg in room_msgs[limit_responses:]]})

# Post a message
@app.route('/api/rooms/<int:room_id>/messages', methods=["POST"])
def create_room_message(room_id):
    '''Create a Message object from the POST data'''
    # Can call curl with --data-binary and retrieve with request.data
    # API test: curl --data "data=Hi, I am Sally&user_id=3" http://localhost:5001/api/rooms/1/messages
    # print request.form

    #import pdb; pdb.set_trace()
    main_room = db.session.query(Room).get(room_id)
    data = request.form.get('data')
    data = bleach.clean(data)
    uid = int(request.form.get('user_id'))
    user = db.session.query(User).get(uid)
    # If nothing is left in the message, don't return anything
    # if data == '':
    #     return
    msg = Message(user=user, room=main_room, data=data)

    # Create the date fields using the database
    db.session.add(msg)
    db.session.commit()

    # Put the event on the bus
    print "Throwing message_created_event"
    bus.notify(Event(
        Event.Types.message_created_event, 
        msg.as_json()))


    # To access the newly created object
    # msgs = Message.query.order_by(Message.message_id).all()
    # msg = msgs[-1]

    return jsonify({"messages": main_room.messages_as_json()})

# Get a specific room's users
@app.route('/api/rooms/<int:room_id>/users', methods=["GET"])
def show_room_users(room_id):
    '''
    Return jsonified users from room_id
    '''
    return jsonify({'users': db.session.query(Room).get(room_id).users_as_json()})

# Join a specific room with a given user
@app.route('/api/rooms/<int:room_id>/users', methods=["POST"])
def create_room_users(room_id):
    '''
    Have a user join a room using the user_id in the POST data
    '''
    a_room = db.session.query(Room).get(room_id)
    uid = int(request.form.get('user_id'))
    user = db.session.query(User).get(uid)

    # If the user is not already in the room
    if not a_room.contains_user(user.user_id):
        # Add the user to the room
        db.session.add(a_room.join_room(user))
        db.session.commit()

        # Put the event on the bus
        print "Throwing user_joins_room"
        bus.notify(Event(
            Event.Types.user_joins_room_event, 
            {   'user_id':user.user_id,
                'user_name': user.name,
                'room_id': room_id}))

    # Return the current list of users in the room; re-use the function we
    # already have to do this
    return show_room_users(room_id)

# Leave a specific room with a given user
#FIXME: This doesn't currently work
# @app.route('/api/rooms/<int:room_id>/users/leave', methods=["POST"])
# def remove_room_users(room_id):
#     '''
#     Have a user leave a room using the user_id in the POST data
#     '''
#     exit(1)
#     # import pdb; pdb.set_trace()
#     # Can call curl with --data-binary and retrieve with request.data
#     # API test: curl --data "data=bar&user_id=1" http://localhost:5001/messages
#     # print request.form
#     main_room = db.session.query(Room).get(room_id)
#     # print main_room
#     uid = int(request.form.get('user_id'))
#     # print data
#     # print type(uid), " uid: ", uid
#     user = db.session.query(User).get(uid)
#     db.session.delete(main_room.leave_room(room=main_room, user=user))
#     db.session.commit()
#     # Debug below
#     show_room_users(room_id)
#     return jsonify({'left': True})

# Get the list of all users
@app.route('/api/users', methods=["GET"])
def show_all_users():
    '''
    Return jsonified users
    '''
    return jsonify({'users': [user.as_json() for user in User.query.all()]})

# Create a user
# API test: curl --data "name=username" http://localhost:5001/api/users
@app.route('/api/users', methods=["POST"])
def create_user():
    '''Return jsonified user from passed in form data'''
    # print request.form
    name = request.form.get('name')
    name = bleach.clean(name)
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    # users = User.query.order_by(User.created_at).all()

    # return jsonify(users[-1].as_json())

    return jsonify(user.as_json())

# Get a specific user
@app.route('/api/users/<int:user_id>', methods=["GET"])
def show_user(user_id):
    '''Return jsonified user from passed in user_id'''
    return jsonify(db.session.query(User).get(user_id).as_json())

# Get a specific user's rooms
@app.route('/api/users/<int:user_id>/rooms', methods=["GET"])
def show_user_rooms(user_id):
    '''Return jsonified user rooms from passed in user_id'''
    return jsonify({'rooms': db.session.query(User).get(user_id).rooms_as_json()})

# Get a specific user's messages
@app.route('/api/users/<int:user_id>/messages', methods=["GET"])
def show_user_messages(user_id):
    '''Return jsonified user messages from passed in user_id'''
    return jsonify({'messages': db.session.query(User).get(user_id).messages_as_json()})



# class ServerListener(Listener):
#     """docstring for ServerListener"""
#     def __init__(self, app, bus):
#         super(ServerListener, self).__init__()
#         self.app = app
#         self.bus = bus

if __name__ == "__main__":

    # Figure out which db to connect to
    db_uri = os.environ.get("DATABASE_URL","postgres:///travis_ci_test")
    # Test
    #connect_to_db(app, db_uri="postgresql:///travis_ci_test")
    # Prod
    #connect_to_db(app, db_uri="postgresql:///chatty")
    connect_to_db(app, db_uri)

    # Override the default JSONEncoder so the custom one knows how to handle
    # our classes
    app.json_encoder = MyJSONEncoder

    # Create our data schema and default objects if needed
    seed_once(app)


    # Tell our sparklebot which user to post messages as and which room
    # to frequent
    default_room = db.session.query(Room).get(1)
    # Get the sparklebot user object, creating it if need be
    sparklebot_check = User.query.filter(User.name == sparklebot_name)
    if not sparklebot_check.first():
        # print "\n\n\nCREATING SPARKLE BOT DB USER\n\n\n"
        # Create the user
        db.session.add(User(sparklebot_name))
        db.session.commit()
    sparklebot_user = sparklebot_check.first()
    sparklebot.set_user_id(sparklebot_user.user_id)
    # Add the user to the room if needed
    if not default_room.contains_user(sparklebot_user.user_id):
        # print "\n\n\nADDING SPARKLE BOT TO DEFAULT ROOM\n\n\n"
        db.session.add(default_room.join_room(sparklebot_user))
        db.session.commit()


    # Right now, we only have one room and one user in that room

    print "\n    HEREEEEE!\n\n"

    # DebugToolbarExtension requires debug=True before it will run correctly
    # Leave this as is because of the 'No handlers could be found for logger
    # "sqlalchemy.pool.QueuePool"' http 500 error that results when it is taken
    # out
    DEBUG = "NO_DEBUG" not in os.environ
    # app.debug = True
    app.debug = DEBUG

    # Set the port
    port = int(os.environ.get("PORT", 5001))

    # Allow more processes so there's enough wiggle room to handle multiple requests
    # Use the DebugToolbar
    # DebugToolbarExtension(app)
    app.run(host="0.0.0.0", port=port, processes=3)















