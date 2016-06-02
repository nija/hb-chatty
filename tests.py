'''Tests for chatty'''
import unittest
import doctest
import json
from datetime import datetime
from server import app
from model import MyJSONEncoder, Message, User, Room, RoomUser, db, connect_to_db, seed_force, seed_once


travis_db_uri = "postgresql:///travis_ci_test"
# class ChatModelTests(unittest.TestCase):
#     '''Tests for the data model and ORM'''

#     def setUp(self):
#         '''What to do before each test'''
#         # Use the nicer JSONEncoder
#         app.json_encoder = MyJSONEncoder
#         # Configure the app
#         app.config['TESTING'] = True
#         app.config['SECRET_KEY'] = 'BalloonicornSmash'
#         # Connect to the database
#         connect_to_db(app, db_uri="postgresql:///cha")
#         # Reset the world so we start with clean data
#         seed_force(app)

#     def tearDown(self):
#         '''What to do after each test'''
#         # Make sure nothing exists and session is closed
#         db.session.close()
#         db.drop_all()

# def load_tests(loader, tests, ignore):
#     """Also run our doctests and file-based doctests."""
#     tests.addTests(doctest.DocTestSuite("server.py"))
#     tests.addTests(doctest.DocFileSuite("tests.txt"))
#     return tests


class ChatAPITests(unittest.TestCase):
    '''Integration tests for the API routes'''

    def setUp(self):
        '''What to do before each test'''
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'BalloonicornSmash'
        # app.config['SQLALCHEMY_ECHO'] = True
        # Connect to the database
        connect_to_db(app, db_uri=travis_db_uri)
        # Reset the world so we start with clean data,
        # but first, avoid the Heisenbug...
        db.session.commit()
        # print 'seeding'
        seed_force(app)
        # print 'finish seeding'

    def tearDown(self):
        '''What to do after each test'''


    def test_show_all_rooms(self):
        '''Test server.show_all_rooms()'''
        room_name = "lalala"
        new_room = Room(name=room_name)
        db.session.add(new_room)
        db.session.commit()

        result = self.client.get('/api/rooms')
        self.assertIn('"name": "{}",'.format(room_name), result.data)

    def test_show_room(self):
        '''Test server.show_room(room_id)'''

        room_name = "lalala"
        new_room = Room(name=room_name)
        db.session.add(new_room)
        db.session.commit()
        new_room = Room.query.filter(Room.name == room_name).first()
        result = self.client.get('/api/rooms/{}'.format(int(new_room.room_id)))
        self.assertIn('"name": "{}",'.format(new_room.name), result.data)
        self.assertIn('"room_id": {}'.format(new_room.room_id), result.data)

    def test_show_room_message(self):
        '''Test GET server.show_room_messages for all four path options.
        /api/rooms/<int:room_id>/messages
        /api/rooms/<int:room_id>/messages?last_updated=<datetime:last_updated>
        /api/rooms/<int:room_id>/messages?limit_responses=<int:limit_responses>
        /api/rooms/<int:room_id>/messages?last_updated=<datetime:last_updated>&limit_responses=<int:limit_responses>
        '''
        # Background Context:
        # Flask's app.test_client normally resets the session scope
        # upon every call to the test_client. Model objects are bound to the
        # session. Because each call to the test_client ends the scope of a
        # session, all the Model objects become detached and difficult to work
        # with.
        # To solve this, we explicitly set the scope as shared so we can issue
        # multiple calls to test_client without having to re-bind our objects
        # to each new session. That's the whole purpose of this next line.
        # Note: There's still something strange going on with session scoping

        with self.client as test_client:
            # if True:
            room_name = "lalala"
            room_msg1 = 'What a happy penguin am I!'
            room_msg2 = "It's practically impossible to look at a penguin and feel angry."
            room_msg3 = 'Burn everything'
            user_name = 'Penny Penguin'

            # Create a room
            new_room = Room(name=room_name)
            db.session.add(new_room)
            db.session.commit()

            # Create a user
            penny_penguin = User(user_name)
            db.session.add(penny_penguin)
            db.session.commit()

            # Add the user to the room
            # new_room = Room.query.filter(Room.name == room_name).first()
            # penny_penguin = User.query.filter(User.name == user_name).first()
            balloonicorn = User.query.get(1)
            anonymouse = User.query.get(2)

            # print type(balloonicorn), balloonicorn, balloonicorn.user_id
            # print type(anonymouse), anonymouse, anonymouse.user_id
            # db.session.add(main_room.join_room(anonymouse))
            db.session.add(new_room.join_room(penny_penguin))
            db.session.add(new_room.join_room(balloonicorn))
            db.session.add(new_room.join_room(anonymouse))
            db.session.commit()

            # import pdb; pdb.set_trace()

            # print type(balloonicorn), balloonicorn, balloonicorn.user_id
            # print type(anonymouse), anonymouse, anonymouse.user_id

            # Have the user say something in the room
            #result = self.client.get('/api/rooms/{}'.format(int(new_room.room_id)))
            # import pdb; pdb.set_trace()

            result_post_1 = test_client.post(
                # result_post_1 = self.client.post(
                '/api/rooms/{}/messages'.format(int(new_room.room_id)),
                data={
                    'data': room_msg1,
                    'user_id': anonymouse.user_id
                })

            # print "\n\n\nYO\n"
            # import pdb; pdb.set_trace()
            balloonicorn.name

            # balloonicorn = db.session.merge(balloonicorn)
            # print "\n\n\n"

            # print "Result POST 1: \n", result_post_1.data
            # penny_penguin = db.session.merge(penny_penguin)
            # anonymouse = db.session.merge(anonymouse)
            # balloonicorn = db.session.merge(balloonicorn)
            # new_room = db.session.merge(new_room)

            # FIXME: Make this a proper datestamp
            # time_stamp = datetime.now().strftime()
            result_post_2 = test_client.post(
                # result_post_2 = self.client.post(
                '/api/rooms/{}/messages'.format(int(new_room.room_id)),
                data={
                    'data': room_msg2,
                    'user_id': penny_penguin.user_id
                })

            # import pdb; pdb.set_trace()

            # print "Result POST 2: \n", result_post_2.data
            # penny_penguin = db.session.merge(penny_penguin)
            # anonymouse = db.session.merge(anonymouse)
            # balloonicorn = db.session.merge(balloonicorn)
            # new_room = db.session.merge(new_room)

            result_post_3 = test_client.post(
                '/api/rooms/{}/messages'.format(int(new_room.room_id)),
                data={
                    'data': room_msg3,
                    'user_id': balloonicorn.user_id
                })

            # print "Result POST 3: \n", result_post_3.data
            # penny_penguin = db.session.merge(penny_penguin)
            # anonymouse = db.session.merge(anonymouse)
            # balloonicorn = db.session.merge(balloonicorn)
            # new_room = db.session.merge(new_room)

            # import pdb; pdb.set_trace()
            result_get_3 = test_client.get(
                '/api/rooms/{}/messages'.format(int(new_room.room_id)))
            # print "Result GET 3: \n", result_get_3.data

            # time_stamp = datetime.timestamp()  #FIXME: get this into unix time?
            # result4 = self.client.get(
            #     '/api/rooms/{}/messages?last_updated={}'.format(int(new_room.room_id),time_stamp))
            # print "Result 4: \n", result4.data

            # penny_penguin = db.session.merge(penny_penguin)
            # anonymouse = db.session.merge(anonymouse)
            # balloonicorn = db.session.merge(balloonicorn)
            # new_room = db.session.merge(new_room)

            jason = json.loads(result_get_3.data)
            msg_list = jason["messages"]

            self.assertIn(penny_penguin.name, result_get_3.data)
            self.assertIn(room_msg1, result_get_3.data)
            self.assertIn(room_msg2, result_get_3.data)
            self.assertEqual(len(msg_list), 3)

    def test_create_room_message(self):
        '''Test POST server.show_room_messages'''
        room_name = "lalala"
        room_msg = 'What a happy penguin!'
        user_name = 'Penny Penguin'

        # Create a room
        new_room = Room(name=room_name)
        db.session.add(new_room)
        db.session.commit()

        # Create a user
        new_user = User(user_name)
        db.session.add(new_user)
        db.session.commit()

        # Add the user to the room
        new_room = Room.query.filter(Room.name == room_name).first()
        new_user = User.query.filter(User.name == user_name).first()
        db.session.add(new_room.join_room(new_user))
        db.session.commit()

        # Have the user say something in the room
        result = self.client.post(
            '/api/rooms/{}/messages'.format(int(new_room.room_id)),
            data={
                'data': room_msg,
                'user_id': new_user.user_id
            })
        jason = json.loads(result.data)
        msg_list = jason["messages"]
        self.assertIn(new_user.name, result.data)
        self.assertIn(room_msg, result.data)
        # We know there should only be one message because everything
        # gets recreated before and after each test
        self.assertEqual(len(msg_list), 1)

    def test_show_room_users(self):
        '''Test GET server.show_room_users'''
        with self.client as test_client:
            room_name = "tesseract"
            user_name = 'Penny Penguin'

            # Create a room
            new_room = Room(name=room_name)
            db.session.add(new_room)
            db.session.commit()

            # Create a user
            penny_penguin = User(user_name)
            db.session.add(penny_penguin)
            db.session.commit()

            # Add the user to the room
            new_room = Room.query.filter(Room.name == room_name).first()
            penny_penguin = User.query.filter(User.name == user_name).first()
            balloonicorn = User.query.get(1)
            anonymouse = User.query.get(2)

            # print type(balloonicorn), balloonicorn, balloonicorn.user_id
            # print type(anonymouse), anonymouse, anonymouse.user_id
            # db.session.add(main_room.join_room(anonymouse))
            db.session.add(new_room.join_room(penny_penguin))
            db.session.add(new_room.join_room(balloonicorn))
            db.session.add(new_room.join_room(anonymouse))
            db.session.commit()

            result = test_client.get(
                '/api/rooms/{}/users'.format(int(new_room.room_id)))
            # print "rooms and users:\n", result.data
            self.assertIn('"name": "{}",'.format(
                penny_penguin.name), result.data)

    def test_create_room_users(self):
        '''Test POST server.show_room_users'''

        with self.client as test_client:
            room_name = "tesseract"
            user_name = 'Penny Penguin'

            # Create a room
            new_room = Room(name=room_name)
            db.session.add(new_room)
            db.session.commit()

            # Create a user
            penny_penguin = User(user_name)
            db.session.add(penny_penguin)
            db.session.commit()

            # Add the user to the room
            new_room = Room.query.filter(Room.name == room_name).first()
            penny_penguin = User.query.filter(User.name == user_name).first()

            result_post_1 = test_client.post(
                '/api/rooms/{}/users'.format(int(new_room.room_id)),
                data={
                    'user_id': penny_penguin.user_id
                })
            # print "result_post_1:\n", result_post_1.data
            penny_penguin
            self.assertIn('"name": "{}",'.format(
                penny_penguin.name), result_post_1.data)

    def test_show_all_users(self):
        '''Test server.show_all_rooms()'''
        # Create a user
        penny_penguin = User('Penny Penguin')
        db.session.add(penny_penguin)
        db.session.commit()
        result = self.client.get('/api/users')
        self.assertIn('"name": "{}",'.format(penny_penguin.name), result.data)

    def test_create_user(self):
        '''Test server.create_user()'''
        name = 'Penny Penguin'
        result = self.client.post('/api/users',
            data={
                'name': name
            })
        user = User.query.filter(User.name == name).first()

        # import pdb; pdb.set_trace()
        self.assertIn('"name": "{}",'.format(name), result.data)
        self.assertEqual(name, user.name)

    def test_show_user(self):
        '''Test server.show_user()'''
        # Get Balloonicorn
        user = User.query.get(1)
        result = self.client.get('/api/users/{}'.format(int(user.user_id)))
        self.assertIn(user.name, result.data)

    def test_show_user_rooms(self):
        '''Test server.show_user()'''
        # Get Balloonicorn
        user = User.query.get(1)
        result = self.client.get('/api/users/{}/rooms'.format(int(user.user_id)))
        data = json.loads(result.data)
        # print "\ndata: ", type(data), len(data), data
        # print user.rooms
        # print len(user.rooms)

        # import pdb; pdb.set_trace()
        self.assertEqual(len(user.rooms), len(data))

    def test_show_user_messages(self):
        '''Test server.show_user()'''
        with self.client as test_client:
            # Get Balloonicorn
            user = User.query.get(1)
            room = Room.query.get(1)
            msg1 = Message(user, room)
            msg2 = Message(user, room, data="Victory!")
            msg3 = Message(user, room, data="This point is ours!")
            db.session.add_all([msg1, msg2, msg3])
            db.session.commit()

            # user
            result = test_client.get('/api/users/{}/messages'.format(int(user.user_id)))
            data = json.loads(result.data)
            # print len(data["messages"]), data["messages"]
            # print len(user.messages), user.messages

            # import pdb; pdb.set_trace()
            self.assertEqual(len(user.messages), len(data["messages"]))

    # def test_sparklebot_handle_event(self):
    #     '''Test POST SparkleBot.handle_event'''
    #     room_name = "lalala"
    #     room_msg = 'Pyro weather 94501'
    #     user_name = 'Penny Penguin'

    #     # Create a room
    #     new_room = Room(name=room_name)
    #     db.session.add(new_room)
    #     db.session.commit()

    #     # Create a user
    #     new_user = User(user_name)
    #     db.session.add(new_user)
    #     db.session.commit()

    #     # Add the user to the room
    #     new_room = Room.query.filter(Room.name == room_name).first()
    #     new_user = User.query.filter(User.name == user_name).first()
    #     db.session.add(new_room.join_room(new_user))
    #     db.session.commit()

    #     # Have the user say something in the room
    #     result = self.client.post(
    #         '/api/rooms/{}/messages'.format(int(new_room.room_id)),
    #         data={
    #             'data': room_msg,
    #             'user_id': new_user.user_id
    #         })

    #     jason = json.loads(result.data)
    #     msg_list = jason["messages"]
    #     print msg_list
    #     # self.assertIn(new_user.name, result.data)
    #     # self.assertIn(room_msg, result.data)
    #     # # We know there should only be one message because everything
    #     # # gets recreated before and after each test
    #     # self.assertEqual(len(msg_list), 1)





class ChatWebTests(unittest.TestCase):
    """Tests for the routes"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'BalloonicornSmash'
        # Connect to the database
        connect_to_db(app, db_uri=travis_db_uri)
        # Reset the world so we start with clean data
        seed_force(app)

    def test_home_page(self):
        '''Checking the root route'''
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)

    def test_path_to_favicon(self):
        '''Checking the favicon route'''
        result = self.client.get("/favicon.ico")
        self.assertEqual(result.status_code, 200)

    def test_path_to_healthcheck(self):
        '''Checking route to healthcheck'''
        result = self.client.get("/healthcheck")
        self.assertEqual(result.status_code, 200)

    def test_path_to_ping(self):
        '''Checking route to ping'''
        result = self.client.get("/ping")
        self.assertEqual(result.status_code, 200)

    # def test_rsvp(self):
    #     '''Checking... post something something'''
    #     result = self.client.post("/process_msg_event",
    #                               data={'name': "Jane", 'data': "jane@jane.com"},
    #                               follow_redirects=True)

    #     self.assertIn("jane@jane", result.data)
    #     self.assertEqual(result.status_code, 200)
        #self.assertNotIn("Please RSVP", result.data)


if __name__ == "__main__":
    unittest.main()
