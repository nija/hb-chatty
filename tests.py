'''Tests for chatty'''
import unittest
import doctest
import json
from server import app
from model import MyJSONEncoder, Message, User, Room, RoomUser, db, connect_to_db, seed_once, seed_force


travis_db_uri="postgresql:///travis_ci_test"
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
        # Connect to the database
        connect_to_db(app, db_uri=travis_db_uri)
        # Reset the world so we start with clean data
        seed_force(app)

    def tearDown(self):
        '''What to do after each test'''
        pass



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
        '''Test GET server.show_room_messages'''
        room_name = "lalala"
        room_msg1 = 'What a happy penguin am I!'
        room_msg2 = "It's practically impossible to look at a penguin and feel angry."
        room_msg3 = 'Burn Everything'
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
        #db.session.add(main_room.join_room(anonymouse))
        db.session.add(new_room.join_room(penny_penguin))
        db.session.add(new_room.join_room(balloonicorn))
        db.session.add(new_room.join_room(anonymouse))
        db.session.commit()
        print type(balloonicorn), balloonicorn, balloonicorn.user_id
        print type(anonymouse), anonymouse, anonymouse.user_id
        # Have the user say something in the room
        #result = self.client.get('/api/rooms/{}'.format(int(new_room.room_id)))
        # import pdb; pdb.set_trace()
        result_post_1 = self.client.post(
            '/api/rooms/{}/messages'.format(int(new_room.room_id)),
             data = {
                'data': room_msg1,
                'user_id': anonymouse.user_id
                })
        print "Result POST 1: \n", result_post_1.data
        penny_penguin = db.session.merge(penny_penguin)
        anonymouse = db.session.merge(anonymouse)
        balloonicorn = db.session.merge(balloonicorn)
        new_room = db.session.merge(new_room)
        #FIXME: Why can't I post with Balloonicorn or Anonymouse?
        result_post_2 = self.client.post(
            '/api/rooms/{}/messages'.format(int(new_room.room_id)),
             data = {
                'data': room_msg2,
                'user_id': penny_penguin.user_id
                })
        print "Result POST 2: \n", result_post_2.data
        penny_penguin = db.session.merge(penny_penguin)
        anonymouse = db.session.merge(anonymouse)
        balloonicorn = db.session.merge(balloonicorn)
        new_room = db.session.merge(new_room)

        result_post_3 = self.client.post(
            '/api/rooms/{}/messages'.format(int(new_room.room_id)),
             data = {
                'data': room_msg3,
                'user_id': balloonicorn.user_id
                })
        print "Result POST 3: \n", result_post_3.data
        penny_penguin = db.session.merge(penny_penguin)
        anonymouse = db.session.merge(anonymouse)
        balloonicorn = db.session.merge(balloonicorn)
        new_room = db.session.merge(new_room)

        result_get_3 = self.client.get(
            '/api/rooms/{}/messages'.format(int(new_room.room_id)))
        print "Result GET 3: \n", result_get_3.data
        # time_stamp = datetime.timestamp()  #FIXME: get this into unix time?
        # result4 = self.client.get(
        #     '/api/rooms/{}/messages?last_updated={}'.format(int(new_room.room_id),time_stamp))
        # print "Result 4: \n", result4.data

        penny_penguin = db.session.merge(penny_penguin)
        anonymouse = db.session.merge(anonymouse)
        balloonicorn = db.session.merge(balloonicorn)
        new_room = db.session.merge(new_room)

        jason = json.loads(result_get_3.data)
        msg_list = jason["messages"]
        self.assertIn(penny_penguin.name, result_get_3.data)
        self.assertIn(room_msg1, result_get_3.data)
        self.assertIn(room_msg2, result_get_3.data)
        self.assertEqual(len(msg_list), 2)


    def test_create_room_message(self):
        '''Test POST server.show_room_messages'''
        room_name = "lalala"
        room_msg = 'What a happy penguin!'
        user_name = 'Linux'
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
        #db.session.add(main_room.join_room(anonymouse))
        db.session.add(new_room.join_room(new_user))
        db.session.commit()
        # Have the user say something in the room
        #result = self.client.get('/api/rooms/{}'.format(int(new_room.room_id)))
        result = self.client.post(
            '/api/rooms/{}/messages'.format(int(new_room.room_id)),
             data = {
                'data': room_msg,
                'user_id': new_user.user_id
                })
        jason = json.loads(result.data)
        msg_list = jason["messages"]
        self.assertIn(new_user.name, result.data)
        self.assertIn(room_msg, result.data)
        self.assertEqual(len(msg_list), 1)









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
        '''Checking the root route'''
        result = self.client.get("/favicon.ico")
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


