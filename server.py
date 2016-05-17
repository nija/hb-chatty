'''Chat Engine'''
# pylint: disable=I0011,C0103
from datetime import datetime
from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import Message, ModelMixin, MyJSONEncoder, Room, User, connect_to_db, db, seed_once, seed_force

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

# ====== END Server Start-up ======

# ====== Routes Definitions ======

# Show homepage
@app.route('/')
def index():
    '''Home page'''

    return render_template("home.html")



######  API calls  ######

# Get the list of all rooms
@app.route('/api/rooms', methods=["GET"])
def show_all_rooms():
    '''
    Return jsonified rooms
    '''
    # We only have one room; this is niiiiice
    rooms = Room.query.all()
    serialize_str = ''
    for room in rooms:
        serialize_str = repr(room.serialize()) + serialize_str
    print serialize_str
    return jsonify({'rooms': serialize_str})

# Get a specific room
@app.route('/api/rooms/<int:room_id>', methods=["GET"])
def show_room(room_id):
    '''Return jsonified room from passed in room_id'''
    main_room = db.session.query(Room).get(room_id)
    # print main_room
    return jsonify(main_room)

# Get a specific room's messages
@app.route('/api/rooms/<int:room_id>/messages', methods=["GET"])
def show_room_messages(room_id):
    '''
    Return jsonified messages from room_id
    '''
    # We only have one room; this is niiiiice
    print "\n\nIn show_room_messages"
    main_room = db.session.query(Room).get(room_id)
    print main_room
    # print main_room.messages
    msgs = main_room.messages_as_json()
    # msg = msgs[0]
    # message_list = [ msg.serialize() for msg in main_room.messages]
    # serialize_str = ''
    # serialize_str = '['
    # for msg in msgs:
    #     serialize_str += repr(msg.serialize())
    # for i, msg in enumerate(msgs):
    #     serialize_str += jsonify(i = msg)
    # serialize_str += ']'
    # return_dict = {}
    # for msg in main_room.messages:
    #     return_dict = dict(msg)
    # return jsonify(return_dict)
    # print serialize_str
    # print "\n\n\tmsg type:", type(msgs[0]), "\n\n\tmsg:", msgs[0]
    # print "\n\n\tmsgs type:", type(msgs), "\n\n\tmsgs:", msgs

    jjson = jsonify({"messages" : msgs})
    print jjson

    return jjson
    # return jsonify({"messages": [{
    #                     "message_id": 100,
    #                     "data": "fake",
    #                     "user_id": 1,
    #                     "room_id": 1
    #                     }]
    #                 })
    # # return jsonify({"messages": msgs})

# Post a message
#TODO: Data sanitization
@app.route('/api/rooms/<int:room_id>/messages', methods=["POST"])
def create_room_message(room_id):
    '''Create a Message object from the POST data'''
    # import pdb; pdb.set_trace()
    # Can call curl with --data-binary and retrieve with request.data
    # API test: curl --data "data=bar&user_id=1" http://localhost:5001/messages
    # print request.form
    main_room = db.session.query(Room).get(room_id)
    # print main_room
    data = request.form.get('data')
    uid = int(request.form.get('user_id'))
    # print data
    # print type(uid), " uid: ", uid
    user = db.session.query(User).get(uid)
    msg = Message(user=user, room=main_room, data=data)
    db.session.add(msg)
    db.session.commit()
    msgs = Message.query.order_by(Message.message_id).all()
    #print "\nMessages:\n", msgs
    msg = msgs[-1]

    return jsonify(msg.serialize())
    #return jsonify({'hello': 'world'})

# Get a specific room's users
@app.route('/api/rooms/<int:room_id>/users', methods=["GET"])
def show_room_users(room_id):
    '''
    Return jsonified users from room_id
    '''
    # We only have one room; this is niiiiice
    main_room = db.session.query(Room).get(room_id)
    users = main_room.users
    serialize_str = ''
    for user in users:
        serialize_str = repr(user.serialize()) + serialize_str
    print serialize_str
    return jsonify({'users': serialize_str})


# Join a specific room with a given user
@app.route('/api/rooms/<int:room_id>/users', methods=["POST"])
def create_room_users(room_id):
    '''
    Have a user join a room using the user_id in the POST data
    '''
    # import pdb; pdb.set_trace()
    # Can call curl with --data-binary and retrieve with request.data
    # API test: curl --data "user_id=1" http://localhost:5001/messages
    # print request.form
    main_room = db.session.query(Room).get(room_id)
    # print main_room
    uid = int(request.form.get('user_id'))
    # print data
    # print type(uid), " uid: ", uid
    user = db.session.query(User).get(uid)
    db.session.add(main_room.join_room(user))
    db.session.commit()
    return show_room_users(room_id)


# Leave a specific room with a given user
#FIXME: This doesn't currently work
@app.route('/api/rooms/<int:room_id>/users/leave', methods=["POST"])
def remove_room_users(room_id):
    '''
    Have a user leave a room using the user_id in the POST data
    '''
    exit(1)
    # import pdb; pdb.set_trace()
    # Can call curl with --data-binary and retrieve with request.data
    # API test: curl --data "data=bar&user_id=1" http://localhost:5001/messages
    # print request.form
    main_room = db.session.query(Room).get(room_id)
    # print main_room
    uid = int(request.form.get('user_id'))
    # print data
    # print type(uid), " uid: ", uid
    user = db.session.query(User).get(uid)
    db.session.delete(main_room.leave_room(room=main_room, user=user))
    db.session.commit()
    # Debug below
    show_room_users(room_id)
    return jsonify({'left': True})

# Get the list of all users
@app.route('/api/users', methods=["GET"])
def show_all_users():
    '''
    Return jsonified users
    '''
    users = User.query.all()
    serialize_str = ''
    for user in users:
        serialize_str = repr(user.serialize()) + serialize_str
    print serialize_str
    return jsonify({'users': serialize_str})


# Create a user
# API test: curl --data "name=username" http://localhost:5001/api/users
@app.route('/api/users', methods=["POST"])
def create_user():
    '''Return jsonified user from passed in form data'''
    #user = db.session.query(User).get(user_id)
    # print user

    name = request.form.get('name')
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    users = User.query.order_by(User.created_at).all()
    # print users
    user = users[-1]

    return jsonify(user.serialize())

# Get a specific user
@app.route('/api/users/<int:user_id>', methods=["GET"])
def show_user(user_id):
    '''Return jsonified user from passed in user_id'''
    user = db.session.query(User).get(user_id)
    # print user
    return jsonify(user.serialize())







if __name__ == "__main__":

    # Connect to the database
    # Test
    #connect_to_db(app, db_uri="postgresql:///ch")
    connect_to_db(app)
    # Prod
    #connect_to_db(app, db_uri="postgresql:///chatty")

    # Override the default JSONEncoder so the custom one knows how to handle
    # our classes
    app.json_encoder = MyJSONEncoder

    # Create our data schema and default objects if needed
    seed_once(app)

    # Right now, we only have one room and one user in that room

    print "\n    HEREEEEE!\n\n"

    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    # Leave this as the last step since we don't want random restarts before now
    app.debug = True
    # app.debug = False

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(port=5001)















