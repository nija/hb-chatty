'''Tests for chatty'''
import unittest
import doctest
from server import app
from model import MyJSONEncoder, Message, User, Room, RoomUser, db, connect_to_db, seed_once, seed_force

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
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'BalloonicornSmash'
        # Connect to the database
        connect_to_db(app, db_uri="postgresql:///cha")
        # Reset the world so we start with clean data
        seed_force(app)

    def tearDown(self):
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

    def test_create_room_messages(self):
        '''Test server.show_room_messages'''
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
        self.assertIn(new_user.name, result.data)
        self.assertIn(room_msg, result.data)



class ChatWebTests(unittest.TestCase):
    """Tests for the routes"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'BalloonicornSmash'
        # Connect to the database
        connect_to_db(app, db_uri="postgresql:///cha")
        # Reset the world so we start with clean data
        seed_force(app)

    def test_home_page(self):
        '''Checking the root route'''
        result = self.client.get("/")
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


