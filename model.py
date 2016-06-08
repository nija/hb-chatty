from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from datetime import datetime, timedelta
from pytz import timezone
import pytz
from flask.json import JSONEncoder
# from contextlib import suppress

# >>> from datetime import datetime, timedelta
# >>> from pytz import timezone
# >>> import pytz
# >>> utc = pytz.utc

# How long to persist data we care about
EXPIRE_DELTA = 2

# Create our database object
db = SQLAlchemy()



##############################################################################
# Mix-ins and support classes

class MyJSONEncoder(JSONEncoder):
    '''
    Override the default JSONEncoder class
    '''
    def default(self, obj):
        # Optional: convert datetime objects to ISO format
        # with suppress(AttributeError):
        #     return obj.isoformat()
        try:
            return obj.isoformat()
        except AttributeError:
            pass

        return dict(obj)

# Moved this to server.py
# app.json_encoder = MyJSONEncoder

##############################################################################
# Basic Classes

class Message(db.Model):
    '''
    Representation of a Message object
    Uses a global called EXPIRE DELTA to set default data retention
    '''
    # import pytz
    # from datetime import datetime
    # datetime.utcnow().replace(tzinfo = pytz.utc)
    # utc_dt = datetime.utcfromtimestamp(1143408899).replace(tzinfo=utc)
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.String(2048))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    expiry_at = db.Column(db.DateTime(timezone=True))
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.room_id'))
    # References
    # Multiple messages belong to a user
    user = db.relationship('User', backref=db.backref('messages', order_by=created_at))
    # Multiple messages belong to a room
    room = db.relationship('Room', backref=db.backref('messages', order_by=created_at))


    def __init__(self, user, room, data="This is a test message from a blue balloon"):
        self.data = data
        self.created_at = datetime.utcnow()
        self.created_at.replace(tzinfo=pytz.utc)
        self.expiry_at = self.created_at + timedelta(days=EXPIRE_DELTA)
        self.user_id = user.user_id
        self.room_id = room.room_id

    def __repr__(self):
        '''
        Return the string representation of the Message
        '''
        # return '\n<{} room.name="{}" user.name="{}" message_id={} data="{}" created_at={} expiry_at={}>'.format(
        #     type(self).__name__, self.room.name, self.user.name, self.message_id, self.data, self.created_at.isoformat(), self.expiry_at.isoformat())
        return '\n<{} room.name="{}" user.name="{}" message_id={} data="{}">'.format(
            type(self).__name__, self.room.name, self.user.name, self.message_id, self.data)

    def serialize(self):
        '''Serialize this'''
        return {
            'message_id': self.message_id,
            'data' : self.data,
            'created_at' : self.created_at.isoformat(),
            'expiry_at' : self.expiry_at.isoformat(),
            'user_id' : self.user_id,
            'user_name': self.user.name,
            'room_id' : self.room_id
        }

    def as_json(self):
        '''
        Another way to call serialize; included for consistency
        '''
        return self.serialize()


# class Log(db.Model):
#     '''
#     Representation of a Log object.
#     Uses a global called EXPIRE DELTA
#     '''
#     #TODO: Figure out if this is even needed 

#     log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     data = db.Column(db.String(2048))
#     created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     expiry_at = db.Column(db.DateTime)

#     def __init__(self, data="This is a test log from a blue balloon"):
#         self.data = data
#         self.created_at = datetime.utcnow()
#         self.expiry_at = self.created_at + timedelta(days=EXPIRE_DELTA)

#     def __repr__(self):
#         '''
#         Return the string representation of the Log
#         '''
#         return '\n<{} log_id={} data="{}" created_at={} expiry_at={}>'.format(
#             type(self).__name__, self.log_id, self.data, self.created_at, self.expiry_at)


class User(db.Model):
    """
    Representation of a User object
    """
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # References
    # Return the Room objects from the roomuser table ('secondary')
    rooms = db.relationship('Room',
                            secondary='room_user',
                            backref=db.backref('users'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        '''Return the string representation of the User'''
        return '\n<{} user_id={} name="{}" created_at={}>'.format(
            type(self).__name__, self.user_id, self.name, self.created_at)

    def serialize(self):
        '''Serialize this'''
        return {
            'user_id': self.user_id,
            'name' : self.name,
            'created_at' : self.created_at
        }

    def as_json(self):
        return self.serialize()

    def messages_as_json(self):
        '''Return user messages as a JSON list
        '''
        return [ msg.as_json() for msg in self.messages]

    def rooms_as_json(self):
        '''Return user's rooms as a JSON list
        '''
        return [ room.as_json() for room in self.rooms]


class Room(db.Model):
    """
    Representation of a Room object.
    NOTE: Add new rooms to db before adding things to the new rooms
    """
    room_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expiry_at = db.Column(db.DateTime)

    def __init__(self, name='main'):
        self.name = name

    def __repr__(self):
        '''Return the string representation of the User'''
        return '\n<{} room_id={} name="{}" created_at={} expiry_at={}>'.format(
            type(self).__name__, self.room_id, self.name, self.created_at, self.expiry_at)

    def serialize(self):
        '''Serialize this'''
        return {
            'room_id': self.room_id,
            'name' : self.name,
            'created_at' : self.created_at,
            'expiry_at' : self.expiry_at
        }

    def as_json(self):
        '''Another way to call serialize; included for consistency'''
        return self.serialize()

    def join_room(self, user):
        '''
        Takes a user, returns an RoomUser object that needs to be added and committed
        to the db.session
        '''
        joined = RoomUser(room=self, user=user)
        #TODO: Put in application logging
        #"Created association: {}{}{} \n".format(joined, self, user)
        return joined

    def contains_user(self, user_id):
        '''Is the user in the room? returns a boolean'''
        check_join = RoomUser.query.filter(
                        RoomUser.room_id == self.room_id,
                        RoomUser.user_id == user_id)
        if check_join.first():
            return True
        return False



    #FIXME: This doesn't work currently
    def leave_room(self, room, user):
        '''
        Takes a user and room, and deletes the right object...
        '''
        to_delete = RoomUser.query(
            RoomUser.room_id == room.room_id, 
            RoomUser.user_id == user.user_id).all()
        #TODO: Put in application logging
        #"Created association: {}{}{} \n".format(joined, self, user)
        return to_delete

    def messages_as_json(self):
        '''Return room messages as a JSON list
        '''
        return [ msg.as_json() for msg in self.messages]

    def users_as_json(self):
        '''Return room users as a JSON list
        '''
        return [ user.as_json() for user in self.users]


class RoomUser(db.Model):
    '''
    Relates the User and Room classes
    '''
    room_user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Foreign keys
    room_id = db.Column(db.Integer, db.ForeignKey('room.room_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow)

    # References
    # Multiple users belong to a room
    room = db.relationship('Room', backref=db.backref('room_user'))
    # Multiple rooms belong to a user
    user = db.relationship('User', backref=db.backref('room_user'))

    def __init__(self, room, user):
        '''Creates an association'''
        self.user_id = user.user_id
        self.room_id = room.room_id

    def __repr__(self):
        '''Returns a useful string representation of the room-user association'''
        return '\n<{} room_user_id={} room_id="{}" user_id="{}" time_stamp={}>'.format(
            type(self).__name__, self.room_user_id, self.room_id, self.user_id, self.time_stamp)

    def serialize(self):
        '''Serialize this'''
        return {
            'room_user_id': self.room_user_id,
            'room_id': self.room_id,
            'user_id': self.user_id,
            'time_stamp': self.time_stamp
        }

##############################################################################
# Helper functions & Data Model tests

# Set up the app if necessary
def seed_once(app):
    '''Create tables if none exist'''
    # Zomg, why did this take so long to figure out??
    # Test to see if our message table exists
    query1 = """
    SELECT count(relname)
    FROM pg_class
    WHERE relname = 'message'
    """
    db_cursor = db.session.execute(query1)
    row = db_cursor.fetchone()
    # Check to see if the table exists; 0 means to recreate everything
    if row[0] == 0:
        #import pdb; pdb.set_trace()
        # print "\n\n\tCreating the world\n\n"
        db.create_all()

        # Create our default room
        main_room = Room(name='Main')
        # print main_room
        # print dir(main_room)
        db.session.add(main_room)
        db.session.commit()
        main_room = db.session.query(Room).get(1)

        # Create the system user
        balloonicorn = User("Balloonicorn")
        db.session.add(balloonicorn)
        db.session.commit()
        balloonicorn = db.session.query(User).get(1)

        # Create the default anonymous user
        anonymouse = User("Anony Mouse")
        db.session.add(anonymouse)
        db.session.commit()
        anonymouse = db.session.query(User).get(2)

        # Add default users to room
        db.session.add(main_room.join_room(balloonicorn))
        db.session.add(main_room.join_room(anonymouse))
        db.session.commit()
        # print "\n\n\tOur world is complete!\n\n"
        # print balloonicorn, balloonicorn.rooms

    # else:      
        # print "\n\n\tOur world EXISTS!\n\tnothing to do!\n\n"


# Force a clean slate
def seed_force(app):
    # Make sure nothing exists
    # print 'dropping'
    db.drop_all()
    # print 'seed once...'
    seed_once(app)
    # print 'finished seed once'

def test_seed_once(app, db_uri):
    '''Create example data for the test database.'''
    connect_to_db(app, db_uri)

    # Get to a known good state
    seed_once(app)

    # Get users
    balloonicorn = db.session.query(User).get(1)

def test_create_get_users(app):
    '''Create and insert Users'''
    balloonicorn = db.session.query(User).get(1)
    # balloonicorn = User(name="Balloonicorn")
    grace = User(name="Grace Hopper")
    # db.session.add(balloonicorn)
    db.session.add(grace)
    db.session.commit()

def test_get_users(app):
    users = User.query.all()
    print "Users:\n", users

def test_join_room(app):
    check_fran = User.query.filter(User.name == 'Fran Allen')
    # import pdb; pdb.set_trace()
    # If Fran Allen doesn't exist
    if not check_fran.first():
        # Create Fran Allen
        print "Creating Fran Allen"
        fran = User(name='Fran Allen')
        db.session.add(fran)
        db.session.commit()

    main_room = db.session.query(Room).get(1)
    print "Got room {}".format(main_room)
    fran = User.query.filter(User.name == 'Fran Allen').first()
    # If the user is not already in the room
    if not main_room.contains_user(fran.user_id):
        # Add the user to the room
        db.session.add(main_room.join_room(fran))
        # db.session.add(main_room.join_room(balloonicorn))
        db.session.commit()
    print 'Room: {}\nUsers: {}'.format(main_room.room_id, main_room.users_as_json())

def test_get_rooms(app):
    ''' '''
    rooms = Room.query.all()
    room_users = RoomUser.query.all()
    print rooms
    print room_users

def test_create_get_messages(app):

    balloonicorn = db.session.query(User).get(1)
    grace = User.query.filter(User.name == 'Grace Hopper').first()
    main_room = db.session.query(Room).get(1)
    # import pdb; pdb.set_trace()
    a_message = Message(room=main_room, user=grace, data="Please cut off a nanosecond and send it over to me")
    b_message = Message(room=main_room, user=grace, data='I need something to compare this to. Could I please have a microsecond?')
    c_message = Message(room=main_room, user=grace, data='I had a running compiler and nobody would touch it... they carefully told me, computers could only do arithmetic; they could not do programs.')
    d_message = Message(room=main_room, user=grace, data="I've always been more interested in the future than in the past.")
    e_message = Message(room=main_room, user=grace, data='Life was simple before World War II. After that, we had systems.')
    f_message = Message(room=main_room, user=grace, data='A ship in port is safe; but that is not what ships are built for. Sail out to sea and do new things.')
    g_message = Message(room=main_room, user=grace, data='The wonderful thing about standards is that there are so many of them to choose from.')
    h_message = Message(room=main_room, user=grace, data="In pioneer days they used oxen for heavy pulling, and when one ox couldn't budge a log, they didn't try to grow a larger ox. We shouldn't be trying for bigger computers, but for more systems of computers.")
    i_message = Message(room=main_room, user=grace, data="It's easier to ask forgiveness than it is to get permission.")
    j_message = Message(room=main_room, user=grace, data='We must state relationships, not procedures.')
    k_message = Message(room=main_room, user=balloonicorn, data="Burn everything")
    db.session.add(a_message)
    db.session.add(b_message)
    db.session.add(c_message)
    db.session.add(d_message)
    db.session.add(e_message)
    db.session.add(f_message)
    db.session.add(g_message)
    db.session.add(h_message)
    db.session.add(i_message)
    db.session.add(j_message)
    db.session.add(k_message)
    db.session.commit()
    #TODO
    return Message.query.all()


#TODO: Turn these into asserts and put them into tests.py
def test_example_data(app, db_uri):
    '''Create example data for the test database.'''
    connect_to_db(app, db_uri)

    # Tests follow

    # Reset the world
    seed_force(app)

    # Try to get users
    # test_create_get_users(app)

    # Test user retrieval
    # test_get_users(app)

    # Test joining a room
    test_join_room(app)



    # Test room and room_user retrieval
    # rooms = Room.query.all()
    # room_users = RoomUser.query.all()
    # print rooms
    # print room_users
    #test_get_rooms(app)

    # Test message creation and retrieval
    #test_create_get_messages(app)


    #######
    # Test relationships

    print "User Messages\n=================================\n"
    users = User.query.all()
    for user in users:
        print "user.messages: ", user.messages
        print "user.rooms: ", user.rooms


    print "\n\nRoom Messages\n=================================\n"
    rooms = Room.query.all()
    for room in rooms:
        print "room.messages: ", room.messages
        print "room users: ", room.users


    print "\n\nAssociations\n=================================\n"
    room_users = RoomUser.query.all()
    for room_user in room_users:
        print "room_user: ", room_user
#====


# Default to connecting to the test db so we don't accidentally screw with our
# real db
def connect_to_db(app, db_uri="postgresql:///chatty"):
    '''
    Configure the database-app connection
    Takes an app and an optional db_uri
    '''
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

if __name__ == '__main__':
    '''
    As a convenience, if we run this module interactively, it will leave
    you in a state of being able to work with the database directly.
    from server import app
    '''
    from server import app 
    #TODO: Make janky testing non-janky
    test_example_data(app, db_uri="postgresql:///chatty")
    # test_seed_once(app, db_uri="postgresql:///chatty")
    # connect_to_db(app, db_uri="postgresql:///chatty")
    print "Connected to DB."


