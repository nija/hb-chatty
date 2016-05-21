'''Tests for chatty'''
import unittest
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

    def test_show_all_rooms(self):
        room_name = "lalala"
        new_room = Room(name=room_name)
        db.session.add(new_room)
        db.session.commit()
        result = self.client.get('/api/rooms')
        self.assertIn(result.data, '"name": "{}",'.format(room_name))

    def tearDown(self):
        pass


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


